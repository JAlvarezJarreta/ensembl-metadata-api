# See the NOTICE file distributed with this work for additional information
#   regarding copyright ownership.
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.`
import re
from collections import defaultdict
import sqlalchemy as db
import sqlalchemy.exc

from ensembl.core.models import Meta, CoordSystem, SeqRegionAttrib, SeqRegion, \
    SeqRegionSynonym, AttribType
from sqlalchemy import select, and_, create_engine
from sqlalchemy import or_
from ensembl.database import DBConnection
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import aliased, Session

from ensembl.production.metadata.api.models import *
from ensembl.production.metadata.updater.base import BaseMetaUpdater
from ensembl.ncbi_taxonomy.api.utils import Taxonomy
from ensembl.ncbi_taxonomy.models import NCBITaxaName
import logging
from ensembl.production.metadata.api.exceptions import *


class CoreMetaUpdater(BaseMetaUpdater):
    def __init__(self, db_uri, metadata_uri, taxonomy_uri, release=None, force=None):
        super().__init__(db_uri, metadata_uri, taxonomy_uri, release, force)
        self.db_type = 'core'
        logging.basicConfig(level=logging.INFO)
        # Single query to get all of the metadata information.
        self.meta_dict = {}
        with self.db.session_scope() as session:
            results = session.query(Meta).all()
            for result in results:
                species_id = result.species_id
                meta_key = result.meta_key
                meta_value = result.meta_value

                if species_id not in self.meta_dict:
                    self.meta_dict[species_id] = {}
                # WARNING! Duplicated meta_keys for a species_id will not error out!. A datacheck is necessary for key values.
                self.meta_dict[species_id][meta_key] = meta_value

    # Basic API for the meta table in the submission database.
    def get_meta_single_meta_key(self, species_id, parameter):
        species_meta = self.meta_dict.get(species_id)
        if species_meta is None:
            return None
        return species_meta.get(parameter)

    def get_meta_list_from_prefix_meta_key(self, species_id, prefix):
        species_meta = self.meta_dict.get(species_id)
        if species_meta is None:
            return None
        result_dict = {k: v for k, v in species_meta.items() if k.startswith(prefix)}
        return result_dict

    def process_core(self, **kwargs):
        # Special case for loading a single species from a collection database. Can be removed in a future release
        sel_species = kwargs.get('species', None)
        if sel_species:
            with self.db.session_scope() as session:
                multi_species = session.execute(
                    select(Meta.species_id).filter(Meta.meta_key == "species.production_name").filter(
                        Meta.meta_value == sel_species).distinct()
                )
        else:
            # Normal handling of collections from here
            # Handle multi-species databases and run an update for each species
            with self.db.session_scope() as session:
                multi_species = session.execute(
                    select(Meta.species_id).filter(Meta.meta_key == "species.production_name").distinct()
                )
        multi_species = [multi_species for multi_species, in multi_species]

        for species in multi_species:
            self.process_species(species)

    def process_species(self, species_id):
        """
        Process an individual species from a core database to update the metadata db.
        This method contains the logic for updating the metadata
        """

        with self.metadata_db.session_scope() as meta_session:
            organism, division, organism_group_member = self.get_or_new_organism(species_id, meta_session)
            assembly, assembly_dataset, assembly_dataset_attributes, assembly_sequences, dataset_source = self.get_or_new_assembly(
                species_id, meta_session)
            genebuild_dataset, genebuild_dataset_attributes = self.get_or_new_genebuild(species_id, meta_session,
                                                                                        dataset_source)

            # Checking for an existing genome uuid:
            old_genome_uuid = self.get_meta_single_meta_key(species_id, "genome.genome_uuid")
            if old_genome_uuid is not None:
                old_genome = meta_session.query(Genome).filter(
                    Genome.genome_uuid == old_genome_uuid).one_or_none()
                # Logic for existing key in database.
                if old_genome is not None:
                    if self.force is False:
                        raise MetadataUpdateException(
                            "Core database contains a genome.genome_uuid which matches an entry in the meta table. "
                            "The force flag was not specified so the core was not updated.")
                    elif self.is_object_new(organism) or self.is_object_new(assembly):
                        raise MetadataUpdateException(
                            "Core database contains a genome.genome_uuid which matches an entry in the meta table"
                            "The assembly data or organism data is new and requires the creation a new uuid. Delete "
                            "the old uuid from the core to continue")
                else:
                    raise MetadataUpdateException(
                        "Database contains a Genome.genome_uuid, but the corresponding data is not in"
                        "the meta table. Please remove it from the meta key and resubmit")

            if self.is_object_new(organism):
                logging.info('New organism')
                # ###############################Checks that dataset is new ##################
                if not self.is_object_new(genebuild_dataset):
                    raise MetadataUpdateException(
                        "New organism, but existing assembly accession and/or genebuild version")
                ###############################################
                # Create genome and populate the database with organism, assembly and dataset
                new_genome, assembly_genome_dataset, genebuild_genome_dataset = self.new_genome(meta_session,
                                                                                                species_id,
                                                                                                organism,
                                                                                                assembly,
                                                                                                assembly_dataset,
                                                                                                genebuild_dataset)
                self.concurrent_commit_genome_uuid(meta_session, species_id, new_genome.genome_uuid)

            elif self.is_object_new(assembly):
                logging.info('New assembly')

                # ###############################Checks that dataset and update are new ##################
                if not self.is_object_new(genebuild_dataset):
                    raise MetadataUpdateException("New assembly, but existing genebuild version")
                ###############################################

                new_genome, assembly_genome_dataset, genebuild_genome_dataset = self.new_genome(meta_session,
                                                                                                species_id,
                                                                                                organism,
                                                                                                assembly,
                                                                                                assembly_dataset,
                                                                                                genebuild_dataset)
                self.concurrent_commit_genome_uuid(meta_session, species_id, new_genome.genome_uuid)

                # Create genome and populate the database with assembly and dataset
            elif self.is_object_new(genebuild_dataset):
                logging.info('New genebuild')
                # Create genome and populate the database with genebuild dataset
                new_genome, assembly_genome_dataset, genebuild_genome_dataset = self.new_genome(meta_session,
                                                                                                species_id,
                                                                                                organism,
                                                                                                assembly,
                                                                                                assembly_dataset,
                                                                                                genebuild_dataset)
                self.concurrent_commit_genome_uuid(meta_session, species_id, new_genome.genome_uuid)

            else:
                # Check if the data has been released:
                if check_release_status(self.metadata_db, genebuild_dataset.dataset_uuid) and not self.force:
                    raise WrongReleaseException("Existing Organism, Assembly, and Datasets within a release. "
                                                "To update released data set force=True. This will force assembly "
                                                "and genebuild"
                                                "dataset updates and assembly sequences.")
                else:
                    logging.info('Rewrite of existing datasets. Only assembly dataset attributes, genebuild '
                                 'dataset, dataset attributes, and assembly sequences are modified.')
                    # In this case, we want to rewrite the existing datasets with new data, but keep the dataset_uuid
                    # Update genebuild_dataset
                    meta_session.query(DatasetAttribute).filter(
                        DatasetAttribute.dataset_id == genebuild_dataset.dataset_id).delete()
                    self.get_or_new_genebuild(species_id,
                                              meta_session,
                                              source=dataset_source,
                                              existing=genebuild_dataset)

                    # #Update assembly_dataset
                    meta_session.query(DatasetAttribute).filter(
                        DatasetAttribute.dataset_id == assembly_dataset.dataset_id).delete()
                    self.get_or_new_assembly(
                        species_id, meta_session, source=dataset_source, existing=assembly_dataset)

    def concurrent_commit_genome_uuid(self, meta_session, species_id, genome_uuid):
        # Currently impossible with myisam without two phase commit (requires full refactor)
        # This is a workaround and should be sufficent.
        with self.db.session_scope() as session:
            meta_session.commit()
            try:
                existing_row = session.query(Meta).filter(
                    and_(
                        Meta.species_id == species_id,
                        Meta.meta_key == 'genome.genome_uuid',
                    )
                ).first()

                if existing_row:
                    session.delete(existing_row)
                new_row = Meta(
                    species_id=species_id,
                    meta_key='genome.genome_uuid',
                    meta_value=genome_uuid
                )
                session.add(new_row)
                session.commit()
            except sqlalchemy.exc.DatabaseError as e:
                raise UpdateBackCoreException(f"Metadata-api failed to insert {genome_uuid} into {self.db_uri} "
                                              f"but it successfully updated the metadata. ")

    def new_genome(self, meta_session, species_id, organism, assembly, assembly_dataset, genebuild_dataset):
        production_name = self.get_meta_single_meta_key(species_id, "species.production_name")
        new_genome = Genome(
            genome_uuid=str(uuid.uuid4()),
            assembly=assembly,
            organism=organism,
            created=func.now(),
            is_best=0,
            production_name=production_name,
        )
        meta_session.add(new_genome)
        assembly_genome_dataset = GenomeDataset(
            genome=new_genome,
            dataset=assembly_dataset,
            is_current=True,
        )
        meta_session.add(assembly_genome_dataset)
        genebuild_genome_dataset = GenomeDataset(
            genome=new_genome,
            dataset=genebuild_dataset,
            is_current=True,
        )
        meta_session.add(genebuild_genome_dataset)
        return new_genome, assembly_genome_dataset, genebuild_genome_dataset

    def get_or_new_organism(self, species_id, meta_session):
        """
        Get an existing Organism instance or create a new one, depending on the information from the metadata database.
        """
        # Fetch the Ensembl name of the organism from metadata using either 'species.biosample_id'
        # or 'species.production_name' as the key.
        biosample_id = self.get_meta_single_meta_key(species_id, "organism.biosample_id")
        if biosample_id is None:
            biosample_id = self.get_meta_single_meta_key(species_id, "species.production_name")

        # Getting the common name from the meta table, otherwise we grab it from ncbi.
        common_name = self.get_meta_single_meta_key(species_id, "species.common_name")
        if common_name is None:
            taxid = self.get_meta_single_meta_key(species_id, "species.taxonomy_id")

            with self.taxonomy_db.session_scope() as session:
                common_name = session.query(NCBITaxaName).filter(
                    NCBITaxaName.taxon_id == taxid,
                    NCBITaxaName.name_class == "genbank common name"
                ).one_or_none()
                common_name = common_name.name if common_name is not None else '-'
        # Instantiate a new Organism object using data fetched from metadata.
        new_organism = Organism(
            species_taxonomy_id=self.get_meta_single_meta_key(species_id, "species.species_taxonomy_id"),
            taxonomy_id=self.get_meta_single_meta_key(species_id, "species.taxonomy_id"),
            common_name=common_name,
            scientific_name=self.get_meta_single_meta_key(species_id, "species.scientific_name"),
            biosample_id=biosample_id,
            strain=self.get_meta_single_meta_key(species_id, "species.strain"),
            strain_type=self.get_meta_single_meta_key(species_id, "strain.type"),
            scientific_parlance_name=self.get_meta_single_meta_key(species_id, "species.parlance_name")
        )

        # Query the metadata database to find if an Organism with the same Ensembl name already exists.
        old_organism = meta_session.query(Organism).filter(
            Organism.biosample_id == new_organism.biosample_id).one_or_none()
        division_name = self.get_meta_single_meta_key(species_id, "species.division")
        division = meta_session.query(OrganismGroup).filter(OrganismGroup.name == division_name).one_or_none()

        # If an existing Organism is found, return it and indicate that it already existed.
        if old_organism:
            organism_group_member = meta_session.query(OrganismGroupMember).filter(
                OrganismGroupMember.organism_id == old_organism.organism_id,
                OrganismGroupMember.organism_group_id == division.organism_group_id).one_or_none()

            return old_organism, division, organism_group_member
        else:
            # If no existing Organism is found, conduct additional checks before creating a new one.

            # Check if the new organism's taxonomy ID exists in the taxonomy database.
            with self.taxonomy_db.session_scope() as session:
                try:
                    Taxonomy.fetch_node_by_id(session, new_organism.taxonomy_id)
                except NoResultFound:
                    raise TaxonNotFoundException(
                        f"taxon id {new_organism.taxonomy_id} not found in taxonomy database for scientific name")

            # Check if an Assembly with the same accession already exists in the metadata database.
            accession = self.get_meta_single_meta_key(species_id, "assembly.accession")
            assembly_test = meta_session.query(Assembly).filter(Assembly.accession == accession).one_or_none()
            if assembly_test is not None:
                logging.info("Assembly Accession already exists for a different organism.")

            # Fetch the division name of the new organism from metadata.
            if division_name is None:
                MissingMetaException("No species.division found in meta table")

            # Query the metadata database to find if an OrganismGroup with the same division name already exists.
            if division is None:
                # If no such OrganismGroup exists, create a new one.
                division = OrganismGroup(
                    type="Division",
                    name=division_name,
                )
                meta_session.add(division)

            # Create a new OrganismGroupMember linking the new Organism to the division group.
            organism_group_member = OrganismGroupMember(
                is_reference=0,
                organism=new_organism,
                organism_group=division,
            )
            meta_session.add(new_organism)
            meta_session.add(organism_group_member)
            # Return the newly created Organism and indicate that it is new.
            return new_organism, division, organism_group_member

    def get_assembly_sequences(self, species_id, assembly):
        """
        Get the assembly sequences and the values that correspond to the metadata table
        """
        assembly_sequences = []
        with self.db.session_scope() as session:
            circular_seq_attrib = aliased(SeqRegionAttrib)
            results = (session.query(SeqRegion.name, SeqRegion.length, CoordSystem.name.label("coord_system_name"),
                                     SeqRegionSynonym.synonym, circular_seq_attrib.value.label("is_circular"))
                       .outerjoin(SeqRegion.coord_system)
                       .outerjoin(SeqRegionSynonym, SeqRegionSynonym.seq_region_id == SeqRegion.seq_region_id)
                       .join(SeqRegion.seq_region_attrib)  # For other attributes
                       .outerjoin(circular_seq_attrib,
                                  and_(circular_seq_attrib.seq_region_id == SeqRegion.seq_region_id,
                                       circular_seq_attrib.attrib_type.has(code="circular_seq")))
                       .join(SeqRegionAttrib.attrib_type)
                       .filter(CoordSystem.species_id == species_id)
                       .filter(AttribType.code == "toplevel")
                       .filter(CoordSystem.name != "lrg")
                       .all())
            attributes = (session.query(SeqRegion.name, AttribType.code, SeqRegionAttrib.value)
                          .select_from(SeqRegion)
                          .join(SeqRegionAttrib)
                          .join(AttribType)
                          .filter(or_(AttribType.code == "sequence_location",
                                      AttribType.code == "karyotype_rank")).all())
            attribute_dict = {}
            for name, code, value in attributes:
                if name not in attribute_dict:
                    attribute_dict[name] = {}
                attribute_dict[name][code] = value

            accession_info = defaultdict(
                # The None's here are improper, but they break far too much for this update if they are changed.
                # When accession is decided I will fix them.
                lambda: {
                    "names": set(), "accession": None, "length": None, "location": None, "chromosomal": None,
                    "karyotype_rank": None
                })

            for seq_region_name, seq_region_length, coord_system_name, synonym, is_circular in results:
                accession_info[seq_region_name]["names"].add(seq_region_name)
                if synonym:
                    accession_info[seq_region_name]["names"].add(synonym)

                # Save the sequence location, length, and chromosomal flag.
                location_mapping = {
                    'nuclear_chromosome': 'SO:0000738',
                    'mitochondrial_chromosome': 'SO:0000737',
                    'chloroplast_chromosome': 'SO:0000745',
                    None: 'SO:0000738',
                }
                # Try to get the sequence location
                location = attribute_dict.get(seq_region_name, {}).get("sequence_location", None)

                # Using the retrieved location to get the sequence location
                sequence_location = location_mapping[location]

                # Try to get the karyotype rank
                karyotype_rank = attribute_dict.get(seq_region_name, {}).get("karyotype_rank", None)

                # Test if chromosomal:
                if karyotype_rank is not None:
                    chromosomal = 1
                else:
                    chromosomal = 1 if coord_system_name == "chromosome" else 0

                # Assign the values to the dictionary
                if not accession_info[seq_region_name]["length"]:
                    accession_info[seq_region_name]["length"] = seq_region_length

                if not accession_info[seq_region_name]["location"]:
                    accession_info[seq_region_name]["location"] = sequence_location

                if accession_info[seq_region_name]["chromosomal"] is None:  # Assuming default is None
                    accession_info[seq_region_name]["chromosomal"] = chromosomal

                if not accession_info[seq_region_name]["karyotype_rank"]:
                    accession_info[seq_region_name]["karyotype_rank"] = karyotype_rank

                accession_info[seq_region_name]["type"] = coord_system_name
                accession_info[seq_region_name]["is_circular"] = 1 if is_circular == "1" else 0

            for accession, info in accession_info.items():
                seq_region_name = accession
                assembly_sequence = AssemblySequence(
                    name=seq_region_name,
                    assembly=assembly,
                    accession=accession,
                    chromosomal=info["chromosomal"],
                    length=info["length"],
                    sequence_location=info["location"],
                    chromosome_rank=info["karyotype_rank"],
                    # md5="", Populated after checksums are ran.
                    # sha512t4u="", Populated after checksums are ran.
                    type=info["type"],
                    is_circular=info["is_circular"]
                )

                assembly_sequences.append(assembly_sequence)
        return assembly_sequences

    def get_or_new_assembly(self, species_id, meta_session, source=None, existing=None):
        # Get the new assembly accession  from the core handed over
        assembly_accession = self.get_meta_single_meta_key(species_id, "assembly.accession")
        assembly = meta_session.query(Assembly).filter(Assembly.accession == assembly_accession).one_or_none()
        if source is None:
            dataset_source = self.get_or_new_source(meta_session, "core")
        else:
            dataset_source = source

        if assembly is not None and existing is None:
            # Get the existing assembly dataset
            assembly_dataset = meta_session.query(Dataset).filter(Dataset.label == assembly_accession).one_or_none()
            # I should not need this, but double check on database updating.
            assembly_dataset_attributes = assembly_dataset.dataset_attributes
            assembly_sequences = assembly.assembly_sequences

            return assembly, assembly_dataset, assembly_dataset_attributes, assembly_sequences, dataset_source

        else:
            is_reference = 1 if self.get_meta_single_meta_key(species_id, "assembly.is_reference") else 0
            with self.db.session_scope() as session:
                level = (session.execute(db.select(CoordSystem.name).filter(
                    CoordSystem.species_id == species_id).order_by(CoordSystem.rank)).all())[0][0]
                tol_id = self.get_meta_single_meta_key(species_id, "assembly.tol_id")
            if existing is None:
                assembly = Assembly(
                    ucsc_name=self.get_meta_single_meta_key(species_id, "assembly.ucsc_alias"),
                    accession=self.get_meta_single_meta_key(species_id, "assembly.accession"),
                    level=level,
                    name=self.get_meta_single_meta_key(species_id, "assembly.name"),
                    accession_body=self.get_meta_single_meta_key(species_id, "assembly.provider"),
                    assembly_default=self.get_meta_single_meta_key(species_id, "assembly.default"),
                    tol_id=tol_id,
                    created=func.now(),
                    assembly_uuid=str(uuid.uuid4()),
                    url_name=self.get_meta_single_meta_key(species_id, "assembly.url_name"),
                    is_reference=is_reference
                )
            dataset_type = meta_session.query(DatasetType).filter(DatasetType.name == "assembly").first()

            if existing is None:
                assembly_dataset = Dataset(
                    dataset_uuid=str(uuid.uuid4()),
                    dataset_type=dataset_type,  # extract from dataset_type
                    name="assembly",
                    # version=None, Could be changed.
                    label=assembly.accession,  # Required. Makes for a quick lookup
                    created=func.now(),
                    dataset_source=dataset_source,  # extract from dataset_source
                    status='Submitted',
                )
            else:
                assembly_dataset = existing
                assembly_dataset.dataset_source = dataset_source

            attributes = self.get_meta_list_from_prefix_meta_key(species_id, "assembly")
            assembly_dataset_attributes = []
            # Should be able to delete the attribute creation.
            for attribute, value in attributes.items():
                meta_attribute = meta_session.query(Attribute).filter(Attribute.name == attribute).one_or_none()
                if meta_attribute is None:
                    meta_attribute = Attribute(
                        name=attribute,
                        label=attribute,
                        description=attribute,
                        type="string",
                    )
                    # TODO re-add after 2500
                    # raise Exception(f"{attribute} does not exist. Add it to the database and reload.")
                dataset_attribute = DatasetAttribute(
                    value=value,
                    dataset=assembly_dataset,
                    attribute=meta_attribute,
                )
                assembly_dataset_attributes.append(dataset_attribute)
            if existing is None:
                meta_session.add(assembly)
                meta_session.add(assembly_dataset)
                assembly_sequences = self.get_assembly_sequences(species_id, assembly)
                meta_session.add_all(assembly_sequences)
            # Only reload the assembly sequences if the data is not released.
            elif assembly.is_released():
                assembly_sequences = meta_session.query(AssemblySequence).filter(
                    AssemblySequence.assembly_id == assembly.assembly_id)
            else:
                meta_session.query(AssemblySequence).filter(
                    AssemblySequence.assembly_id == assembly.assembly_id).delete()
                assembly_sequences = self.get_assembly_sequences(species_id, assembly)
                meta_session.add_all(assembly_sequences)
            meta_session.add_all(assembly_dataset_attributes)
            return assembly, assembly_dataset, assembly_dataset_attributes, assembly_sequences, dataset_source

    def get_or_new_genebuild(self, species_id, meta_session, source=None, existing=False):
        """
        Process an individual species from a core database to update the metadata db.
        This method contains the logic for updating the metadata
        This is not a get, as we don't update the metadata for genebuild, only replace it if it is not released.
        """
        # The assembly accession and genebuild version are extracted from the metadata of the species
        assembly_accession = self.get_meta_single_meta_key(species_id, "assembly.accession")
        genebuild_version = self.get_meta_single_meta_key(species_id, "genebuild.version")
        if genebuild_version is None:
            raise MissingMetaException("genebuild.version is required in the core database")

        # The genebuild accession is formed by combining the assembly accession and the genebuild version
        genebuild_accession = assembly_accession + "_" + genebuild_version
        if source is None:
            dataset_source = self.get_or_new_source(meta_session, "core")
        else:
            dataset_source = source

        dataset_type = meta_session.query(DatasetType).filter(DatasetType.name == "genebuild").first()

        genebuild_start_date = self.get_meta_single_meta_key(species_id, "genebuild.start_date")
        genebuild_provider_name = self.get_meta_single_meta_key(species_id, "genebuild.provider_name")

        test_status = meta_session.query(Dataset).filter(Dataset.label == genebuild_accession).one_or_none()
        if test_status:
            # Check for genebuild.provider_name
            provider_name_check = meta_session.query(DatasetAttribute).join(Attribute).filter(
                DatasetAttribute.dataset_id == test_status.dataset_id,
                Attribute.name == "genebuild.provider_name",
                DatasetAttribute.value == genebuild_provider_name
            ).one_or_none()

            if provider_name_check:
                # Check for genebuild.start_date
                start_date_check = meta_session.query(DatasetAttribute).join(Attribute).filter(
                    DatasetAttribute.dataset_id == test_status.dataset_id,
                    Attribute.name == "genebuild.start_date",
                    DatasetAttribute.value == genebuild_start_date
                ).one_or_none()

                if start_date_check is None:
                    test_status = None


        if test_status is not None and existing is False:
            genebuild_dataset = test_status
            genebuild_dataset_attributes = genebuild_dataset.dataset_attributes
            return genebuild_dataset, genebuild_dataset_attributes

        if existing is False:
            genebuild_dataset = Dataset(
                dataset_uuid=str(uuid.uuid4()),
                dataset_type=dataset_type,
                name="genebuild",
                version=genebuild_version,
                label=genebuild_accession,
                created=func.now(),
                dataset_source=dataset_source,
                status='Submitted',
            )
        else:
            genebuild_dataset = existing
            genebuild_dataset.label = genebuild_accession
            genebuild_dataset.dataset_source = dataset_source
            genebuild_dataset.version = genebuild_version

        attributes = self.get_meta_list_from_prefix_meta_key(species_id, "genebuild.")

        genebuild_dataset_attributes = []
        for attribute, value in attributes.items():
            meta_attribute = meta_session.query(Attribute).filter(Attribute.name == attribute).one_or_none()
            if meta_attribute is None:
                # TODO: This will be removed after the 2000 species are loaded.
                meta_attribute = Attribute(
                    name=attribute,
                    label=attribute,
                    description=attribute,
                    type="string",
                )
            # raise Exception(f"{attribute} does not exist. Add it to the database and reload.")
            dataset_attribute = DatasetAttribute(
                value=value,
                dataset=genebuild_dataset,
                attribute=meta_attribute,
            )
            genebuild_dataset_attributes.append(dataset_attribute)
        # TODO: These should be deleted eventually as the paramaters have been changed to genebuild.XXX but not until the 241.
        # Grab the necessary sample data and add it as an datasetattribute
        gene_param_attribute = meta_session.query(Attribute).filter(Attribute.name == "sample.gene_param").one_or_none()
        if gene_param_attribute is None:
            gene_param_attribute = Attribute(
                name="sample.gene_param",
                label="sample.gene_param",
                description="Sample Gene Data",
                type="string",
            )
        sample_gene_param = DatasetAttribute(
            value=self.get_meta_single_meta_key(species_id, "sample.gene_param"),
            dataset=genebuild_dataset,
            attribute=gene_param_attribute,
        )
        genebuild_dataset_attributes.append(sample_gene_param)
        sample_location_attribute = meta_session.query(Attribute).filter(
            Attribute.name == "sample.location_param").one_or_none()
        if sample_location_attribute is None:
            sample_location_attribute = Attribute(
                name="sample.location_param",
                label="sample.location_param",
                description="Sample Location Data",
                type="string",
            )
        sample_location_param = DatasetAttribute(
            value=self.get_meta_single_meta_key(species_id, "sample.location_param"),
            dataset=genebuild_dataset,
            attribute=sample_location_attribute,
        )
        genebuild_dataset_attributes.append(sample_location_param)

        return genebuild_dataset, genebuild_dataset_attributes

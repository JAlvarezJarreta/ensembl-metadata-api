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
#   limitations under the License.
import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker
import pymysql
from ensembl.production.metadata.config import get_metadata_uri, get_taxonomy_uri
from ensembl.database.dbconnection import DBConnection
from ensembl.production.metadata.models import *


#Database ORM connection.
class load_database(DBConnection):
    """
    Load a database and directly create a session for ORM interaction with the database
    """
    def create_session(self, engine):
        self._session = Session(engine, future=True)

    def __init__(self, url):
        super().__init__(url)
        self.create_session(self._engine)

    #Commit any changes to the database and create a new session instance.
    def commit(self):
        self._session.commit()
        self._session.close()
        self.create_session(self._engine)

    #rollback any changes made before commiting the session instance.
    def rollback(self):
        self._session.rollback()


def check_parameter(param):
    if param is not None and not isinstance(param, list):
        param = [param]
    return param


class BaseAdaptor:
    def __init__(self, metadata_uri=None):
        if metadata_uri is None:
            metadata_uri = get_metadata_uri()
        self.metadata_db = load_database(metadata_uri)


class ReleaseAdaptor(BaseAdaptor):
    def fetch_releases(
        self,
        release_id=None,
        release_version=None,
        current_only=True,
        release_type=None,
        site_name=None,
    ):
        release_id = check_parameter(release_id)
        release_version = check_parameter(release_version)
        release_type = check_parameter(release_type)
        site_name = check_parameter(site_name)


        #SELECT ensembl_release.release_id, ensembl_release.version AS release_version, ensembl_release.release_date, ensembl_release.label AS release_label, ensembl_release.is_current, ensembl_release.release_type, ensembl_site.name AS site_name, ensembl_site.label AS site_label, ensembl_site.uri AS site_uri
        #FROM ensembl_release JOIN ensembl_site ON ensembl_site.site_id = ensembl_release.site_id
        release_select = db.select(
            EnsemblRelease.release_id,
            EnsemblRelease.version.label("release_version"),
            EnsemblRelease.release_date,
            EnsemblRelease.label.label("release_label"),
            EnsemblRelease.is_current,
            EnsemblRelease.release_type,
            EnsemblSite.name.label("site_name"),
            EnsemblSite.label.label("site_label"),
            EnsemblSite.uri.label("site_uri")
        ).join(EnsemblRelease.site)

        #WHERE ensembl_release.release_id = :release_id_1
        if release_id is not None:
            release_select = release_select.filter(
                EnsemblRelease.release_id == release_id
            )
        #WHERE ensembl_release.version = :version_1
        elif release_version is not None:
            release_select = release_select.filter(
                EnsemblRelease.version == release_version
            )
        #WHERE ensembl_release.is_current =:is_current_1
        elif current_only:
            release_select = release_select.filter(
                EnsemblRelease.is_current == 1
            )

        #WHERE ensembl_release.release_type = :release_type_1
        if release_type is not None:
            release_select = release_select.filter(
                EnsemblRelease.release_type == release_type
            )

        #WHERE ensembl_site.name = :name_1
        if site_name is not None:
            release_select = release_select.filter(
                EnsemblSite.name == site_name
            )
        return self.metadata_db._session.execute(release_select)


    def fetch_releases_for_genome(self, genome_uuid, site_name=None):

        # SELECT genome_release.release_id
        # FROM genome_release
        # JOIN genome ON genome.genome_id = genome_release.genome_id
        # WHERE genome.genome_uuid =:genome_uuid_1
        release_id_select = db.select(
            GenomeRelease.release_id
        ).filter(
            Genome.genome_uuid == genome_uuid
        ).join(
            GenomeRelease.genome
        )
        #Don't really like this section. Refactor later.
        release_ids = []
        release_objects = self.metadata_db._session.execute(release_id_select)
        for rid in release_objects:
            release_ids.append(rid[0])

        return self.fetch_releases(release_id=release_ids, site_name=site_name)

    def fetch_releases_for_dataset(self, dataset_uuid, site_name=None):
        dataset = db.Table("dataset", self.md, autoload_with=self.metadata_db)
        genome_dataset = db.Table(
            "genome_dataset", self.md, autoload_with=self.metadata_db
        )

        release_id_select = (
            db.select(genome_dataset.c.release_id)
            .select_from(dataset)
            .filter_by(dataset_uuid=dataset_uuid)
            .join(genome_dataset)
        )

        release_ids = [
            rid for (rid,) in self.metadata_db_session.execute(release_id_select)
        ]

        return self.fetch_releases(release_id=release_ids, site_name=site_name)


TEST = ReleaseAdaptor('mysql://danielp:Killadam69@localhost/ensembl_metadata_2020')
TEST2 = TEST.fetch_releases_for_genome('3704ceb1-948d-11ec-a39d-005056b38ce3')
for i in TEST2:
    print (i)







class GenomeAdaptor(BaseAdaptor):
    taxon_names = {}

    def __init__(self, metadata_uri=None, taxonomy_uri=None):
        super().__init__(metadata_uri)

        if taxonomy_uri is None:
            taxonomy_uri = config.TAXONOMY_URI
        self.taxonomy_db = load_database(taxonomy_uri)
        self.taxonomy_db_session = Session(self.taxonomy_db, future=True)

        # Cache the taxon names; data is in a separate db,
        # which is tricky to fetch elegantly and efficiently otherwise.
        taxonomy_ids = self.fetch_taxonomy_ids()
        self.taxon_names = self.fetch_taxonomy_names(taxonomy_ids)

    def fetch_taxonomy_ids(self):
        organism = db.Table("organism", self.md, autoload_with=self.metadata_db)
        taxonomy_id_select = db.select(organism.c.taxonomy_id.distinct())
        taxonomy_ids = [tid for (tid,) in self.metadata_db.execute(taxonomy_id_select)]
        return taxonomy_ids

    def fetch_taxonomy_names(self, taxonomy_id):
        ncbi_taxa_name = db.Table(
            "ncbi_taxa_name", self.md, autoload_with=self.taxonomy_db
        )

        taxons = {}
        for tid in taxonomy_id:
            names = {"scientific_name": None, "synonym": []}
            taxons[tid] = names

        sci_name_select = db.select(
            ncbi_taxa_name.c.taxon_id, ncbi_taxa_name.c.name
        ).filter(
            ncbi_taxa_name.c.taxon_id.in_(taxonomy_id),
            ncbi_taxa_name.c.name_class == "scientific name",
        )
        for x in self.taxonomy_db.execute(sci_name_select):
            taxons[x.taxon_id]["scientific_name"] = x.name

        synonym_class = [
            "common name",
            "equivalent name",
            "genbank common name",
            "genbank synonym",
            "synonym",
        ]
        synonyms_select = db.select(
            ncbi_taxa_name.c.taxon_id, ncbi_taxa_name.c.name
        ).filter(
            ncbi_taxa_name.c.taxon_id.in_(taxonomy_id),
            ncbi_taxa_name.c.name_class.in_(synonym_class),
        )
        for x in self.taxonomy_db.execute(synonyms_select):
            taxons[x.taxon_id]["synonym"].append(x.name)

        return taxons

    def fetch_genomes(
        self,
        genome_id=None,
        genome_uuid=None,
        assembly_accession=None,
        ensembl_name=None,
        taxonomy_id=None,
        unreleased_only=False,
        site_name=None,
        release_type=None,
        release_version=None,
        current_only=True,
    ):
        genome_id = check_parameter(genome_id)
        genome_uuid = check_parameter(genome_uuid)
        assembly_accession = check_parameter(assembly_accession)
        ensembl_name = check_parameter(ensembl_name)
        taxonomy_id = check_parameter(taxonomy_id)

        genome = db.Table("genome", self.md, autoload_with=self.metadata_db)
        assembly = self.md.tables["assembly"]
        organism = self.md.tables["organism"]

        genome_select = (
            db.select(
                genome.c.genome_id,
                genome.c.genome_uuid,
                organism.c.ensembl_name,
                organism.c.url_name,
                organism.c.display_name,
                organism.c.strain,
                organism.c.taxonomy_id,
                assembly.c.accession.label("assembly_accession"),
                assembly.c.name.label("assembly_name"),
                assembly.c.ucsc_name.label("assembly_ucsc_name"),
                assembly.c.level.label("assembly_level"),
            )
            .select_from(genome)
            .join(assembly)
            .join(organism)
        )

        if unreleased_only:
            genome_release = db.Table(
                "genome_release", self.md, autoload_with=self.metadata_db
            )

            genome_select = genome_select.outerjoin(genome_release).filter_by(
                genome_id=None
            )

        elif site_name is not None:
            genome_release = db.Table(
                "genome_release", self.md, autoload_with=self.metadata_db
            )
            release = self.md.tables["ensembl_release"]
            site = self.md.tables["ensembl_site"]

            genome_select = (
                genome_select.join(genome_release)
                .join(release)
                .join(site)
                .filter_by(name=site_name)
            )

            if release_type is not None:
                genome_select = genome_select.filter(
                    release.c.release_type == release_type
                )

            if current_only:
                genome_select = genome_select.filter(genome_release.c.is_current == 1)

            if release_version is not None:
                genome_select = genome_select.filter(
                    release.c.version <= release_version
                )

        # These options are in order of decreasing specificity,
        # and thus the ones later in the list can be redundant.
        if genome_id is not None:
            genome_select = genome_select.filter(genome.c.genome_id.in_(genome_id))
        elif genome_uuid is not None:
            genome_select = genome_select.filter(genome.c.genome_uuid.in_(genome_uuid))
        elif assembly_accession is not None:
            genome_select = genome_select.filter(
                assembly.c.accession.in_(assembly_accession)
            )
        elif ensembl_name is not None:
            genome_select = genome_select.filter(
                organism.c.ensembl_name.in_(ensembl_name)
            )
        elif taxonomy_id is not None:
            genome_select = genome_select.filter(
                organism.c.taxonomy_id.in_(taxonomy_id)
            )

        for result in self.metadata_db_session.execute(genome_select):
            taxon_names = self.taxon_names[result.taxonomy_id]
            result_dict = dict(result)
            result_dict.update(taxon_names)
            yield result_dict

    def fetch_genomes_by_genome_uuid(
        self,
        genome_uuid,
        unreleased_only=False,
        site_name=None,
        release_type=None,
        release_version=None,
        current_only=True,
    ):
        return self.fetch_genomes(
            genome_uuid=genome_uuid,
            unreleased_only=unreleased_only,
            site_name=site_name,
            release_type=release_type,
            release_version=release_version,
            current_only=current_only,
        )

    def fetch_genomes_by_assembly_accession(
        self,
        assembly_accession,
        unreleased_only=False,
        site_name=None,
        release_type=None,
        release_version=None,
        current_only=True,
    ):
        return self.fetch_genomes(
            assembly_accession=assembly_accession,
            unreleased_only=unreleased_only,
            site_name=site_name,
            release_type=release_type,
            release_version=release_version,
            current_only=current_only,
        )

    def fetch_genomes_by_ensembl_name(
        self,
        ensembl_name,
        unreleased_only=False,
        site_name=None,
        release_type=None,
        release_version=None,
        current_only=True,
    ):
        return self.fetch_genomes(
            ensembl_name=ensembl_name,
            unreleased_only=unreleased_only,
            site_name=site_name,
            release_type=release_type,
            release_version=release_version,
            current_only=current_only,
        )

    def fetch_genomes_by_taxonomy_id(
        self,
        taxonomy_id,
        unreleased_only=False,
        site_name=None,
        release_type=None,
        release_version=None,
        current_only=True,
    ):
        return self.fetch_genomes(
            taxonomy_id=taxonomy_id,
            unreleased_only=unreleased_only,
            site_name=site_name,
            release_type=release_type,
            release_version=release_version,
            current_only=current_only,
        )

    def fetch_genomes_by_scientific_name(
        self,
        scientific_name,
        unreleased_only=False,
        site_name=None,
        release_type=None,
        release_version=None,
        current_only=True,
    ):
        taxonomy_ids = [
            t_id
            for t_id in self.taxon_names
            if self.taxon_names[t_id]["scientific_name"] == scientific_name
        ]

        return self.fetch_genomes_by_taxonomy_id(
            taxonomy_ids,
            unreleased_only=unreleased_only,
            site_name=site_name,
            release_type=release_type,
            release_version=release_version,
            current_only=current_only,
        )

    def fetch_genomes_by_synonym(
        self,
        synonym,
        unreleased_only=False,
        site_name=None,
        release_type=None,
        release_version=None,
        current_only=True,
    ):
        taxonomy_ids = []
        for taxon_id in self.taxon_names:
            if synonym.casefold() in [
                x.casefold() for x in self.taxon_names[taxon_id]["synonym"]
            ]:
                taxonomy_ids.append(taxon_id)

        return self.fetch_genomes_by_taxonomy_id(
            taxonomy_ids,
            unreleased_only=unreleased_only,
            site_name=site_name,
            release_type=release_type,
            release_version=release_version,
            current_only=current_only,
        )

    def fetch_sequences(
        self,
        genome_id=None,
        genome_uuid=None,
        assembly_accession=None,
        chromosomal_only=False,
    ):
        genome_id = check_parameter(genome_id)
        genome_uuid = check_parameter(genome_uuid)
        assembly_accession = check_parameter(assembly_accession)

        assembly = db.Table("assembly", self.md, autoload_with=self.metadata_db)
        assembly_sequence = db.Table(
            "assembly_sequence", self.md, autoload_with=self.metadata_db
        )

        seq_select = (
            db.select(
                assembly_sequence.c.accession,
                assembly_sequence.c.name,
                assembly_sequence.c.sequence_location,
                assembly_sequence.c.length,
                assembly_sequence.c.chromosomal,
                assembly_sequence.c.sequence_checksum,
                assembly_sequence.c.ga4gh_identifier,
            )
            .select_from(assembly)
            .join(
                assembly_sequence,
                assembly.c.assembly_id == assembly_sequence.c.assembly_id,
            )
        )
        if chromosomal_only:
            seq_select = seq_select.filter_by(chromosomal=1)

        # These options are in order of decreasing specificity,
        # and thus the ones later in the list can be redundant.
        if genome_id is not None:
            genome = db.Table("genome", self.md, autoload_with=self.metadata_db)
            seq_select = seq_select.join(genome).filter(
                genome.c.genome_id.in_(genome_id)
            )
        elif genome_uuid is not None:
            genome = db.Table("genome", self.md, autoload_with=self.metadata_db)
            seq_select = seq_select.join(genome).filter(
                genome.c.genome_uuid.in_(genome_uuid)
            )
        elif assembly_accession is not None:
            seq_select = seq_select.filter(assembly.c.accession.in_(assembly_accession))

        for result in self.metadata_db_session.execute(seq_select):
            yield dict(result)

    def fetch_sequences_by_genome_uuid(self, genome_uuid, chromosomal_only=False):
        return self.fetch_sequences(
            genome_uuid=genome_uuid, chromosomal_only=chromosomal_only
        )

    def fetch_sequences_by_assembly_accession(
        self, assembly_accession, chromosomal_only=False
    ):
        return self.fetch_sequences(
            assembly_accession=assembly_accession, chromosomal_only=chromosomal_only
        )

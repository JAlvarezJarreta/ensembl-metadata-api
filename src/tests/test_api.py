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
"""
Unit tests for api module
"""

import pytest

from ensembl.database import UnitTestDB
from ensembl.production.metadata.api.genome import GenomeAdaptor
from ensembl.production.metadata.api.release import ReleaseAdaptor


@pytest.mark.parametrize("multi_dbs", [[{'src': 'ensembl_metadata'}, {'src': 'ncbi_taxonomy'}]],
                         indirect=True)
class TestMetadataDB:
    dbc = None  # type: UnitTestDB

    def test_load_database(self, multi_dbs):
        db_test = ReleaseAdaptor(multi_dbs['ensembl_metadata'].dbc.url)
        assert db_test, "DB should not be empty"

    @pytest.mark.parametrize(
        "allow_unreleased, unreleased_only, current_only, output_count",
        [
            # fetches everything (7 released + 2 unreleased)
            (True, False, True, 9),
            # fetches all released genomes (with current_only=0)
            (False, False, False, 7),
            # fetches released genomes with current_only=1 (default)
            (False, False, True, 6),
            # fetches all unreleased genomes
            (False, True, True, 2),
        ]
    )
    def test_fetch_all_genomes(self, multi_dbs, allow_unreleased, unreleased_only, current_only, output_count):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_genomes(
            allow_unreleased=allow_unreleased,
            unreleased_only=unreleased_only,
            current_only=current_only
        )
        assert len(test) == output_count

    def test_fetch_with_all_args_no_conflict(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_genomes(
            genome_uuid="a733550b-93e7-11ec-a39d-005056b38ce3",
            assembly_accession="GCA_000002985.3",
            assembly_name="WBcel235",
            ensembl_name="caenorhabditis_elegans",
            taxonomy_id="6239",
            group="EnsemblMetazoa",
            allow_unreleased=False,
            site_name="Ensembl",
            release_type="integrated",
            release_version="108.0",
            current_only=True
        )
        assert len(test) == 0

    def test_fetch_with_all_args_conflict(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_genomes(
            genome_uuid="a733550b-93e7-11ec-a39d-005056b38ce3",
            assembly_accession="GCA_000002985.3",
            assembly_name="WBcel235",
            ensembl_name="caenorhabditis_elegans",
            taxonomy_id="9606",  # Conflicting taxonomy_id
            group="EnsemblBacteria",  # Conflicting group
            allow_unreleased=False,
            site_name="Ensembl",
            release_type="integrated",
            release_version="108.0",
            current_only=True
        )
        assert len(test) == 0

    def test_fetch_releases(self, multi_dbs):
        conn = ReleaseAdaptor(multi_dbs['ensembl_metadata'].dbc.url)
        test = conn.fetch_releases(release_id=2)
        # test the one to many connection
        assert test[0].EnsemblSite.name == 'Ensembl'
        assert test[0].EnsemblSite.label == 'Ensembl Genome Browser'
        # test the direct access.
        assert test[0].EnsemblRelease.label == 'Scaling Phase 1'

    # currently only have one release, so the testing is not comprehensive
    def test_fetch_releases_for_genome(self, multi_dbs):
        conn = ReleaseAdaptor(multi_dbs['ensembl_metadata'].dbc.url)
        test = conn.fetch_releases_for_genome('a73351f7-93e7-11ec-a39d-005056b38ce3')
        assert test[0].EnsemblSite.name == 'Ensembl'

    def test_fetch_releases_for_dataset(self, multi_dbs):
        conn = ReleaseAdaptor(multi_dbs['ensembl_metadata'].dbc.url)
        test = conn.fetch_releases_for_dataset('3316fe1a-83e7-46da-8a56-cf2b693d8060')
        assert test[0].EnsemblSite.name == 'Ensembl'

    def test_fetch_taxonomy_names(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_taxonomy_names(taxonomy_ids=[6239, 511145])
        assert test[511145]['scientific_name'] == 'Escherichia coli str. K-12 substr. MG1655'

    def test_fetch_taxonomy_ids(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_taxonomy_ids(taxonomy_names='Caenorhabditis elegans')
        assert test[0] == 6239

    def test_fetch_genomes(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_genomes(genome_uuid='a7335667-93e7-11ec-a39d-005056b38ce3')
        assert test[0].Organism.scientific_name == 'Homo sapiens'

    # def test_fetch_genomes_by_group_division(self, multi_dbs):
    #     conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
    #                          taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
    #     division_filter = 'EnsemblVertebrates'
    #     test = conn.fetch_genomes(group=division_filter)
    #     assert len(test) == 1
#        Other PR will likely change this drastically, so the effort is not really necessary. Their are 7 groups.
#        assert division_filter in division_results

    def test_fetch_genomes_by_genome_uuid(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_genomes_by_genome_uuid('a733550b-93e7-11ec-a39d-005056b38ce3')
        assert test[0].Organism.scientific_name == 'Caenorhabditis elegans'

    def test_fetch_genome_by_ensembl_and_assembly_name(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_genomes(assembly_name='WBcel235', ensembl_name='caenorhabditis_elegans')
        assert test[0].Organism.scientific_name == 'Caenorhabditis elegans'

    def test_fetch_genomes_by_assembly_accession(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_genomes_by_assembly_accession('GCA_000005845.2')
        assert test[0].Organism.scientific_name == 'Escherichia coli str. K-12 substr. MG1655 str. K12 (GCA_000005845)'

    def test_fetch_genomes_by_assembly_sequence_accession(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_sequences(
            genome_uuid='a7335667-93e7-11ec-a39d-005056b38ce3',
            assembly_accession='GCA_000001405.28',
            assembly_sequence_accession='CM000686.2'
        )
        assert test[0].AssemblySequence.name == 'Y'

    def test_fetch_genomes_by_assembly_sequence_accession_empty(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_sequences(
            genome_uuid='s0m3-r4nd0m-g3n3-uu1d-v4lu3',
            assembly_accession='GCA_000001405.28',
            assembly_sequence_accession='CM000686.2'
        )
        assert len(test) == 0

    def test_fetch_genomes_by_ensembl_name(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_genomes_by_ensembl_name('caenorhabditis_elegans')
        assert test[0].Organism.scientific_name == 'Caenorhabditis elegans'

    def test_fetch_genomes_by_taxonomy_id(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_genomes_by_taxonomy_id(6239)
        assert test[0].Organism.scientific_name == 'Caenorhabditis elegans'

    def test_fetch_genomes_by_scientific_name(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_genomes_by_scientific_name(
            scientific_name='Caenorhabditis elegans',
            site_name='Ensembl'
        )
        assert test[0].Organism.scientific_name == 'Caenorhabditis elegans'

    def test_fetch_sequences(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_sequences(assembly_uuid='eeaaa2bf-151c-4848-8b85-a05a9993101e')
        # this test is going to drive me nuts
        # Locally and on GitLab CI/CD: AssemblySequence.accession == 'CHR_HG107_PATCH'
        # in Travis, its: AssemblySequence.accession == 'KI270757.1'
        # to please bothI'm using 'sequence_location' for now
        assert test[0].AssemblySequence.sequence_location == 'SO:0000738'

    def test_fetch_sequences_by_gneome_assembly(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_sequences(
            genome_uuid='a7335667-93e7-11ec-a39d-005056b38ce3',
            assembly_accession='GCA_000001405.28',
            chromosomal_only=False
        )
        assert test[-1].AssemblySequence.chromosomal == 0

    def test_fetch_sequences_chromosomal_only(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_sequences(
            genome_uuid='a7335667-93e7-11ec-a39d-005056b38ce3',
            assembly_accession='GCA_000001405.28',
            chromosomal_only=True
        )
        assert test[-1].AssemblySequence.chromosomal == 1

    @pytest.mark.parametrize(
        "genome_uuid, dataset_uuid, allow_unreleased, unreleased_only, expected_dataset_uuid, expected_count",
        [
            # nothing specified + allow_unreleased -> fetches everything
            (None, None, True, False, "559d7660-d92d-47e1-924e-e741151c2cef", 33),
            # specifying genome_uuid
            ("a73357ab-93e7-11ec-a39d-005056b38ce3", None, False, False, "b4ff55e3-d06a-4772-bb13-81c3207669e3", 5),
            # specifying dataset_uuid
            (None, "0dc05c6e-2910-4dbd-879a-719ba97d5824", False, False, "0dc05c6e-2910-4dbd-879a-719ba97d5824", 1),
            # fetch unreleased datasets only
            (None, None, False, True, "feaa37ea-4217-4d9d-afca-600bdae11b36", 3),
        ]
    )
    def test_fetch_genome_dataset_all(
        self, multi_dbs, genome_uuid,
        dataset_uuid, allow_unreleased,
        unreleased_only, expected_dataset_uuid,
        expected_count
    ):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_genome_datasets(
            genome_uuid=genome_uuid,
            dataset_uuid=dataset_uuid,
            unreleased_only=unreleased_only,
            allow_unreleased=allow_unreleased,
            # fetch all datasets (default: dataset_name="assembly")
            dataset_name="all"
        )
        assert test[0].Dataset.dataset_uuid == expected_dataset_uuid
        assert len(test) == expected_count

    @pytest.mark.parametrize(
        "ensembl_name, assembly_name, use_default_assembly, expected_output",
        [
            ("homo_sapiens", "GRCh37.p13", False, "3704ceb1-948d-11ec-a39d-005056b38ce3"),
            ("homo_sapiens", "GRCh37", True, "3704ceb1-948d-11ec-a39d-005056b38ce3"),
        ]
    )
    def test_fetch_genome_uuid(self, multi_dbs, ensembl_name, assembly_name, use_default_assembly, expected_output):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_genomes(
            ensembl_name=ensembl_name,
            assembly_name=assembly_name,
            use_default_assembly=use_default_assembly,
            allow_unreleased=False,
            current_only=False
        )
        assert len(test) == 1
        assert test[0].Genome.genome_uuid == expected_output

    @pytest.mark.parametrize(
        "ensembl_name, assembly_name, use_default_assembly, expected_output",
        [
            ("homo_sapiens", "GRCh38.p13", False, "a7335667-93e7-11ec-a39d-005056b38ce3"),
            ("homo_sapiens", "GRCh38", True, "a7335667-93e7-11ec-a39d-005056b38ce3"),
        ]
    )
    def test_fetch_genome_uuid_is_current(self, multi_dbs, ensembl_name, assembly_name, use_default_assembly, expected_output):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_genomes(
            ensembl_name=ensembl_name,
            assembly_name=assembly_name,
            use_default_assembly=use_default_assembly,
            allow_unreleased=False
        )
        assert len(test) == 1
        assert test[0].Genome.genome_uuid == expected_output

    @pytest.mark.parametrize(
        "ensembl_name, assembly_name, use_default_assembly",
        [
            ("homo_sapiens", "GRCh37", False),
            ("homo_sapiens", "GRCh37.p13", True),
        ]
    )
    def test_fetch_genome_uuid_empty(self, multi_dbs, ensembl_name, assembly_name, use_default_assembly):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_genomes(
            ensembl_name=ensembl_name,
            assembly_name=assembly_name,
            use_default_assembly=use_default_assembly
        )
        assert len(test) == 0

    def test_popular_species(self, multi_dbs):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_organisms_group_counts()
        # First result should be Human
        assert test[0][2] == 'Human'
        # We should have three assemblies associated with Human (Two for grch37.38 organism + one t2t)
        assert test[0][5] == 3
        for data in test[1:]:
            # All others have only one genome in test DB
            assert data[5] == 1

    @pytest.mark.parametrize(
        "allow_unreleased, output_count, expected_genome_uuid",
        [
            # fetches everything
            (True, 9, "90720316-006c-470b-a7dd-82d28f952264"),
            # fetches released datasets and genomes with current_only=1 (default)
            (False, 6, "a733550b-93e7-11ec-a39d-005056b38ce3"),
        ]
    )
    def test_fetch_genomes_info(self, multi_dbs, allow_unreleased, output_count, expected_genome_uuid):
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test = conn.fetch_genomes_info(
            allow_unreleased_genomes=allow_unreleased,
            allow_unreleased_datasets=allow_unreleased,
            group_type=['division', 'internal']
        )
        output_to_list = list(test)
        assert len(output_to_list) == output_count
        assert output_to_list[0][0]['genome'].Genome.genome_uuid == expected_genome_uuid


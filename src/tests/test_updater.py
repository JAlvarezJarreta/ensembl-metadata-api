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
import os

import pytest
from sqlalchemy import create_engine, MetaData, Table, select
from ensembl.database import UnitTestDB

from ensembl.production.metadata.api.factory import meta_factory
from ensembl.production.metadata.api.genome import GenomeAdaptor


@pytest.mark.parametrize("multi_dbs", [[{'src': 'ensembl_metadata'}, {'src': 'ncbi_taxonomy'},
                                        {'src': 'core_1'}, {'src': 'core_2'}, {'src': 'core_3'}, {'src': 'core_4'}]],
                         indirect=True)
class TestUpdater:
    dbc = None  # type: UnitTestDB

    def test_new_organism(self, multi_dbs):
        test = meta_factory(multi_dbs['core_1'].dbc.url, multi_dbs['ensembl_metadata'].dbc.url)
        test.process_core()
        # Look for organism, assembly and geneset
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        # Test the species
        test_collect = conn.fetch_genomes_by_ensembl_name('Jabberwocky')
        assert test_collect[0].Organism.scientific_name == 'carol_jabberwocky'
        # Test the Assembly
        assert test_collect[0].Assembly.accession == 'weird01'
        # select * from genebuild where version = 999 and name = 'genebuild and label =01
        engine = create_engine(multi_dbs['ensembl_metadata'].dbc.url)
        metadata = MetaData()
        dataset = Table('dataset', metadata, autoload=True, autoload_with=engine)
        query = select([dataset]).where(
            (dataset.c.version == 999) & (dataset.c.name == 'genebuild') & (dataset.c.label == '01')
        )
        row = engine.execute(query).fetchone()
        assert row[-2] == '01'

    #
    def test_update_organism(self, multi_dbs):
        test = meta_factory(multi_dbs['core_2'].dbc.url, multi_dbs['ensembl_metadata'].dbc.url)
        test.process_core()
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test_collect = conn.fetch_genomes_by_ensembl_name('Jabberwocky')
        assert test_collect[0].Organism.scientific_name == 'lewis_carol'

    def test_update_assembly(self, multi_dbs):
        test = meta_factory(multi_dbs['core_3'].dbc.url, multi_dbs['ensembl_metadata'].dbc.url)
        test.process_core()
        conn = GenomeAdaptor(metadata_uri=multi_dbs['ensembl_metadata'].dbc.url,
                             taxonomy_uri=multi_dbs['ncbi_taxonomy'].dbc.url)
        test_collect = conn.fetch_genomes_by_ensembl_name('Jabberwocky')
        assert test_collect[1].Organism.scientific_name == 'lewis_carol'
        assert test_collect[1].Assembly.accession == 'weird02'

    #
    def test_update_geneset(self, multi_dbs):
        test = meta_factory(multi_dbs['core_4'].dbc.url, multi_dbs['ensembl_metadata'].dbc.url)
        test.process_core()
        engine = create_engine(multi_dbs['ensembl_metadata'].dbc.url)
        metadata = MetaData()
        dataset = Table('dataset', metadata, autoload=True, autoload_with=engine)
        query = select([dataset]).where(
            (dataset.c.version == 999) & (dataset.c.name == 'genebuild') & (dataset.c.label == '02')
        )
        row = engine.execute(query).fetchone()
        assert row[-2] == '02'


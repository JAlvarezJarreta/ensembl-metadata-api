#  See the NOTICE file distributed with this work for additional information
#  regarding copyright ownership.
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import logging

import grpc

import ensembl.production.metadata.grpc.ensembl_metadata_pb2_grpc as ensembl_metadata_pb2_grpc
from ensembl_metadata_pb2 import (
    GenomeUUIDRequest,
    GenomeNameRequest,
    ReleaseRequest,
    GenomeSequenceRequest,
    AssemblyIDRequest,
    DatasetAttributesValuesRequest,
    GenomeBySpecificKeywordRequest,
    AssemblyAccessionIDRequest,
    OrganismIDRequest,
    DatasetsRequest,
    GenomeDatatypeRequest,
    GenomeInfoRequest,
    OrganismsGroupRequest,
    AssemblyRegionRequest,
    GenomeAssemblySequenceRegionRequest,
    GenomeTagRequest,
    FTPLinksRequest,
    ReleaseVersionRequest,
    GenomeByReleaseVersionRequest
)


def get_genome(stub, genome_request):
    if isinstance(genome_request, GenomeUUIDRequest):
        genome = stub.GetGenomeByUUID(genome_request)
        print(genome)
    elif isinstance(genome_request, GenomeNameRequest):
        genome = stub.GetGenomeByName(genome_request)
        print(genome)
    else:
        print("Unrecognised request message")
        return

    if genome.genome_uuid == '':
        print("No genome")
        return


def get_genomes_by_specific_keyword(stub, genome_request):
    if isinstance(genome_request, GenomeBySpecificKeywordRequest):
        genomes = stub.GetGenomesBySpecificKeyword(genome_request)
        for genome in genomes:
            print(genome)

def get_genomes(stub):
    request1 = GenomeUUIDRequest(genome_uuid="9caa2cae-d1c8-4cfc-9ffd-2e13bc3e95b1")
    request2 = GenomeUUIDRequest(genome_uuid="rhubarb")
    request3 = GenomeNameRequest(ensembl_name="129S1_SvImJ_v1", site_name="Ensembl")
    request4 = GenomeNameRequest(
        ensembl_name="accipiter_gentilis", site_name="rapid", release_version=13.0
    )
    request5 = GenomeNameRequest(
        ensembl_name="banana", site_name="plants", release_version=104.0
    )
    print("**** Valid UUID ****")
    get_genome(stub, request1)
    print("**** Invalid UUID ****")
    get_genome(stub, request2)
    print("**** Name, no release ****")
    get_genome(stub, request3)
    print("**** Name, past release ****")
    get_genome(stub, request4)
    print("**** Invalid name ****")
    get_genome(stub, request5)


def get_genome_by_keyword(stub):
    request1 = GenomeBySpecificKeywordRequest(common_name="Human")
    request2 = GenomeBySpecificKeywordRequest(assembly_accession_id="GCA_018473315.1")
    request3 = GenomeBySpecificKeywordRequest(assembly_name="HG03540.alt.pat.f1_v2")
    request4 = GenomeBySpecificKeywordRequest(ensembl_name="HG03540.alt.pat.f1_v2")
    request5 = GenomeBySpecificKeywordRequest(scientific_name="Homo sapiens")
    request6 = GenomeBySpecificKeywordRequest(scientific_parlance_name="Human")
    request7 = GenomeBySpecificKeywordRequest(species_taxonomy_id="9606")
    print("**** Search by common_name ****")
    get_genomes_by_specific_keyword(stub, request1)
    print("**** Search by assembly_accession_id ****")
    get_genomes_by_specific_keyword(stub, request2)
    print("**** Search by assembly_name ****")
    get_genomes_by_specific_keyword(stub, request3)
    print("**** Search by ensembl_name ****")
    get_genomes_by_specific_keyword(stub, request4)
    print("**** Search by scientific_name ****")
    get_genomes_by_specific_keyword(stub, request5)
    print("**** Search by scientific_parlance_name ****")
    get_genomes_by_specific_keyword(stub, request6)
    print("**** Search by species_taxonomy_id ****")
    get_genomes_by_specific_keyword(stub, request7)


def get_genomes_by_release_version(stub):
    genome_request = GenomeByReleaseVersionRequest(release_version=110.1)
    print("**** Get genomes by release_version ****")
    genomes = stub.GetGenomesByReleaseVersion(genome_request)
    for genome in genomes:
        print(genome)


def list_genome_sequences(stub):
    request1 = GenomeSequenceRequest(
        genome_uuid="2afef36f-3660-4b8c-819b-d1e5a77c9918", chromosomal_only=True
    )
    genome_sequences1 = stub.GetGenomeSequence(request1)
    print("**** Only chromosomes ****")
    for seq in genome_sequences1:
        print(seq)

    request2 = GenomeSequenceRequest(genome_uuid="2afef36f-3660-4b8c-819b-d1e5a77c9918")
    genome_sequences2 = stub.GetGenomeSequence(request2)
    print("**** All sequences ****")
    for seq in genome_sequences2:
        print(seq)

    request3 = GenomeSequenceRequest(genome_uuid="garbage")
    genome_sequences3 = stub.GetGenomeSequence(request3)
    print("**** Invalid UUID ****")
    for seq in genome_sequences3:
        print(seq)


def list_genome_assembly_sequences(stub):
    request1 = AssemblyRegionRequest(
        genome_uuid="2afef36f-3660-4b8c-819b-d1e5a77c9918",
        chromosomal_only=False
    )
    genome_assembly_sequences1 = stub.GetAssemblyRegion(request1)

    request2 = AssemblyRegionRequest(
        genome_uuid="2afef36f-3660-4b8c-819b-d1e5a77c9918",
        chromosomal_only=True
    )
    genome_assembly_sequences2 = stub.GetAssemblyRegion(request2)
    print("**** Chromosomal and non-chromosomal ****")
    for seq in genome_assembly_sequences1:
        print(seq)

    print("**** Chromosomal_only ****")
    for seq in genome_assembly_sequences2:
        print(seq)


def list_genome_assembly_sequences_region(stub):
    request1 = GenomeAssemblySequenceRegionRequest(
        genome_uuid="9caa2cae-d1c8-4cfc-9ffd-2e13bc3e95b1",
        sequence_region_name="HG03540#1#h1tg000001l"
    )
    genome_assembly_sequences_region1 = stub.GetGenomeAssemblySequenceRegion(request1)
    print("**** Non-chromosomal ****")
    print(genome_assembly_sequences_region1)

    request2 = GenomeAssemblySequenceRegionRequest(
        genome_uuid="2afef36f-3660-4b8c-819b-d1e5a77c9918",
        sequence_region_name="3"
    )
    genome_assembly_sequences_region2 = stub.GetGenomeAssemblySequenceRegion(request2)
    print("**** Chromosomal ****")
    print(genome_assembly_sequences_region2)


def list_releases(stub):
    request1 = ReleaseRequest()
    releases1 = stub.GetRelease(request1)
    print("**** All releases ****")
    for release in releases1:
        print(release)

    request2 = ReleaseRequest(site_name=["Ensembl"])
    releases2 = stub.GetRelease(request2)
    print("**** All Ensembl releases ****")
    for release in releases2:
        print(release)

    request3 = ReleaseRequest(site_name=["Ensembl"], current_only=1)
    releases3 = stub.GetRelease(request3)
    print("**** Current Ensembl release ****")
    for release in releases3:
        print(release)

    request4 = ReleaseRequest(release_label=["2024-09-18"])
    releases4 = stub.GetRelease(request4)
    print("**** Release 2024-09-18 (partial) ****")
    for release in releases4:
        print(release)

    request5 = ReleaseRequest(release_label=["2023-10"])
    releases5 = stub.GetRelease(request5)
    print("**** Release 2023-10 (integrated) ****")
    for release in releases5:
        print(release)

    request6 = ReleaseRequest(release_label=["00-00"])
    releases6 = stub.GetRelease(request6)
    print("**** Release 00-00 (doesn't exist)****")
    for release in releases6:
        print(release)


def list_releases_by_uuid(stub):
    request1 = GenomeUUIDRequest(genome_uuid="a73351f7-93e7-11ec-a39d-005056b38ce3")
    releases1 = stub.GetReleaseByUUID(request1)
    print("**** Release for Narwhal ****")
    for release in releases1:
        print(release)


def get_species_information_by_uuid(stub):
    request1 = GenomeUUIDRequest(genome_uuid="9caa2cae-d1c8-4cfc-9ffd-2e13bc3e95b1")
    releases1 = stub.GetSpeciesInformation(request1)
    print("**** Species information ****")
    print(releases1)


def get_assembly_information(stub):
    request1 = AssemblyIDRequest(assembly_uuid="9d2dc346-358a-4c70-8fd8-3ff194246a76")
    releases1 = stub.GetAssemblyInformation(request1)
    print("**** Assembly information ****")
    print(releases1)


def get_genomes_by_assembly_accession(stub):
    request1 = AssemblyAccessionIDRequest(assembly_accession="GCA_001624185.1")
    genomes1 = stub.GetGenomesByAssemblyAccessionID(request1)
    print("**** Genomes from assembly accession information ****")
    for genome in genomes1:
        print(genome)

    request2 = AssemblyAccessionIDRequest(assembly_accession=None)
    genomes2 = stub.GetGenomesByAssemblyAccessionID(request2)
    print("**** Genomes from null assembly accession ****")
    print(list(genomes2))


def get_sub_species_info(stub):
    request1 = OrganismIDRequest(
        organism_uuid="86dd50f1-421e-4829-aca5-13ccc9a459f6",
        group="EnsemblPlants"
    )
    releases1 = stub.GetSubSpeciesInformation(request1)
    print("**** Sub species information ****")
    print(releases1)


def get_top_level_statistics(stub):
    request1 = OrganismIDRequest(
        organism_uuid="86dd50f1-421e-4829-aca5-13ccc9a459f6",
        group="EnsemblPlants"
    )
    releases1 = stub.GetTopLevelStatistics(request1)
    print("**** Top level statistics ****")
    print(releases1)


def get_top_level_statistics_by_uuid(stub):
    genome_request = GenomeUUIDRequest(
        genome_uuid="a7335667-93e7-11ec-a39d-005056b38ce3"
    )
    toplevel_stats_by_uuid_request = stub.GetTopLevelStatisticsByUUID(genome_request)
    print("**** Top level statistics by UUID ****")
    print(toplevel_stats_by_uuid_request)


def get_datasets_list_by_uuid(stub):
    request1 = DatasetsRequest(
        genome_uuid="9caa2cae-d1c8-4cfc-9ffd-2e13bc3e95b1"
    )
    request2 = DatasetsRequest(
        genome_uuid="9caa2cae-d1c8-4cfc-9ffd-2e13bc3e95b1", release_version=108.0
    )
    print("**** Release not specified ****")
    datasets1 = stub.GetDatasetsListByUUID(request1)
    print(datasets1)
    print("**** Release specified ****")
    datasets2 = stub.GetDatasetsListByUUID(request2)
    print(datasets2)


def get_dataset_infos_by_dataset_type(stub):
    request1 = GenomeDatatypeRequest(
        genome_uuid="9caa2cae-d1c8-4cfc-9ffd-2e13bc3e95b1", dataset_type="assembly"
    )
    datasets1 = stub.GetDatasetInformation(request1)
    print(datasets1.datasets)


def get_genome_uuid(stub):
    request1 = GenomeInfoRequest(
        production_name="homo_sapiens_37", assembly_name="GRCh37.p13"
    )
    genome_uuid1 = stub.GetGenomeUUID(request1)
    request2 = GenomeInfoRequest(
        production_name="homo_sapiens_37", assembly_name="GRCh37", use_default=True
    )
    genome_uuid2 = stub.GetGenomeUUID(request2)
    request3 = GenomeInfoRequest(
        production_name="homo_sapiens_37", assembly_name="GRCh37.p13", use_default=True
    )
    genome_uuid3 = stub.GetGenomeUUID(request3)

    print("**** Using assembly_name ****")
    print(genome_uuid1)
    print("**** Using assembly_default ****")
    print(genome_uuid2)
    print("**** Using assembly_default (No results) ****")
    print(genome_uuid3)


def get_organisms_group_count(stub):
    request = OrganismsGroupRequest()
    organisms_group_count = stub.GetOrganismsGroupCount(request)
    print(organisms_group_count)


def get_genome_uuid_by_tag(stub):
    request1 = GenomeTagRequest(genome_tag="grch37")
    genome_uuid1 = stub.GetGenomeUUIDByTag(request1)
    request2 = GenomeTagRequest(genome_tag="grch38")
    genome_uuid2 = stub.GetGenomeUUIDByTag(request2)
    request3 = GenomeTagRequest(genome_tag="r64-1-1")
    genome_uuid3 = stub.GetGenomeUUIDByTag(request3)
    request4 = GenomeTagRequest(genome_tag="foo")
    genome_uuid4 = stub.GetGenomeUUIDByTag(request4)

    print("**** Genome Tag: grch37 ****")
    print(genome_uuid1)
    print("**** Genome Tag: grch38 ****")
    print(genome_uuid2)
    print("**** Genome Tag: r64-1-1 ****")
    print(genome_uuid3)
    print("**** Genome Tag: foo ****")
    print(genome_uuid4)


def get_ftp_links(stub):

    # valid genome uuid and no dataset should return all the datasets links of that genome uuid
    request1 = FTPLinksRequest(genome_uuid="b997075a-292d-4e15-bfe5-23dca5a57b26", dataset_type="all")

    # valid genome uuid and a valid dataset should return corresponding dataset link
    request2 = FTPLinksRequest(genome_uuid="b997075a-292d-4e15-bfe5-23dca5a57b26", dataset_type="assembly")

    # invalid genome uuid should return no dataset links
    request3 = FTPLinksRequest(genome_uuid="b997075a-292d-4e15-bfe5-", dataset_type="all")

    # valid genome uuid and invalid dataset should return no dataset links
    request4 = FTPLinksRequest(genome_uuid="b997075a-292d-4e15-bfe5-23dca5a57b26", dataset_type="test")

    # no genome uuid should return no dataset links
    request5 = FTPLinksRequest(dataset_type="all")

    print("**** FTP Links - valid genome uuid and no dataset - return all the datasets links ****")
    print(stub.GetFTPLinks(request1))
    print("**** FTP Links - valid genome uuid and a valid dataset - return corresponding dataset link ****")
    print(stub.GetFTPLinks(request2))
    print("**** FTP Links - invalid genome uuid - returns no dataset links ****")
    print(stub.GetFTPLinks(request3))
    print("**** FTP Links - valid genome uuid and invalid dataset - return no dataset links ****")
    print(stub.GetFTPLinks(request4))
    print("**** FTP Links - no genome uuid - return no dataset links ****")
    print(stub.GetFTPLinks(request5))


def get_release_version_by_genome_uuid(stub):
    request1 = ReleaseVersionRequest(
        genome_uuid="a73351f7-93e7-11ec-a39d-005056b38ce3"
    )
    genome_uuid1 = stub.GetReleaseVersionByUUID(request1)
    request2 = ReleaseVersionRequest(
        genome_uuid="a73351f7-93e7-11ec-a39d-005056b38ce3",
        dataset_type="genebuild"
    )
    genome_uuid2 = stub.GetReleaseVersionByUUID(request2)
    request3 = ReleaseVersionRequest(
        genome_uuid="a73351f7-93e7-11ec-a39d-005056b38ce3",
        dataset_type="genebuild",
        release_version=110.1
    )
    genome_uuid3 = stub.GetReleaseVersionByUUID(request3)
    request4 = ReleaseVersionRequest(
        genome_uuid="a73351f7-93e7-11ec-a39d-005056b38ce3",
        dataset_type="genebuild",
        release_version=115
    )
    genome_uuid4 = stub.GetReleaseVersionByUUID(request4)
    request5 = ReleaseVersionRequest(
        dataset_type="genebuild",
        release_version=110.1
    )
    genome_uuid5 = stub.GetReleaseVersionByUUID(request5)

    print("**** Release Version: By genome_uuid ****")
    print(genome_uuid1)
    print("**** Release Version: By genome_uuid and dataset_type ****")
    print(genome_uuid2)
    print("**** Release Version: By genome_uuid, dataset_type and release ****")
    print(genome_uuid3)
    print("**** Release Version: With higher release version (e.g. 115) ****")
    print(genome_uuid4)
    print("**** Release Version: No genome_uuid provided (no results) ****")
    print(genome_uuid5)


def get_datasets_attributes_values_by_genome_uuid(stub):
    request1 = DatasetAttributesValuesRequest(
        genome_uuid="a73351f7-93e7-11ec-a39d-005056b38ce3"
    )
    attributes1 = stub.GetAttributesValuesByUUID(request1)
    print("**** Dataset Attributes Values: By genome_uuid only (default dataset_type is 'assembly') ****")
    print(attributes1)

    request2 = DatasetAttributesValuesRequest(
        genome_uuid="a73351f7-93e7-11ec-a39d-005056b38ce3",
        dataset_type="homologies"
    )
    attributes2 = stub.GetAttributesValuesByUUID(request2)
    print("**** Dataset Attributes Values: By genome_uuid and dataset_type='homologies' ****")
    print(attributes2)

    request3 = DatasetAttributesValuesRequest(
        genome_uuid="a73351f7-93e7-11ec-a39d-005056b38ce3",
        dataset_type="homologies",
        attribute_name=["compara.stats.homology_coverage"]
    )
    attributes3 = stub.GetAttributesValuesByUUID(request3)
    print("**** Dataset Attributes Values: By genome_uuid, dataset_type='homologies' and attribute_name=['compara.stats.homology_coverage'] ****")
    print(attributes3)

    request4 = DatasetAttributesValuesRequest(
        genome_uuid="a73351f7-93e7-11ec-a39d-005056b38ce3",
        dataset_type="homologies",
        release_version=110.1
    )
    attributes4 = stub.GetAttributesValuesByUUID(request4)
    print(
        "**** Dataset Attributes Values: By genome_uuid, dataset_type='homologies' and release_version=110.1 ****")
    print(attributes4)

    request5 = DatasetAttributesValuesRequest(
        genome_uuid="a73351f7-93e7-11ec-a39d-005056b38ce3",
        dataset_type="homologies",
        attribute_name=["i.dont.exist"]
    )
    attributes5 = stub.GetAttributesValuesByUUID(request5)
    print(
        "**** Dataset Attributes Values: By genome_uuid, dataset_type='homologies' and attribute_name=['i.dont.exist'] ****")
    print(attributes5)

    request6 = DatasetAttributesValuesRequest(
        genome_uuid="a73351f7-93e7-11ec-a39d-005056b38ce3",
        dataset_type="homologies",
        latest_only=0
    )
    attributes6 = stub.GetAttributesValuesByUUID(request6)
    print(
        "**** Dataset Attributes Values: By genome_uuid, dataset_type='homologies' and latest_only=0 ****")
    print(attributes6)

def get_attributes_by_genome_uuid(stub):
    request = GenomeUUIDRequest(
        genome_uuid="a7335667-93e7-11ec-a39d-005056b38ce3"
    )
    genome_attributes = stub.GetAttributesByGenomeUUID(request)

    print("**** Attributes: By genome_uuid ****")
    print(genome_attributes)


def get_brief_genome_details_by_uuid(stub):
    request1 = GenomeUUIDRequest(
        genome_uuid="a7335667-93e7-11ec-a39d-005056b38ce3"
    )
    brief_genome_details1 = stub.GetBriefGenomeDetailsByUUID(request1)
    print("**** Brief Genome Details: By genome_uuid ****")
    print(brief_genome_details1)

    request2 = GenomeUUIDRequest(
        genome_uuid="grch37"
    )
    brief_genome_details2 = stub.GetBriefGenomeDetailsByUUID(request2)
    print("**** Brief Genome Details: By Tag (grch37) ****")
    print(brief_genome_details2)


def get_vep_file_paths_by_uuid(stub):
    request1 = GenomeUUIDRequest(
        genome_uuid="a7335667-93e7-11ec-a39d-005056b38ce3"
    )
    vep_paths1 = stub.GetVepFilePathsByUUID(request1)
    print("**** VEP Paths By genome_uuid ****")
    print(vep_paths1)

    request2 = GenomeUUIDRequest(
        genome_uuid="i-dont-exist-as-uuid"
    )
    vep_paths2 = stub.GetVepFilePathsByUUID(request2)
    print("**** VEP Paths By genome_uuid (non existing UUID) ****")
    print(vep_paths2)


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ensembl_metadata_pb2_grpc.EnsemblMetadataStub(channel)
        print("---------------Get Species Information-----------")
        get_species_information_by_uuid(stub)
        print("---------------Get Assembly Information-----------")
        get_assembly_information(stub)
        print(
            "---------------Get Genome Information from assembly accession-----------"
        )
        get_genomes_by_assembly_accession(stub)
        print("---------------Get Subspecies Information-----------")
        get_sub_species_info(stub)
        print("---------------Get Top Level Statistics-----------")
        get_top_level_statistics(stub)
        print("---------------Get Top Level Statistics By UUID-----------")
        get_top_level_statistics_by_uuid(stub)
        print("-------------- Get Genomes --------------")
        get_genomes(stub)
        print("-------------- Get Genome By Keyword --------------")
        get_genome_by_keyword(stub)
        print("-------------- Get Genome By release_version --------------")
        get_genomes_by_release_version(stub)
        print("-------------- List Genome Sequences --------------")
        list_genome_sequences(stub)
        print("-------------- List Genome Assembly Sequences --------------")
        list_genome_assembly_sequences(stub)
        print("-------------- List Region Info for Given Sequence Name --------------")
        list_genome_assembly_sequences_region(stub)
        print("-------------- List Releases --------------")
        list_releases(stub)
        print("-------------- List Releases for Genome --------------")
        list_releases_by_uuid(stub)
        print("---------------Get Datasets List-----------")
        get_datasets_list_by_uuid(stub)
        print("-------------- List Dataset information for Genome --------------")
        get_dataset_infos_by_dataset_type(stub)
        print("-------------- Get Genome UUID --------------")
        get_genome_uuid(stub)
        print("-------------- Get Organisms Group Count --------------")
        get_organisms_group_count(stub)
        print("-------------- Get Genome UUID By Tag --------------")
        get_genome_uuid_by_tag(stub)
        print("-------------- Get FTP Links by Genome UUID and dataset --------------")
        get_ftp_links(stub)
        print("-------------- Get Release Version By Genome UUID --------------")
        get_release_version_by_genome_uuid(stub)
        print("-------------- Get Attributes By Genome UUID --------------")
        get_attributes_by_genome_uuid(stub)
        print("-------------- Get Brief Genome Details By UUID --------------")
        get_brief_genome_details_by_uuid(stub)
        print("-------------- Get VEP File Paths By UUID --------------")
        get_vep_file_paths_by_uuid(stub)


if __name__ == "__main__":
    logging.basicConfig()
    run()

# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from ensembl.production.metadata.grpc import ensembl_metadata_pb2 as ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2


class EnsemblMetadataStub(object):
    """IMPORTANT: the directory structure of the protos directory should mirror the structure of the src directory to avoid
    Python import errors.

    Metadata for the genomes in Ensembl.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetGenomeByUUID = channel.unary_unary(
                '/ensembl_metadata.EnsemblMetadata/GetGenomeByUUID',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUIDRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Genome.FromString,
                )
        self.GetGenomeUUID = channel.unary_unary(
                '/ensembl_metadata.EnsemblMetadata/GetGenomeUUID',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeInfoRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUID.FromString,
                )
        self.GetGenomesByKeyword = channel.unary_stream(
                '/ensembl_metadata.EnsemblMetadata/GetGenomesByKeyword',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeByKeywordRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Genome.FromString,
                )
        self.GetGenomesByAssemblyAccessionID = channel.unary_stream(
                '/ensembl_metadata.EnsemblMetadata/GetGenomesByAssemblyAccessionID',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.AssemblyAccessionIDRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Genome.FromString,
                )
        self.GetSpeciesInformation = channel.unary_unary(
                '/ensembl_metadata.EnsemblMetadata/GetSpeciesInformation',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUIDRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Species.FromString,
                )
        self.GetAssemblyInformation = channel.unary_unary(
                '/ensembl_metadata.EnsemblMetadata/GetAssemblyInformation',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.AssemblyIDRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.AssemblyInfo.FromString,
                )
        self.GetSubSpeciesInformation = channel.unary_unary(
                '/ensembl_metadata.EnsemblMetadata/GetSubSpeciesInformation',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.OrganismIDRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.SubSpecies.FromString,
                )
        self.GetKaryotypeInformation = channel.unary_unary(
                '/ensembl_metadata.EnsemblMetadata/GetKaryotypeInformation',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUIDRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Karyotype.FromString,
                )
        self.GetTopLevelStatistics = channel.unary_unary(
                '/ensembl_metadata.EnsemblMetadata/GetTopLevelStatistics',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.OrganismIDRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.TopLevelStatistics.FromString,
                )
        self.GetTopLevelStatisticsByUUID = channel.unary_unary(
                '/ensembl_metadata.EnsemblMetadata/GetTopLevelStatisticsByUUID',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUIDRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.TopLevelStatisticsByUUID.FromString,
                )
        self.GetGenomeByName = channel.unary_unary(
                '/ensembl_metadata.EnsemblMetadata/GetGenomeByName',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeNameRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Genome.FromString,
                )
        self.GetRelease = channel.unary_stream(
                '/ensembl_metadata.EnsemblMetadata/GetRelease',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.ReleaseRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Release.FromString,
                )
        self.GetReleaseByUUID = channel.unary_stream(
                '/ensembl_metadata.EnsemblMetadata/GetReleaseByUUID',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUIDRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Release.FromString,
                )
        self.GetGenomeSequence = channel.unary_stream(
                '/ensembl_metadata.EnsemblMetadata/GetGenomeSequence',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeSequenceRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeSequence.FromString,
                )
        self.GetGenomeAssemblySequence = channel.unary_stream(
                '/ensembl_metadata.EnsemblMetadata/GetGenomeAssemblySequence',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeAssemblySequenceRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeAssemblySequence.FromString,
                )
        self.GetGenomeAssemblySequenceRegion = channel.unary_unary(
                '/ensembl_metadata.EnsemblMetadata/GetGenomeAssemblySequenceRegion',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeAssemblySequenceRegionRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeAssemblySequenceRegion.FromString,
                )
        self.GetDatasetsListByUUID = channel.unary_unary(
                '/ensembl_metadata.EnsemblMetadata/GetDatasetsListByUUID',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.DatasetsRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Datasets.FromString,
                )
        self.GetDatasetInformation = channel.unary_unary(
                '/ensembl_metadata.EnsemblMetadata/GetDatasetInformation',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeDatatypeRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.DatasetInfos.FromString,
                )
        self.GetOrganismsGroupCount = channel.unary_unary(
                '/ensembl_metadata.EnsemblMetadata/GetOrganismsGroupCount',
                request_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.OrganismsGroupRequest.SerializeToString,
                response_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.OrganismsGroupCount.FromString,
                )


class EnsemblMetadataServicer(object):
    """IMPORTANT: the directory structure of the protos directory should mirror the structure of the src directory to avoid
    Python import errors.

    Metadata for the genomes in Ensembl.
    """

    def GetGenomeByUUID(self, request, context):
        """Retrieve genome by its UUID.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetGenomeUUID(self, request, context):
        """Retrieve genome UUID by providing production name and assembly id.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetGenomesByKeyword(self, request, context):
        """Retrieve genomes by keyword search
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetGenomesByAssemblyAccessionID(self, request, context):
        """Retrieve all genomes for a give assembly accession ID
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSpeciesInformation(self, request, context):
        """Get species information for a genome UUID
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAssemblyInformation(self, request, context):
        """Get assembly information
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSubSpeciesInformation(self, request, context):
        """Get subspecies information
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetKaryotypeInformation(self, request, context):
        """Get karyotype information
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTopLevelStatistics(self, request, context):
        """Get top level statistics
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTopLevelStatisticsByUUID(self, request, context):
        """Get top level statistics by UUID
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetGenomeByName(self, request, context):
        """Retrieve genome by Ensembl name and site, and optionally release.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRelease(self, request, context):
        """Retrieve release details.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetReleaseByUUID(self, request, context):
        """Retrieve release details for a genome.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetGenomeSequence(self, request, context):
        """Retrieve sequence metadata for a genome's assembly.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetGenomeAssemblySequence(self, request, context):
        """Retrieve region information for a genome's assembly.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetGenomeAssemblySequenceRegion(self, request, context):
        """Retrieve region information for a genome's assembly with a given sequence region name.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDatasetsListByUUID(self, request, context):
        """Retrieve a list of dataset_ids associated with a genome UUID.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDatasetInformation(self, request, context):
        """Retrieve dataset info by genome uuid and dataset_type
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOrganismsGroupCount(self, request, context):
        """Retrieve organisms group count
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EnsemblMetadataServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetGenomeByUUID': grpc.unary_unary_rpc_method_handler(
                    servicer.GetGenomeByUUID,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUIDRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Genome.SerializeToString,
            ),
            'GetGenomeUUID': grpc.unary_unary_rpc_method_handler(
                    servicer.GetGenomeUUID,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeInfoRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUID.SerializeToString,
            ),
            'GetGenomesByKeyword': grpc.unary_stream_rpc_method_handler(
                    servicer.GetGenomesByKeyword,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeByKeywordRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Genome.SerializeToString,
            ),
            'GetGenomesByAssemblyAccessionID': grpc.unary_stream_rpc_method_handler(
                    servicer.GetGenomesByAssemblyAccessionID,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.AssemblyAccessionIDRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Genome.SerializeToString,
            ),
            'GetSpeciesInformation': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSpeciesInformation,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUIDRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Species.SerializeToString,
            ),
            'GetAssemblyInformation': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAssemblyInformation,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.AssemblyIDRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.AssemblyInfo.SerializeToString,
            ),
            'GetSubSpeciesInformation': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSubSpeciesInformation,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.OrganismIDRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.SubSpecies.SerializeToString,
            ),
            'GetKaryotypeInformation': grpc.unary_unary_rpc_method_handler(
                    servicer.GetKaryotypeInformation,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUIDRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Karyotype.SerializeToString,
            ),
            'GetTopLevelStatistics': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTopLevelStatistics,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.OrganismIDRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.TopLevelStatistics.SerializeToString,
            ),
            'GetTopLevelStatisticsByUUID': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTopLevelStatisticsByUUID,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUIDRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.TopLevelStatisticsByUUID.SerializeToString,
            ),
            'GetGenomeByName': grpc.unary_unary_rpc_method_handler(
                    servicer.GetGenomeByName,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeNameRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Genome.SerializeToString,
            ),
            'GetRelease': grpc.unary_stream_rpc_method_handler(
                    servicer.GetRelease,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.ReleaseRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Release.SerializeToString,
            ),
            'GetReleaseByUUID': grpc.unary_stream_rpc_method_handler(
                    servicer.GetReleaseByUUID,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUIDRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Release.SerializeToString,
            ),
            'GetGenomeSequence': grpc.unary_stream_rpc_method_handler(
                    servicer.GetGenomeSequence,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeSequenceRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeSequence.SerializeToString,
            ),
            'GetGenomeAssemblySequence': grpc.unary_stream_rpc_method_handler(
                    servicer.GetGenomeAssemblySequence,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeAssemblySequenceRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeAssemblySequence.SerializeToString,
            ),
            'GetGenomeAssemblySequenceRegion': grpc.unary_unary_rpc_method_handler(
                    servicer.GetGenomeAssemblySequenceRegion,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeAssemblySequenceRegionRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeAssemblySequenceRegion.SerializeToString,
            ),
            'GetDatasetsListByUUID': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDatasetsListByUUID,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.DatasetsRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Datasets.SerializeToString,
            ),
            'GetDatasetInformation': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDatasetInformation,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeDatatypeRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.DatasetInfos.SerializeToString,
            ),
            'GetOrganismsGroupCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOrganismsGroupCount,
                    request_deserializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.OrganismsGroupRequest.FromString,
                    response_serializer=ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.OrganismsGroupCount.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ensembl_metadata.EnsemblMetadata', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class EnsemblMetadata(object):
    """IMPORTANT: the directory structure of the protos directory should mirror the structure of the src directory to avoid
    Python import errors.

    Metadata for the genomes in Ensembl.
    """

    @staticmethod
    def GetGenomeByUUID(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ensembl_metadata.EnsemblMetadata/GetGenomeByUUID',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUIDRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Genome.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetGenomeUUID(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ensembl_metadata.EnsemblMetadata/GetGenomeUUID',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeInfoRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUID.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetGenomesByKeyword(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/ensembl_metadata.EnsemblMetadata/GetGenomesByKeyword',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeByKeywordRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Genome.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetGenomesByAssemblyAccessionID(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/ensembl_metadata.EnsemblMetadata/GetGenomesByAssemblyAccessionID',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.AssemblyAccessionIDRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Genome.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSpeciesInformation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ensembl_metadata.EnsemblMetadata/GetSpeciesInformation',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUIDRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Species.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAssemblyInformation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ensembl_metadata.EnsemblMetadata/GetAssemblyInformation',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.AssemblyIDRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.AssemblyInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSubSpeciesInformation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ensembl_metadata.EnsemblMetadata/GetSubSpeciesInformation',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.OrganismIDRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.SubSpecies.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetKaryotypeInformation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ensembl_metadata.EnsemblMetadata/GetKaryotypeInformation',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUIDRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Karyotype.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTopLevelStatistics(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ensembl_metadata.EnsemblMetadata/GetTopLevelStatistics',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.OrganismIDRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.TopLevelStatistics.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTopLevelStatisticsByUUID(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ensembl_metadata.EnsemblMetadata/GetTopLevelStatisticsByUUID',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUIDRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.TopLevelStatisticsByUUID.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetGenomeByName(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ensembl_metadata.EnsemblMetadata/GetGenomeByName',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeNameRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Genome.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetRelease(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/ensembl_metadata.EnsemblMetadata/GetRelease',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.ReleaseRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Release.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetReleaseByUUID(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/ensembl_metadata.EnsemblMetadata/GetReleaseByUUID',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeUUIDRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Release.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetGenomeSequence(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/ensembl_metadata.EnsemblMetadata/GetGenomeSequence',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeSequenceRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeSequence.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetGenomeAssemblySequence(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/ensembl_metadata.EnsemblMetadata/GetGenomeAssemblySequence',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeAssemblySequenceRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeAssemblySequence.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetGenomeAssemblySequenceRegion(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ensembl_metadata.EnsemblMetadata/GetGenomeAssemblySequenceRegion',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeAssemblySequenceRegionRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeAssemblySequenceRegion.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDatasetsListByUUID(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ensembl_metadata.EnsemblMetadata/GetDatasetsListByUUID',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.DatasetsRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.Datasets.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDatasetInformation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ensembl_metadata.EnsemblMetadata/GetDatasetInformation',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.GenomeDatatypeRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.DatasetInfos.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetOrganismsGroupCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ensembl_metadata.EnsemblMetadata/GetOrganismsGroupCount',
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.OrganismsGroupRequest.SerializeToString,
            ensembl_dot_production_dot_metadata_dot_grpc_dot_ensembl__metadata__pb2.OrganismsGroupCount.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import AnalogInChannelProvider_pb2 as AnalogInChannelProvider__pb2


class AnalogInChannelProviderStub(object):
    """Feature: Analog In Channel Provider
    Allows to control one analog input channel of an I/O module
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get_NumberOfChannels = channel.unary_unary(
                '/sila2.de.cetoni.io.analoginchannelprovider.v1.AnalogInChannelProvider/Get_NumberOfChannels',
                request_serializer=AnalogInChannelProvider__pb2.Get_NumberOfChannels_Parameters.SerializeToString,
                response_deserializer=AnalogInChannelProvider__pb2.Get_NumberOfChannels_Responses.FromString,
                )
        self.Subscribe_Value = channel.unary_stream(
                '/sila2.de.cetoni.io.analoginchannelprovider.v1.AnalogInChannelProvider/Subscribe_Value',
                request_serializer=AnalogInChannelProvider__pb2.Subscribe_Value_Parameters.SerializeToString,
                response_deserializer=AnalogInChannelProvider__pb2.Subscribe_Value_Responses.FromString,
                )
        self.Get_FCPAffectedByMetadata_ChannelIndex = channel.unary_unary(
                '/sila2.de.cetoni.io.analoginchannelprovider.v1.AnalogInChannelProvider/Get_FCPAffectedByMetadata_ChannelIndex',
                request_serializer=AnalogInChannelProvider__pb2.Get_FCPAffectedByMetadata_ChannelIndex_Parameters.SerializeToString,
                response_deserializer=AnalogInChannelProvider__pb2.Get_FCPAffectedByMetadata_ChannelIndex_Responses.FromString,
                )


class AnalogInChannelProviderServicer(object):
    """Feature: Analog In Channel Provider
    Allows to control one analog input channel of an I/O module
    """

    def Get_NumberOfChannels(self, request, context):
        """Number Of Channels
        The number of analog input channels. This value is 0-indexed, i.e. the first channel has index 0, the second one index 1
        and so on.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Subscribe_Value(self, request, context):
        """Value
        The value of the analog input channel.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get_FCPAffectedByMetadata_ChannelIndex(self, request, context):
        """Channel Index
        The index of the channel that should be used.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AnalogInChannelProviderServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get_NumberOfChannels': grpc.unary_unary_rpc_method_handler(
                    servicer.Get_NumberOfChannels,
                    request_deserializer=AnalogInChannelProvider__pb2.Get_NumberOfChannels_Parameters.FromString,
                    response_serializer=AnalogInChannelProvider__pb2.Get_NumberOfChannels_Responses.SerializeToString,
            ),
            'Subscribe_Value': grpc.unary_stream_rpc_method_handler(
                    servicer.Subscribe_Value,
                    request_deserializer=AnalogInChannelProvider__pb2.Subscribe_Value_Parameters.FromString,
                    response_serializer=AnalogInChannelProvider__pb2.Subscribe_Value_Responses.SerializeToString,
            ),
            'Get_FCPAffectedByMetadata_ChannelIndex': grpc.unary_unary_rpc_method_handler(
                    servicer.Get_FCPAffectedByMetadata_ChannelIndex,
                    request_deserializer=AnalogInChannelProvider__pb2.Get_FCPAffectedByMetadata_ChannelIndex_Parameters.FromString,
                    response_serializer=AnalogInChannelProvider__pb2.Get_FCPAffectedByMetadata_ChannelIndex_Responses.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sila2.de.cetoni.io.analoginchannelprovider.v1.AnalogInChannelProvider', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AnalogInChannelProvider(object):
    """Feature: Analog In Channel Provider
    Allows to control one analog input channel of an I/O module
    """

    @staticmethod
    def Get_NumberOfChannels(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sila2.de.cetoni.io.analoginchannelprovider.v1.AnalogInChannelProvider/Get_NumberOfChannels',
            AnalogInChannelProvider__pb2.Get_NumberOfChannels_Parameters.SerializeToString,
            AnalogInChannelProvider__pb2.Get_NumberOfChannels_Responses.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Subscribe_Value(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/sila2.de.cetoni.io.analoginchannelprovider.v1.AnalogInChannelProvider/Subscribe_Value',
            AnalogInChannelProvider__pb2.Subscribe_Value_Parameters.SerializeToString,
            AnalogInChannelProvider__pb2.Subscribe_Value_Responses.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Get_FCPAffectedByMetadata_ChannelIndex(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sila2.de.cetoni.io.analoginchannelprovider.v1.AnalogInChannelProvider/Get_FCPAffectedByMetadata_ChannelIndex',
            AnalogInChannelProvider__pb2.Get_FCPAffectedByMetadata_ChannelIndex_Parameters.SerializeToString,
            AnalogInChannelProvider__pb2.Get_FCPAffectedByMetadata_ChannelIndex_Responses.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
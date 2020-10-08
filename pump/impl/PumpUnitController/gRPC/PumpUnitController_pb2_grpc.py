# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import PumpUnitController_pb2 as PumpUnitController__pb2


class PumpUnitControllerStub(object):
  """Feature: Pump Unit Controller
  Allows to control the currently used units for passing and retrieving flow rates and volumes to and from a pump.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SetFlowUnit = channel.unary_unary(
        '/sila2.de.cetoni.pumps.syringepumps.pumpunitcontroller.v1.PumpUnitController/SetFlowUnit',
        request_serializer=PumpUnitController__pb2.SetFlowUnit_Parameters.SerializeToString,
        response_deserializer=PumpUnitController__pb2.SetFlowUnit_Responses.FromString,
        )
    self.SetVolumeUnit = channel.unary_unary(
        '/sila2.de.cetoni.pumps.syringepumps.pumpunitcontroller.v1.PumpUnitController/SetVolumeUnit',
        request_serializer=PumpUnitController__pb2.SetVolumeUnit_Parameters.SerializeToString,
        response_deserializer=PumpUnitController__pb2.SetVolumeUnit_Responses.FromString,
        )
    self.Subscribe_FlowUnit = channel.unary_stream(
        '/sila2.de.cetoni.pumps.syringepumps.pumpunitcontroller.v1.PumpUnitController/Subscribe_FlowUnit',
        request_serializer=PumpUnitController__pb2.Subscribe_FlowUnit_Parameters.SerializeToString,
        response_deserializer=PumpUnitController__pb2.Subscribe_FlowUnit_Responses.FromString,
        )
    self.Subscribe_VolumeUnit = channel.unary_stream(
        '/sila2.de.cetoni.pumps.syringepumps.pumpunitcontroller.v1.PumpUnitController/Subscribe_VolumeUnit',
        request_serializer=PumpUnitController__pb2.Subscribe_VolumeUnit_Parameters.SerializeToString,
        response_deserializer=PumpUnitController__pb2.Subscribe_VolumeUnit_Responses.FromString,
        )


class PumpUnitControllerServicer(object):
  """Feature: Pump Unit Controller
  Allows to control the currently used units for passing and retrieving flow rates and volumes to and from a pump.
  """

  def SetFlowUnit(self, request, context):
    """Set Flow Unit
    Sets the flow unit for the pump. The flow unit defines the unit to be used for all flow values passed to or retrieved
    from the pump.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetVolumeUnit(self, request, context):
    """Set Volume Unit
    Sets the default volume unit. The volume unit defines the unit to be used for all volume values passed to or retrieved
    from the pump.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Subscribe_FlowUnit(self, request, context):
    """Flow Unit
    The currently used flow unit.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Subscribe_VolumeUnit(self, request, context):
    """Volume Unit
    The currently used volume unit.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_PumpUnitControllerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SetFlowUnit': grpc.unary_unary_rpc_method_handler(
          servicer.SetFlowUnit,
          request_deserializer=PumpUnitController__pb2.SetFlowUnit_Parameters.FromString,
          response_serializer=PumpUnitController__pb2.SetFlowUnit_Responses.SerializeToString,
      ),
      'SetVolumeUnit': grpc.unary_unary_rpc_method_handler(
          servicer.SetVolumeUnit,
          request_deserializer=PumpUnitController__pb2.SetVolumeUnit_Parameters.FromString,
          response_serializer=PumpUnitController__pb2.SetVolumeUnit_Responses.SerializeToString,
      ),
      'Subscribe_FlowUnit': grpc.unary_stream_rpc_method_handler(
          servicer.Subscribe_FlowUnit,
          request_deserializer=PumpUnitController__pb2.Subscribe_FlowUnit_Parameters.FromString,
          response_serializer=PumpUnitController__pb2.Subscribe_FlowUnit_Responses.SerializeToString,
      ),
      'Subscribe_VolumeUnit': grpc.unary_stream_rpc_method_handler(
          servicer.Subscribe_VolumeUnit,
          request_deserializer=PumpUnitController__pb2.Subscribe_VolumeUnit_Parameters.FromString,
          response_serializer=PumpUnitController__pb2.Subscribe_VolumeUnit_Responses.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'sila2.de.cetoni.pumps.syringepumps.pumpunitcontroller.v1.PumpUnitController', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))

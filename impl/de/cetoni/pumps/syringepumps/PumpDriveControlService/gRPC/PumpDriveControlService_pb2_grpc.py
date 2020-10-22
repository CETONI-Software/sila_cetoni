# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import PumpDriveControlService_pb2 as PumpDriveControlService__pb2


class PumpDriveControlServiceStub(object):
  """Feature: Pump Drive Control Service

  Functionality to control and maintain the drive that drives the pump.
  Allows to initialize a pump (e.g. by executing a reference move) and obtain status information about the pump
  drive's current state (i.e. enabled/disabled).
  The initialization has to be successful in order for the pump to work correctly and dose fluids. If the
  initialization fails, the DefinedExecutionError InitializationFailed is thrown.

  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.InitializePumpDrive = channel.unary_unary(
        '/sila2.de.cetoni.pumps.syringepumps.pumpdrivecontrolservice.v1.PumpDriveControlService/InitializePumpDrive',
        request_serializer=PumpDriveControlService__pb2.InitializePumpDrive_Parameters.SerializeToString,
        response_deserializer=PumpDriveControlService__pb2.InitializePumpDrive_Responses.FromString,
        )
    self.EnablePumpDrive = channel.unary_unary(
        '/sila2.de.cetoni.pumps.syringepumps.pumpdrivecontrolservice.v1.PumpDriveControlService/EnablePumpDrive',
        request_serializer=PumpDriveControlService__pb2.EnablePumpDrive_Parameters.SerializeToString,
        response_deserializer=PumpDriveControlService__pb2.EnablePumpDrive_Responses.FromString,
        )
    self.DisablePumpDrive = channel.unary_unary(
        '/sila2.de.cetoni.pumps.syringepumps.pumpdrivecontrolservice.v1.PumpDriveControlService/DisablePumpDrive',
        request_serializer=PumpDriveControlService__pb2.DisablePumpDrive_Parameters.SerializeToString,
        response_deserializer=PumpDriveControlService__pb2.DisablePumpDrive_Responses.FromString,
        )
    self.Subscribe_PumpDriveState = channel.unary_stream(
        '/sila2.de.cetoni.pumps.syringepumps.pumpdrivecontrolservice.v1.PumpDriveControlService/Subscribe_PumpDriveState',
        request_serializer=PumpDriveControlService__pb2.Subscribe_PumpDriveState_Parameters.SerializeToString,
        response_deserializer=PumpDriveControlService__pb2.Subscribe_PumpDriveState_Responses.FromString,
        )
    self.Subscribe_FaultState = channel.unary_stream(
        '/sila2.de.cetoni.pumps.syringepumps.pumpdrivecontrolservice.v1.PumpDriveControlService/Subscribe_FaultState',
        request_serializer=PumpDriveControlService__pb2.Subscribe_FaultState_Parameters.SerializeToString,
        response_deserializer=PumpDriveControlService__pb2.Subscribe_FaultState_Responses.FromString,
        )


class PumpDriveControlServiceServicer(object):
  """Feature: Pump Drive Control Service

  Functionality to control and maintain the drive that drives the pump.
  Allows to initialize a pump (e.g. by executing a reference move) and obtain status information about the pump
  drive's current state (i.e. enabled/disabled).
  The initialization has to be successful in order for the pump to work correctly and dose fluids. If the
  initialization fails, the DefinedExecutionError InitializationFailed is thrown.

  """

  def InitializePumpDrive(self, request, context):
    """Initialize Pump Drive
    Initialize the pump drive (e.g. by executing a reference move).
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def EnablePumpDrive(self, request, context):
    """Enable Pump Drive
    Set the pump into enabled state.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DisablePumpDrive(self, request, context):
    """Disable Pump Drive
    Set the pump into disabled state.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Subscribe_PumpDriveState(self, request, context):
    """Pump Drive State
    The current state of the pump. This is either enabled (true) or disabled (false). Only if the sate is enabled, the pump
    can dose fluids.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Subscribe_FaultState(self, request, context):
    """Fault State
    Returns if the pump is in fault state. If the value is true (i.e. the pump is in fault state), it can be cleared by
    calling EnablePumpDrive.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_PumpDriveControlServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'InitializePumpDrive': grpc.unary_unary_rpc_method_handler(
          servicer.InitializePumpDrive,
          request_deserializer=PumpDriveControlService__pb2.InitializePumpDrive_Parameters.FromString,
          response_serializer=PumpDriveControlService__pb2.InitializePumpDrive_Responses.SerializeToString,
      ),
      'EnablePumpDrive': grpc.unary_unary_rpc_method_handler(
          servicer.EnablePumpDrive,
          request_deserializer=PumpDriveControlService__pb2.EnablePumpDrive_Parameters.FromString,
          response_serializer=PumpDriveControlService__pb2.EnablePumpDrive_Responses.SerializeToString,
      ),
      'DisablePumpDrive': grpc.unary_unary_rpc_method_handler(
          servicer.DisablePumpDrive,
          request_deserializer=PumpDriveControlService__pb2.DisablePumpDrive_Parameters.FromString,
          response_serializer=PumpDriveControlService__pb2.DisablePumpDrive_Responses.SerializeToString,
      ),
      'Subscribe_PumpDriveState': grpc.unary_stream_rpc_method_handler(
          servicer.Subscribe_PumpDriveState,
          request_deserializer=PumpDriveControlService__pb2.Subscribe_PumpDriveState_Parameters.FromString,
          response_serializer=PumpDriveControlService__pb2.Subscribe_PumpDriveState_Responses.SerializeToString,
      ),
      'Subscribe_FaultState': grpc.unary_stream_rpc_method_handler(
          servicer.Subscribe_FaultState,
          request_deserializer=PumpDriveControlService__pb2.Subscribe_FaultState_Parameters.FromString,
          response_serializer=PumpDriveControlService__pb2.Subscribe_FaultState_Responses.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'sila2.de.cetoni.pumps.syringepumps.pumpdrivecontrolservice.v1.PumpDriveControlService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
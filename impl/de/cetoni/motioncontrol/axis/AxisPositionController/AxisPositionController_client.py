#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: sila_cetoni

*MotionControl client*

:details: MotionControl:
    Allows to control motion systems like axis systems

:file:    AxisPositionController_client.py
:authors: Florian Meinicke

:date: (creation)          2021-07-09T10:33:26.281915
:date: (last modification) 2021-07-09T10:33:26.281915

.. note:: Code generated by sila2codegenerator 0.3.6

_______________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
__version__ = "0.1.0"

# import general packages
import logging
import argparse
import grpc
import time
import datetime

# import meta packages
from typing import Union, Optional

# import SiLA2 library modules
from sila2lib.framework import SiLAFramework_pb2 as silaFW_pb2
from sila2lib.sila_client import SiLA2Client
from sila2lib.framework.std_features import SiLAService_pb2 as SiLAService_feature_pb2
from sila2lib.error_handling import client_err
from sila2lib.error_handling.client_err import SiLAClientError
import sila2lib.utils.py2sila_types as p2s
#   Usually not needed, but - feel free to modify
# from sila2lib.framework.std_features import SimulationController_pb2 as SimController_feature_pb2

# import feature gRPC modules
# Import gRPC libraries of features
from .gRPC import AxisPositionController_pb2
from .gRPC import AxisPositionController_pb2_grpc
# import default arguments for this feature
from .AxisPositionController_default_arguments import default_dict as AxisPositionController_default_dict

from . import METADATA_AXIS_IDENTIFIER


# noinspection PyPep8Naming, PyUnusedLocal
class AxisPositionControllerClient:
    """
        Allows to control motion systems like axis systems

    .. note:: For an example on how to construct the parameter or read the response(s) for command calls and properties,
              compare the default dictionary that is stored in the directory of the corresponding feature.
    """
    # The following variables will be filled when run() is executed
    #: Storage for the connected servers version
    server_version: str = ''
    #: Storage for the display name of the connected server
    server_display_name: str = ''
    #: Storage for the description of the connected server
    server_description: str = ''

    def __init__(self,
                 channel = None):
        """Class initialiser"""

        # Create stub objects used to communicate with the server
        self.AxisPositionController_stub = \
            AxisPositionController_pb2_grpc.AxisPositionControllerStub(channel)


        # initialise class variables for server information storage
        self.server_version = ''
        self.server_display_name = ''
        self.server_description = ''

    def _serialize_axis_id(self, axis_id: int) -> bytes:
        """
        Converts the given Axis Identifier from its string representation into
        a serialized protobuf message
        """
        return AxisPositionController_pb2.Metadata_AxisIdentifier(
            AxisIdentifier=silaFW_pb2.String(value=axis_id)).SerializeToString()

    def MoveToPosition(self, axis_id: str, Position: float, Velocity: float) \
            -> silaFW_pb2.CommandConfirmation:
        """
        Wrapper to call the observable command MoveToPosition on the server.

        :param axis_id: The index of the axis to use. Will be sent along as metadata
                        of the call
        :param Position: The position to move to. Has to be in the range between
                         MinimumPosition and MaximumPosition
        :param Velocity: The velocity value for the movement

        :returns: A command confirmation object with the following information:
            commandExecutionUUID: A command id with which this observable command can be referenced in future calls
            lifetimeOfExecution (optional): The (maximum) lifetime of this command call.
        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug(f"Calling MoveToPosition for axis {axis_id}:")
        try:
            parameter = AxisPositionController_pb2.MoveToPosition_Parameters(
                Position=silaFW_pb2.Real(value=Position),
                Velocity=AxisPositionController_pb2.DataType_Velocity(
                    Velocity=silaFW_pb2.Real(value=Velocity))
            )
            metadata = ((METADATA_AXIS_IDENTIFIER, self._serialize_axis_id(axis_id)),)

            response = self.AxisPositionController_stub.MoveToPosition(parameter, metadata=metadata)

            logging.debug('MoveToPosition response: {response}'.format(response=response))
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response

    def MoveToPosition_Info(self, axis_id: str,
                            uuid: Union[str, silaFW_pb2.CommandExecutionUUID]) \
            -> silaFW_pb2.ExecutionInfo:
        """
        Wrapper to get an intermediate response for the observable command MoveToPosition on the server.

        :param axis_id: The index of the axis to use. Will be sent along as metadata
                        of the call
        :param uuid: The UUID that has been returned with the first command call. Can be given as string or as the
                     corresponding SiLA2 gRPC object.

        :returns: A gRPC object with the status information that has been defined for this command. The following fields
                  are defined:
                    * *commandStatus*: Status of the command (enumeration)
                    * *progressInfo*: Information on the progress of the command (0 to 1)
                    * *estimatedRemainingTime*: Estimate of the remaining time required to run the command
                    * *updatedLifetimeOfExecution*: An update on the execution lifetime
        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        if type(uuid) is str:
            uuid = silaFW_pb2.CommandExecutionUUID(value=uuid)

        logging.debug("Requesting status information for command MoveToPosition for axis {axis_id} (UUID={uuid}):".format(
                uuid=uuid.value
            )
        )
        try:
            metadata = ((METADATA_AXIS_IDENTIFIER, self._serialize_axis_id(axis_id)),)
            response = self.AxisPositionController_stub.MoveToPosition_Info(uuid, metadata=metadata)
            logging.debug('MoveToPosition status information: {response}'.format(response=response))
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response

    def MoveToPosition_Result(self, axis_id: str,
                              uuid: Union[str, silaFW_pb2.CommandExecutionUUID]) \
            -> AxisPositionController_pb2.MoveToPosition_Responses:
        """
        Wrapper to get an intermediate response for the observable command MoveToPosition on the server.

        :param axis_id: The index of the axis to use. Will be sent along as metadata
                        of the call
        :param uuid: The UUID that has been returned with the first command call. Can be given as string or as the
                     corresponding SiLA2 gRPC object.

        :returns: A gRPC object with the result response that has been defined for this command.

        .. note:: Whether the result is available or not can and should be evaluated by calling the
                  :meth:`MoveToPosition_Info` method of this call.
        """
        if type(uuid) is str:
            uuid = silaFW_pb2.CommandExecutionUUID(value=uuid)

        logging.debug("Requesting status information for command MoveToPosition for axis {axis_id} (UUID={uuid}):".format(
                axis_id=axis_id,
                uuid=uuid.value
            )
        )

        try:
            metadata = ((METADATA_AXIS_IDENTIFIER, self._serialize_axis_id(axis_id)),)
            response = self.AxisPositionController_stub.MoveToPosition_Result(uuid, metadata=metadata)
            logging.debug('MoveToPosition result response: {response}'.format(response=response))
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response

    def MoveToHomePosition(self, axis_id: str): # -> (AxisPositionController):
        """
        Wrapper to call the unobservable command MoveToHomePosition on the server.

        :param axis_id: The index of the axis to use. Will be sent along as metadata
                        of the call
        :returns: A gRPC object with the response that has been defined for this command.
        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug(f"Calling MoveToHomePosition for axis {axis_id}:")
        try:
            metadata = ((METADATA_AXIS_IDENTIFIER, self._serialize_axis_id(axis_id)),)

            response = self.AxisPositionController_stub.MoveToHomePosition(
                AxisPositionController_pb2.MoveToHomePosition_Parameters(),
                metadata
            )
            logging.debug(f"MoveToHomePosition response: {response}")

        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return


    def StopMoving(self, axis_id: str): # -> (AxisPositionController):
        """
        Wrapper to call the unobservable command StopMoving on the server.

        :param axis_id: The index of the axis to use. Will be sent along as metadata
                        of the call

        :returns: A gRPC object with the response that has been defined for this command.
        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug(f"Calling StopMoving for axis {axis_id}:")
        try:
            metadata = ((METADATA_AXIS_IDENTIFIER, self._serialize_axis_id(axis_id)),)

            response = self.AxisPositionController_stub.StopMoving(
                AxisPositionController_pb2.StopMoving_Parameters(),
                metadata
            )
            logging.debug(f"StopMoving response: {response}")

        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return



    def Subscribe_Position(self, axis_id: str) \
            -> AxisPositionController_pb2.Subscribe_Position_Responses:
        """
        Wrapper to get property Position from the server.

        :param axis_id: The index of the axis to use. Will be sent along as metadata
                        of the call
        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug(f"Reading observable property Position for axis {axis_id}:")
        try:
            metadata = ((METADATA_AXIS_IDENTIFIER, self._serialize_axis_id(axis_id)),)
            response = self.AxisPositionController_stub.Subscribe_Position(
                AxisPositionController_pb2.Subscribe_Position_Parameters(),
                metadata
            )
            logging.debug(
                'Subscribe_Position response: {response}'.format(
                    response=response
                )
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response

    def Get_PositionUnit(self, axis_id: str) \
            -> AxisPositionController_pb2.Get_PositionUnit_Responses:
        """
        Wrapper to get property PositionUnit from the server.

        :param axis_id: The index of the axis to use. Will be sent along as metadata
                        of the call
        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug(f"Reading unobservable property PositionUnit for axis {axis_id}:")
        try:
            metadata = ((METADATA_AXIS_IDENTIFIER, self._serialize_axis_id(axis_id)),)
            response = self.AxisPositionController_stub.Get_PositionUnit(
                AxisPositionController_pb2.Get_PositionUnit_Parameters(),
                metadata
            )
            logging.debug(
                'Get_PositionUnit response: {response}'.format(
                    response=response
                )
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response.PositionUnit

    def Get_MinimumPosition(self, axis_id: str) \
            -> AxisPositionController_pb2.Get_MinimumPosition_Responses:
        """
        Wrapper to get property MinimumPosition from the server.

        :param axis_id: The index of the axis to use. Will be sent along as metadata
                        of the call
        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug(f"Reading unobservable property MinimumPosition for axis {axis_id}:")
        try:
            metadata = ((METADATA_AXIS_IDENTIFIER, self._serialize_axis_id(axis_id)),)
            response = self.AxisPositionController_stub.Get_MinimumPosition(
                AxisPositionController_pb2.Get_MinimumPosition_Parameters(),
                metadata
            )
            logging.debug(
                'Get_MinimumPosition response: {response}'.format(
                    response=response
                )
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response.MinimumPosition

    def Get_MaximumPosition(self, axis_id: str) \
            -> AxisPositionController_pb2.Get_MaximumPosition_Responses:
        """
        Wrapper to get property MaximumPosition from the server.

        :param axis_id: The index of the axis to use. Will be sent along as metadata
                        of the call
        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug(f"Reading unobservable property MaximumPosition for axis {axis_id}:")
        try:
            metadata = ((METADATA_AXIS_IDENTIFIER, self._serialize_axis_id(axis_id)),)
            response = self.AxisPositionController_stub.Get_MaximumPosition(
                AxisPositionController_pb2.Get_MaximumPosition_Parameters(),
                metadata
            )
            logging.debug(
                'Get_MaximumPosition response: {response}'.format(
                    response=response
                )
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response.MaximumPosition

    def Get_MinimumVelocity(self, axis_id: str) \
            -> AxisPositionController_pb2.Get_MinimumVelocity_Responses:
        """
        Wrapper to get property MinimumVelocity from the server.

        :param axis_id: The index of the axis to use. Will be sent along as metadata
                        of the call
        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug(f"Reading unobservable property MinimumVelocity for axis {axis_id}:")
        try:
            metadata = ((METADATA_AXIS_IDENTIFIER, self._serialize_axis_id(axis_id)),)
            response = self.AxisPositionController_stub.Get_MinimumVelocity(
                AxisPositionController_pb2.Get_MinimumVelocity_Parameters(),
                metadata
            )
            logging.debug(
                'Get_MinimumVelocity response: {response}'.format(
                    response=response
                )
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response.MinimumVelocity

    def Get_MaximumVelocity(self, axis_id: str) \
            -> AxisPositionController_pb2.Get_MaximumVelocity_Responses:
        """
        Wrapper to get property MaximumVelocity from the server.

        :param axis_id: The index of the axis to use. Will be sent along as metadata
                        of the call
        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug(f"Reading unobservable property MaximumVelocity for axis {axis_id}:")
        try:
            metadata = ((METADATA_AXIS_IDENTIFIER, self._serialize_axis_id(axis_id)),)
            response = self.AxisPositionController_stub.Get_MaximumVelocity(
                AxisPositionController_pb2.Get_MaximumVelocity_Parameters(),
                metadata
            )
            logging.debug(
                'Get_MaximumVelocity response: {response}'.format(
                    response=response
                )
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response.MaximumVelocity



    def Get_FCPAffectedByMetadata_AxisIdentifier(self) \
            -> AxisPositionController_pb2.Get_FCPAffectedByMetadata_AxisIdentifier_Responses:
        """
        Wrapper to get property FCPAffectedByMetadata_AxisIdentifier from the server.

        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug("Reading unobservable property FCPAffectedByMetadata_AxisIdentifier:")
        try:
            response = self.AxisPositionController_stub.Get_FCPAffectedByMetadata_AxisIdentifier(
                AxisPositionController_pb2.Get_FCPAffectedByMetadata_AxisIdentifier_Parameters()
            )
            logging.debug(
                'Get_FCPAffectedByMetadata_AxisIdentifier response: {response}'.format(
                    response=response
                )
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response.AffectedCalls



    @staticmethod
    def grpc_error_handling(error_object: grpc.Call) -> None:
        """Handles exceptions of type grpc.RpcError"""
        # pass to the default error handling
        grpc_error =  client_err.grpc_error_handling(error_object=error_object)

        logging.error(grpc_error.error_type)
        if hasattr(grpc_error.message, "parameter"):
            logging.error(grpc_error.message.parameter)
        logging.error(grpc_error.message.message)



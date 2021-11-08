"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Control Loop Service*

:details: ControlLoopService:
    Allows to control a Qmix Device with a Control Loop

:file:    ControlLoopService_real.py
:authors: Florian Meinicke

:date: (creation)          2020-10-08T09:17:41.395352
:date: (last modification) 2021-10-05T09:04:08.784973

.. note:: Code generated by sila2codegenerator 0.3.6

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

__version__ = "0.1.0"

# import general packages
import logging
import math
import time         # used for observables
import uuid         # used for observables
import grpc         # used for type hinting only
from typing import Dict

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2

# import SiLA errors
from impl.common.errors import SiLAFrameworkError, SiLAFrameworkErrorType

# import gRPC modules for this feature
from .gRPC import ControlLoopService_pb2 as ControlLoopService_pb2
# from .gRPC import ControlLoopService_pb2_grpc as ControlLoopService_pb2_grpc

# import default arguments
from .ControlLoopService_default_arguments import default_dict

from qmixsdk.qmixcontroller import ControllerChannel


# noinspection PyPep8Naming,PyUnusedLocal
class ControlLoopServiceReal:
    """
    Implementation of the *Control Loop Service* in *Real* mode
        The SiLA 2 driver for Qmix Control Devices
    """

    def __init__(self):
        """Class initialiser"""

        logging.debug('Started server in mode: {mode}'.format(mode='Real'))

    def WriteSetPoint(self, request, controller: ControllerChannel, context: grpc.ServicerContext) \
            -> ControlLoopService_pb2.WriteSetPoint_Responses:
        """
        Executes the unobservable command "Write Set Point"
            Write a Set Point value to the Controller Device

        :param request: gRPC request containing the parameters passed:
            request.SetPointValue (Set Point Value): The Set Point value to write
        :param controller: The controller to operate on
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        setpoint = request.SetPointValue.value

        logging.info(f"Writing SetPoint {setpoint} to device")
        controller.write_setpoint(setpoint)

        return ControlLoopService_pb2.WriteSetPoint_Responses()


    def RunControlLoop(self, request, controller: ControllerChannel, context: grpc.ServicerContext) \
            -> silaFW_pb2.CommandConfirmation:
        """
        Executes the observable command "Run Control Loop"
            Run the Control Loop

        :param request: gRPC request containing the parameters passed
        :param controller: The controller to operate on
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A command confirmation object with the following information:
            commandId: A command id with which this observable command can be referenced in future calls
            lifetimeOfExecution: The (maximum) lifetime of this command call.
        """

        controller.enable_control_loop(True)
        result = ('' if controller.is_control_loop_enabled() else 'not ') + 'successful'
        logging.debug(f"Starting control loop with set point {controller.get_setpoint()} was {result}")

        # respond with UUID and lifetime of execution
        return silaFW_pb2.CommandConfirmation(
            commandExecutionUUID=silaFW_pb2.CommandExecutionUUID(value=str(uuid.uuid4()))
        )

    def RunControlLoop_Info(self, request, controller: ControllerChannel, context: grpc.ServicerContext) \
            -> silaFW_pb2.ExecutionInfo:
        """
        Returns execution information regarding the command call :meth:`~.RunControlLoop`.

        :param request: A request object with the following properties
            commandId: The UUID of the command executed.
        :param controller: The controller to operate on
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: An ExecutionInfo response stream for the command with the following fields:
            commandStatus: Status of the command (enumeration)
            progressInfo: Information on the progress of the command (0 to 1)
            estimatedRemainingTime: Estimate of the remaining time required to run the command
            updatedLifetimeOfExecution: An update on the execution lifetime
        """

        yield silaFW_pb2.ExecutionInfo(
            commandStatus=silaFW_pb2.ExecutionInfo.CommandStatus.waiting
        )

        # we loop only as long as the command is running
        while controller.is_control_loop_enabled():
            yield silaFW_pb2.ExecutionInfo(
                commandStatus=silaFW_pb2.ExecutionInfo.CommandStatus.running
            )

            logging.debug(f"Current controller value: {controller.read_actual_value()}")
            logging.debug(f"Device status: {controller.read_status()}")
            # we add a small delay to give the client a chance to keep up.
            time.sleep(1)
        else:
            # one last time yield the status
            yield silaFW_pb2.ExecutionInfo(
                commandStatus=silaFW_pb2.ExecutionInfo.CommandStatus.finishedSuccessfully
            )

    def RunControlLoop_Result(self, request, controller: ControllerChannel, context: grpc.ServicerContext) \
            -> ControlLoopService_pb2.RunControlLoop_Responses:
        """
        Returns the final result of the command call :meth:`~.RunControlLoop`.

        :param request: A request object with the following properties
            CommandExecutionUUID: The UUID of the command executed.
        :param controller: The controller to operate on
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        return ControlLoopService_pb2.RunControlLoop_Responses()


    def StopControlLoop(self, request, controller: ControllerChannel, context: grpc.ServicerContext) \
            -> ControlLoopService_pb2.StopControlLoop_Responses:
        """
        Executes the unobservable command "Stop Control Loop"
            Stops the Control Loop (has no effect, if no Loop is currently running)

        :param request: gRPC request containing the parameters passed
        :param controller: The controller to operate on
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        controller.enable_control_loop(False)

        return ControlLoopService_pb2.StopControlLoop_Responses()

    def Subscribe_ControllerValue(self, request, controller: ControllerChannel, context: grpc.ServicerContext) \
            -> ControlLoopService_pb2.Subscribe_ControllerValue_Responses:
        """
        Requests the observable property Controller Value
            The actual value from the Device

        :param request: An empty gRPC request object (properties have no parameters)
        :param controller: The controller to operate on
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            ControllerValue (Controller Value): The actual value from the Device
        """

        new_value = controller.read_actual_value()
        value = new_value + 1 # force sending the first value
        while True:
            new_value = controller.read_actual_value()
            if not math.isclose(new_value, value):
                value = new_value
                yield ControlLoopService_pb2.Subscribe_ControllerValue_Responses(
                    ControllerValue=silaFW_pb2.Real(value=value)
                )
            time.sleep(0.1) # give client some time to catch up


    def Subscribe_SetPointValue(self, request, controller: ControllerChannel, context: grpc.ServicerContext) \
            -> ControlLoopService_pb2.Subscribe_SetPointValue_Responses:
        """
        Requests the observable property Set Point Value
            The current SetPoint value of the Device

        :param request: An empty gRPC request object (properties have no parameters)
        :param controller: The controller to operate on
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            SetPointValue (Set Point Value): The current SetPoint value of the Device
        """

        new_setpoint = controller.get_setpoint()
        setpoint = new_setpoint + 1 # force sending the first value
        while True:
            new_setpoint = controller.get_setpoint()
            if not math.isclose(new_setpoint, setpoint):
                setpoint = new_setpoint
                yield ControlLoopService_pb2.Subscribe_SetPointValue_Responses(
                    SetPointValue=silaFW_pb2.Real(value=setpoint)
                )
            time.sleep(0.1) # give client some time to catch up

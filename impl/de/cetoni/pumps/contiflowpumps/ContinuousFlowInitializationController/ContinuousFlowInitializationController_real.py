"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Continuous Flow Initialization Controller*

:details: ContinuousFlowInitializationController:
    Allows to initialize a contiflow pump before starting the continuous flow.

:file:    ContinuousFlowInitializationController_real.py
:authors: Florian Meinicke

:date: (creation)          2020-10-22T07:15:54.314816
:date: (last modification) 2021-07-10T10:33:25.074361

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
import time         # used for observables
import uuid         # used for observables
import grpc         # used for type hinting only

from sila2lib.error_handling.server_err import SiLAFrameworkError, SiLAFrameworkErrorType

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2

# import gRPC modules for this feature
from .gRPC import ContinuousFlowInitializationController_pb2 as ContinuousFlowInitializationController_pb2
# from .gRPC import ContinuousFlowInitializationController_pb2_grpc as ContinuousFlowInitializationController_pb2_grpc

# import default arguments
from .ContinuousFlowInitializationController_default_arguments import default_dict

# import qmixsdk
from qmixsdk.qmixbus import PollingTimer
from qmixsdk.qmixpump import *


# noinspection PyPep8Naming,PyUnusedLocal
class ContinuousFlowInitializationControllerReal:
    """
    Implementation of the *Continuous Flow Initialization Controller* in *Real* mode
        Allows to control a continuous flow pump that is made up of two syringe pumps
    """

    def __init__(self, pump: ContiFlowPump, simulation_mode: bool = True):
        """
        Class initialiser.

        :param pump: A valid `qxmixpump.ContiFlowPump` for this service to use
        :param simulation_mode: Sets whether at initialisation the simulation mode is active or the real mode.
        """

        self.pump = pump
        self.timer = PollingTimer(30000)

        logging.debug('Started server in mode: {mode}'.format(mode='Real'))

    def _get_initialization_state(self) -> silaFW_pb2.ExecutionInfo:
        """
        Method to fill an ExecutionInfo message from the SiLA server for the InitializeContiflow observable command

        :return: An execution info object with the current command state
        """

        #: Enumeration of silaFW_pb2.ExecutionInfo.CommandStatus
        command_status = silaFW_pb2.ExecutionInfo.CommandStatus.waiting
        if self.pump.is_initializing() and not self.timer.is_expired():
            command_status = silaFW_pb2.ExecutionInfo.CommandStatus.running
        elif self.pump.is_initialized():
            command_status = silaFW_pb2.ExecutionInfo.CommandStatus.finishedSuccessfully
        else:
            command_status = silaFW_pb2.ExecutionInfo.CommandStatus.finishedWithError
        #: Duration silaFW_pb2.Duration(seconds=<seconds>, nanos=<nanos>)
        command_estimated_remaining = self.timer.get_msecs_to_expiration() / 1000

        return silaFW_pb2.ExecutionInfo(
            commandStatus=command_status,
            estimatedRemainingTime=silaFW_pb2.Duration(
                seconds=int(command_estimated_remaining)
            ),
            updatedLifetimeOfExecution=silaFW_pb2.Duration(
                seconds=int(self.timer.period_ms / 1000)
            )
        )

    def InitializeContiflow(self, request, context: grpc.ServicerContext) \
            -> silaFW_pb2.CommandConfirmation:
        """
        Executes the observable command "Initialize Contiflow"
            Initialize the continuous flow pump.
            Call this command after all parameters have been set, to prepare the conti flow pump for the start of the continuous flow. The initialization procedure ensures, that the syringes are sufficiently filled to start the continuous flow. So calling this command may cause a syringe refill if the syringes are not sufficiently filled. So before calling this command you should ensure, that syringe refilling properly works an can be executed. If you have a certain syringe refill procedure, you can also manually refill the syringes with the normal syringe pump functions. If the syringes are sufficiently filled if you call this function, no refilling will take place.

        :param request: gRPC request containing the parameters passed:
            request.EmptyParameter (Empty Parameter): An empty parameter data type used if no parameter is required.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A command confirmation object with the following information:
            commandId: A command id with which this observable command can be referenced in future calls
            lifetimeOfExecution: The (maximum) lifetime of this command call.
        """

        self.pump.initialize()
        self.timer.restart()

        # respond with UUID and lifetime of execution
        self.command_uuid = silaFW_pb2.CommandExecutionUUID(value=str(uuid.uuid4()))
        return silaFW_pb2.CommandConfirmation(
            commandExecutionUUID=self.command_uuid,
            lifetimeOfExecution=silaFW_pb2.Duration(seconds=int(self.timer.period_ms / 1000))
        )

    def InitializeContiflow_Info(self, request, context: grpc.ServicerContext) \
            -> silaFW_pb2.ExecutionInfo:
        """
        Returns execution information regarding the command call :meth:`~.InitializeContiflow`.

        :param request: A request object with the following properties
            commandId: The UUID of the command executed.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: An ExecutionInfo response stream for the command with the following fields:
            commandStatus: Status of the command (enumeration)
            progressInfo: Information on the progress of the command (0 to 1)
            estimatedRemainingTime: Estimate of the remaining time required to run the command
            updatedLifetimeOfExecution: An update on the execution lifetime
        """
        if request != self.command_uuid:
            raise SiLAFrameworkError(SiLAFrameworkErrorType.INVALID_COMMAND_EXECUTION_UUID)

        # Get the current state
        execution_info = self._get_initialization_state()

        # we loop only as long as the command is running
        while execution_info.commandStatus == silaFW_pb2.ExecutionInfo.CommandStatus.waiting \
                or execution_info.commandStatus == silaFW_pb2.ExecutionInfo.CommandStatus.running:
            # Update all values
            execution_info = self._get_initialization_state()

            yield execution_info

            # we add a small delay to give the client a chance to keep up.
            time.sleep(0.5)
        else:
            # one last time yield the status
            yield execution_info

    def InitializeContiflow_Result(self, request, context: grpc.ServicerContext) \
            -> ContinuousFlowInitializationController_pb2.InitializeContiflow_Responses:
        """
        Returns the final result of the command call :meth:`~.InitializeContiflow`.

        :param request: A request object with the following properties
            CommandExecutionUUID: The UUID of the command executed.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """
        if request != self.command_uuid:
            raise SiLAFrameworkError(SiLAFrameworkErrorType.INVALID_COMMAND_EXECUTION_UUID)

        return ContinuousFlowInitializationController_pb2.InitializeContiflow_Responses()


    def Subscribe_IsInitialized(self, request, context: grpc.ServicerContext) \
            -> ContinuousFlowInitializationController_pb2.Subscribe_IsInitialized_Responses:
        """
        Requests the observable property Is Initialized
            Returns true, if the continuous fow pump is initialized and ready for continuous flow start.
            Use this function to check if the pump is initialized before you start a continuous flow. If you change and continuous flow parameter, like valve settings, cross flow duration and so on, the pump will leave the initialized state. That means, after each parameter change, an initialization is required. Changing the flow rate or the dosing volume does not require and initialization.


        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            IsInitialized (Is Initialized): Returns true, if the continuous fow pump is initialized and ready for continuous flow start.
            Use this function to check if the pump is initialized before you start a continuous flow. If you change and continuous flow parameter, like valve settings, cross flow duration and so on, the pump will leave the initialized state. That means, after each parameter change, an initialization is required. Changing the flow rate or the dosing volume does not require and initialization.
        """

        while True:
            yield ContinuousFlowInitializationController_pb2.Subscribe_IsInitialized_Responses(
                IsInitialized=silaFW_pb2.Boolean(value=self.pump.is_initialized())
            )

            time.sleep(0.5) # give client a chance to keep up

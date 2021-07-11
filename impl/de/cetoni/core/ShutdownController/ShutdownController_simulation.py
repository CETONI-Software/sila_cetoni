"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Shutdown Controller*

:details: ShutdownController:
    Provides a generic way of telling a SiLA2 server that it is about to be shut down. The server implements a routine
    to be executed before the hardware is shut down (e.g. saving device parameters or bringing the device into a safe
    position).

:file:    ShutdownController_simulation.py
:authors: Florian Meinicke

:date: (creation)          2019-07-17T09:54:01.897783
:date: (last modification) 2021-07-09T10:33:27.668515

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

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2

# import gRPC modules for this feature
from .gRPC import ShutdownController_pb2 as ShutdownController_pb2
# from .gRPC import ShutdownController_pb2_grpc as ShutdownController_pb2_grpc

# import default arguments
from .ShutdownController_default_arguments import default_dict

# import SiLA Defined Error factories
from .ShutdownController_defined_errors import ShutdownFailedError

# noinspection PyPep8Naming,PyUnusedLocal
class ShutdownControllerSimulation:
    """
    Implementation of the *Shutdown Controller* in *Simulation* mode
    """

    def __init__(self):
        """Class initialiser"""

        logging.debug('Started server in mode: {mode}'.format(mode='Simulation'))

    def _get_command_state(self, command_uuid: str) -> silaFW_pb2.ExecutionInfo:
        """
        Method to fill an ExecutionInfo message from the SiLA server for observable commands

        :param command_uuid: The uuid of the command for which to return the current state

        :return: An execution info object with the current command state
        """

        #: Enumeration of silaFW_pb2.ExecutionInfo.CommandStatus
        command_status = silaFW_pb2.ExecutionInfo.CommandStatus.waiting
        #: Real silaFW_pb2.Real(0...1)
        command_progress = None
        #: Duration silaFW_pb2.Duration(seconds=<seconds>, nanos=<nanos>)
        command_estimated_remaining = None
        #: Duration silaFW_pb2.Duration(seconds=<seconds>, nanos=<nanos>)
        command_lifetime_of_execution = None

        # TODO: check the state of the command with the given uuid and return the correct information

        # just return a default in this example
        return silaFW_pb2.ExecutionInfo(
            commandStatus=command_status,
            progressInfo=(
                command_progress if command_progress is not None else None
            ),
            estimatedRemainingTime=(
                command_estimated_remaining if command_estimated_remaining is not None else None
            ),
            updatedLifetimeOfExecution=(
                command_lifetime_of_execution if command_lifetime_of_execution is not None else None
            )
        )

    def Shutdown(self, request, context: grpc.ServicerContext) \
            -> silaFW_pb2.CommandConfirmation:
        """
        Executes the observable command "Shutdown"
            Initiates the shutdown routine. If no errors occurred during the shutdown process the server should be considered ready to be physically shutdown (i.e. the device can be shut down/powered off).

        :param request: gRPC request containing the parameters passed:
            request.EmptyParameter (Empty Parameter): An empty parameter data type used if no parameter is required.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A command confirmation object with the following information:
            commandId: A command id with which this observable command can be referenced in future calls
            lifetimeOfExecution: The (maximum) lifetime of this command call.
        """

        # initialise default values
        #: Duration silaFW_pb2.Duration(seconds=<seconds>, nanos=<nanos>)
        lifetime_of_execution: silaFW_pb2.Duration = None

        # TODO:
        #   Execute the actual command
        #   Optional: Generate a lifetime_of_execution

        # respond with UUID and lifetime of execution
        command_uuid = silaFW_pb2.CommandExecutionUUID(value=str(uuid.uuid4()))
        if lifetime_of_execution is not None:
            return silaFW_pb2.CommandConfirmation(
                commandExecutionUUID=command_uuid,
                lifetimeOfExecution=lifetime_of_execution
            )
        else:
            return silaFW_pb2.CommandConfirmation(
                commandExecutionUUID=command_uuid
            )

    def Shutdown_Info(self, request, context: grpc.ServicerContext) \
            -> silaFW_pb2.ExecutionInfo:
        """
        Returns execution information regarding the command call :meth:`~.Shutdown`.

        :param request: A request object with the following properties
            commandId: The UUID of the command executed.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: An ExecutionInfo response stream for the command with the following fields:
            commandStatus: Status of the command (enumeration)
            progressInfo: Information on the progress of the command (0 to 1)
            estimatedRemainingTime: Estimate of the remaining time required to run the command
            updatedLifetimeOfExecution: An update on the execution lifetime
        """
        # Get the UUID of the command
        command_uuid = request.value

        # Get the current state
        execution_info = self._get_command_state(command_uuid=command_uuid)

        # construct the initial return dictionary in case while is not executed
        return_values = {'commandStatus': execution_info.commandStatus}
        if execution_info.HasField('progressInfo'):
            return_values['progressInfo'] = execution_info.progressInfo
        if execution_info.HasField('estimatedRemainingTime'):
            return_values['estimatedRemainingTime'] = execution_info.estimatedRemainingTime
        if execution_info.HasField('updatedLifetimeOfExecution'):
            return_values['updatedLifetimeOfExecution'] = execution_info.updatedLifetimeOfExecution

        # we loop only as long as the command is running
        while execution_info.commandStatus == silaFW_pb2.ExecutionInfo.CommandStatus.waiting \
                or execution_info.commandStatus == silaFW_pb2.ExecutionInfo.CommandStatus.running:
            # TODO:
            #   Evaluate the command status --> command_status. Options:
            #       command_stats = silaFW_pb2.ExecutionInfo.CommandStatus.waiting
            #       command_stats = silaFW_pb2.ExecutionInfo.CommandStatus.running
            #       command_stats = silaFW_pb2.ExecutionInfo.CommandStatus.finishedSuccessfully
            #       command_stats = silaFW_pb2.ExecutionInfo.CommandStatus.finishedWithError
            #   Optional:
            #       * Determine the progress (progressInfo)
            #       * Determine the estimated remaining time
            #       * Update the Lifetime of execution

            # Update all values
            execution_info = self._get_command_state(command_uuid=command_uuid)

            # construct the return dictionary
            return_values = {'commandStatus': execution_info.commandStatus}
            if execution_info.HasField('progressInfo'):
                return_values['progressInfo'] = execution_info.progressInfo
            if execution_info.HasField('estimatedRemainingTime'):
                return_values['estimatedRemainingTime'] = execution_info.estimatedRemainingTime
            if execution_info.HasField('updatedLifetimeOfExecution'):
                return_values['updatedLifetimeOfExecution'] = execution_info.updatedLifetimeOfExecution

            yield silaFW_pb2.ExecutionInfo(**return_values)

            # we add a small delay to give the client a chance to keep up.
            time.sleep(0.5)
        else:
            # one last time yield the status
            yield silaFW_pb2.ExecutionInfo(**return_values)

    def Shutdown_Result(self, request, context: grpc.ServicerContext) \
            -> ShutdownController_pb2.Shutdown_Responses:
        """
        Returns the final result of the command call :meth:`~.Shutdown`.

        :param request: A request object with the following properties
            CommandExecutionUUID: The UUID of the command executed.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        # initialise the return value
        return_value: ShutdownController_pb2.Shutdown_Responses = None

        # Get the UUID of the command
        command_uuid = request.value

        # TODO:
        #   Add implementation of Simulation for command Shutdown here and write the resulting response
        #   in return_value

        # fallback to default
        if return_value is None:
            return_value = ShutdownController_pb2.Shutdown_Responses(
                #**default_dict['Shutdown_Responses']
            )

        return return_value

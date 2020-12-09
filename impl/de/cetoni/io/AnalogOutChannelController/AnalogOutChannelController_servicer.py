"""
________________________________________________________________________

:PROJECT: SiLA2_python

*Analog Out Channel Controller*

:details: AnalogOutChannelController:
    Allows to control one analog out channel of an I/O module

:file:    AnalogOutChannelController_servicer.py
:authors: Florian Meinicke

:date: (creation)          2020-12-09T09:15:03.169510
:date: (last modification) 2020-12-09T09:15:03.169510

.. note:: Code generated by sila2codegenerator 0.2.0

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
import grpc

# meta packages
from typing import Union

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
from sila2lib.error_handling.server_err import SiLAError

# import SiLA errors
from impl.common.qmix_error import QmixSDKError, DeviceError, SiLAFrameworkError, SiLAValidationError

# import gRPC modules for this feature
from .gRPC import AnalogOutChannelController_pb2 as AnalogOutChannelController_pb2
from .gRPC import AnalogOutChannelController_pb2_grpc as AnalogOutChannelController_pb2_grpc

# import simulation and real implementation
from .AnalogOutChannelController_simulation import AnalogOutChannelControllerSimulation
from .AnalogOutChannelController_real import AnalogOutChannelControllerReal


class AnalogOutChannelController(AnalogOutChannelController_pb2_grpc.AnalogOutChannelControllerServicer):
    """
    The SiLA 2 driver for Qmix I/O Devices
    """
    implementation: Union[AnalogOutChannelControllerSimulation, AnalogOutChannelControllerReal]
    simulation_mode: bool

    def __init__(self, channel, simulation_mode: bool = True):
        """
        Class initialiser.

        :param channel: The Qmix I/O channel
        :param simulation_mode: Sets whether at initialisation the simulation mode is active or the real mode.
        """

        self.channel = channel
        self.simulation_mode = simulation_mode
        if simulation_mode:
            self.switch_to_simulation_mode()
        else:
            self.switch_to_real_mode()

    def _inject_implementation(self,
                               implementation: Union[AnalogOutChannelControllerSimulation,
                                                     AnalogOutChannelControllerReal]
                               ) -> bool:
        """
        Dependency injection of the implementation used.
            Allows to set the class used for simulation/real mode.

        :param implementation: A valid implementation of the QmixIOServicer.
        """

        self.implementation = implementation
        return True

    def switch_to_simulation_mode(self):
        """Method that will automatically be called by the server when the simulation mode is requested."""
        self.simulation_mode = True
        self._inject_implementation(AnalogOutChannelControllerSimulation())

    def switch_to_real_mode(self):
        """Method that will automatically be called by the server when the real mode is requested."""
        self.simulation_mode = False
        self._inject_implementation(AnalogOutChannelControllerReal(self.channel))

    def SetOutputValue(self, request, context: grpc.ServicerContext) \
            -> AnalogOutChannelController_pb2.SetOutputValue_Responses:
        """
        Executes the unobservable command "Set Output Value"
            Set the value of the analog output channel.

        :param request: gRPC request containing the parameters passed:
            request.Value (Value): The value to set.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            request.EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        logging.debug(
            "SetOutputValue called in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )

        try:
            return self.implementation.SetOutputValue(request, context)
        except DeviceError as err:
            err = QmixSDKError(err)
            err.raise_rpc_error(context=context)

    def Subscribe_Value(self, request, context: grpc.ServicerContext) \
            -> AnalogOutChannelController_pb2.Subscribe_Value_Responses:
        """
        Requests the observable property Value
            The value of the analog I/O channel.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response stream with the following fields:
            request.Value (Value): The value of the analog I/O channel.
        """

        logging.debug(
            "Property Value requested in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )
        try:
            return self.implementation.Subscribe_Value(request, context)
        except DeviceError as err:
            err = QmixSDKError(err)
            err.raise_rpc_error(context=context)


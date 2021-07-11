"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Pump Unit Controller*

:details: PumpUnitController:
    Allows to control the currently used units for passing and retrieving flow rates and volumes to and from a pump.

:file:    PumpUnitController_servicer.py
:authors: Florian Meinicke

:date: (creation)          2019-07-16T11:11:31.287651
:date: (last modification) 2021-07-11T07:37:45.427832

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
import grpc

# meta packages
from typing import Union

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
# import SiLA errors
from impl.common.qmix_errors import SiLAError, DeviceError, QmixSDKSiLAError, UnitConversionError

# import gRPC modules for this feature
from .gRPC import PumpUnitController_pb2 as PumpUnitController_pb2
from .gRPC import PumpUnitController_pb2_grpc as PumpUnitController_pb2_grpc

# import simulation and real implementation
from .PumpUnitController_simulation import PumpUnitControllerSimulation
from .PumpUnitController_real import PumpUnitControllerReal


class PumpUnitController(PumpUnitController_pb2_grpc.PumpUnitControllerServicer):
    """
    This is a sample service for controlling neMESYS syringe pumps via SiLA2
    """
    implementation: Union[PumpUnitControllerSimulation, PumpUnitControllerReal]
    simulation_mode: bool

    def __init__(self, pump, simulation_mode: bool = True):
        """
        Class initialiser.

        :param pump: A valid `qxmixpump` for this service to use
        :param simulation_mode: Sets whether at initialisation the simulation mode is active or the real mode
        """

        self.pump = pump

        self.simulation_mode = simulation_mode
        if simulation_mode:
            self.switch_to_simulation_mode()
        else:
            self.switch_to_real_mode()

    def _inject_implementation(self,
                               implementation: Union[PumpUnitControllerSimulation,
                                                     PumpUnitControllerReal]
                               ) -> bool:
        """
        Dependency injection of the implementation used.
            Allows to set the class used for simulation/real mode.

        :param implementation: A valid implementation of the neMESYSServicer.
        """

        self.implementation = implementation
        return True

    def switch_to_simulation_mode(self):
        """Method that will automatically be called by the server when the simulation mode is requested."""
        self.simulation_mode = True
        self._inject_implementation(PumpUnitControllerSimulation())

    def switch_to_real_mode(self):
        """Method that will automatically be called by the server when the real mode is requested."""
        self.simulation_mode = False
        self._inject_implementation(PumpUnitControllerReal(self.pump))

    def SetFlowUnit(self, request, context: grpc.ServicerContext) \
            -> PumpUnitController_pb2.SetFlowUnit_Responses:
        """
        Executes the unobservable command "Set Flow Unit"
            Sets the flow unit for the pump. The flow unit defines the unit to be used for all flow values passed to or retrieved from the pump.

        :param request: gRPC request containing the parameters passed:
            request.FlowUnit (Flow Unit): The flow unit to be set.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        logging.debug(
            "SetFlowUnit called in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )

        # parameter validation
        # if request.my_paramameter.value out of scope :
        #        sila_val_err = SiLAValidationError(parameter="myParameter",
        #                                           msg=f"Parameter {request.my_parameter.value} out of scope!")
        #        sila_val_err.raise_rpc_error(context)

        try:
            return self.implementation.SetFlowUnit(request, context)
        except (SiLAError, UnitConversionError, DeviceError) as err:
            if isinstance(err, DeviceError):
                err = QmixSDKSiLAError(err)
            err.raise_rpc_error(context)

    def SetVolumeUnit(self, request, context: grpc.ServicerContext) \
            -> PumpUnitController_pb2.SetVolumeUnit_Responses:
        """
        Executes the unobservable command "Set Volume Unit"
            Sets the default volume unit. The volume unit defines the unit to be used for all volume values passed to or retrieved from the pump.

        :param request: gRPC request containing the parameters passed:
            request.VolumeUnit (Volume Unit): The volume unit for the flow rate.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        logging.debug(
            "SetVolumeUnit called in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )

        # parameter validation
        # if request.my_paramameter.value out of scope :
        #        sila_val_err = SiLAValidationError(parameter="myParameter",
        #                                           msg=f"Parameter {request.my_parameter.value} out of scope!")
        #        sila_val_err.raise_rpc_error(context)

        try:
            return self.implementation.SetVolumeUnit(request, context)
        except (SiLAError, UnitConversionError, DeviceError) as err:
            if isinstance(err, DeviceError):
                err = QmixSDKSiLAError(err)
            err.raise_rpc_error(context)

    def Subscribe_FlowUnit(self, request, context: grpc.ServicerContext) \
            -> PumpUnitController_pb2.Subscribe_FlowUnit_Responses:
        """
        Requests the observable property Flow Unit
            The currently used flow unit.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response stream with the following fields:
            FlowUnit (Flow Unit): The currently used flow unit.
        """

        logging.debug(
            "Property FlowUnit requested in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )

        try:
            for value in self.implementation.Subscribe_FlowUnit(request, context):
                yield value
        except (SiLAError, UnitConversionError, DeviceError) as err:
            if isinstance(err, DeviceError):
                err = QmixSDKSiLAError(err)
            err.raise_rpc_error(context)

    def Subscribe_VolumeUnit(self, request, context: grpc.ServicerContext) \
            -> PumpUnitController_pb2.Subscribe_VolumeUnit_Responses:
        """
        Requests the observable property Volume Unit
            The currently used volume unit.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response stream with the following fields:
            VolumeUnit (Volume Unit): The currently used volume unit.
        """

        logging.debug(
            "Property VolumeUnit requested in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )

        try:
            for value in self.implementation.Subscribe_VolumeUnit(request, context):
                yield value
        except (SiLAError, UnitConversionError, DeviceError) as err:
            if isinstance(err, DeviceError):
                err = QmixSDKSiLAError(err)
            err.raise_rpc_error(context)


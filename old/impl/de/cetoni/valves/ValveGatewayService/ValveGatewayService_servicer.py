"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Valve Gateway Service*

:details: ValveGatewayService:
    Provides means to access individual valves of a valve terminal

:file:    ValveGatewayService_servicer.py
:authors: Florian Meinicke

:date: (creation)          2021-01-07T13:40:21.896121
:date: (last modification) 2021-07-10T09:27:04.765906

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
from typing import Union, Tuple

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
from sila2lib.error_handling.server_err import SiLAError

# import gRPC modules for this feature
from .gRPC import ValveGatewayService_pb2 as ValveGatewayService_pb2
from .gRPC import ValveGatewayService_pb2_grpc as ValveGatewayService_pb2_grpc

# import simulation and real implementation
from .ValveGatewayService_simulation import ValveGatewayServiceSimulation
from .ValveGatewayService_real import ValveGatewayServiceReal


class ValveGatewayService(ValveGatewayService_pb2_grpc.ValveGatewayServiceServicer):
    """
    Allows to control valve devices
    """
    implementation: Union[ValveGatewayServiceSimulation, ValveGatewayServiceReal]
    simulation_mode: bool

    def __init__(self, valves: list, simulation_mode: bool = True):
        """
        Class initialiser.

        :param valves: A list of valves for a single valve device
        :param simulation_mode: Sets whether at initialisation the simulation mode is active or the real mode.
        """

        self.valves = valves

        self.simulation_mode = simulation_mode
        if simulation_mode:
            self.switch_to_simulation_mode()
        else:
            self.switch_to_real_mode()

    def _inject_implementation(self,
                               implementation: Union[ValveGatewayServiceSimulation,
                                                     ValveGatewayServiceReal]
                               ) -> bool:
        """
        Dependency injection of the implementation used.
            Allows to set the class used for simulation/real mode.

        :param implementation: A valid implementation of the ValveServicer.
        """

        self.implementation = implementation
        return True

    def switch_to_simulation_mode(self):
        """Method that will automatically be called by the server when the simulation mode is requested."""
        self.simulation_mode = True
        self._inject_implementation(ValveGatewayServiceSimulation())

    def switch_to_real_mode(self):
        """Method that will automatically be called by the server when the real mode is requested."""
        self.simulation_mode = False
        self._inject_implementation(ValveGatewayServiceReal(self.valves))

    def get_valve(self, metadata: Tuple[Tuple[str, str]], type: str):
        """
        Get the valve that is identified by the valve name given in `metadata`

        :param metdata: The metadata of the call. It should contain the requested valve name
        :param type: Either "Command" or "Property"
        :return: A valid valve object if the valve can be identified, otherwise a SiLAFrameworkError will be raised
        """
        return self.implementation.get_valve(metadata, type)

    def Get_NumberOfValves(self, request, context: grpc.ServicerContext) \
            -> ValveGatewayService_pb2.Get_NumberOfValves_Responses:
        """
        Requests the unobservable property Number Of Valves
            The number of valves of a terminal

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            NumberOfValves (Number Of Valves): The number of valves of a terminal
        """

        logging.debug(
            "Property NumberOfValves requested in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )
        try:
            return self.implementation.Get_NumberOfValves(request, context)
        except SiLAError as err:
            err.raise_rpc_error(context=context)

    def Get_FCPAffectedByMetadata_ValveIndex(self, request, context: grpc.ServicerContext) \
            -> ValveGatewayService_pb2.Get_FCPAffectedByMetadata_ValveIndex_Responses:
        """
        Requests the unobservable property FCPAffectedByMetadata Valve Index
            Specifies which Features/Commands/Properties of the SiLA server are affected by the Valve Index Metadata.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            AffectedCalls (AffectedCalls): A string containing a list of Fully Qualified Identifiers of Features, Commands and Properties for which the SiLA Client Metadata is expected as part of the respective RPCs.
        """

        logging.debug(
            "Property FCPAffectedByMetadata_ValveIndex requested in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )
        try:
            return self.implementation.Get_FCPAffectedByMetadata_ValveIndex(request, context)
        except SiLAError as err:
            err.raise_rpc_error(context=context)
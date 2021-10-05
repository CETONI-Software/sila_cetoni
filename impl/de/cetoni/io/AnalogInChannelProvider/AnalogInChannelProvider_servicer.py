"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Analog In Channel Provider*

:details: AnalogInChannelProvider:
    Allows to control one analog input channel of an I/O module

:file:    AnalogInChannelProvider_servicer.py
:authors: Florian Meinicke

:date: (creation)          2020-12-09T09:15:03.159511
:date: (last modification) 2021-07-08T11:41:56.256026

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
from typing import Union, List

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2

# import SiLA errors
from impl.common.errors import QmixSDKSiLAError, DeviceError, SiLAError

# import helpers
from impl.common.decorators import channel_index, InvalidChannelIndexError as DecoratorInvalidChannelIndex

# import gRPC modules for this feature
from .gRPC import AnalogInChannelProvider_pb2 as AnalogInChannelProvider_pb2
from .gRPC import AnalogInChannelProvider_pb2_grpc as AnalogInChannelProvider_pb2_grpc

# import simulation and real implementation
from .AnalogInChannelProvider_simulation import AnalogInChannelProviderSimulation
from .AnalogInChannelProvider_real import AnalogInChannelProviderReal

# import SiLA Defined Error factories
from .AnalogInChannelProvider_defined_errors import InvalidChannelIndexError

from qmixsdk.qmixanalogio import AnalogInChannel

from . import METADATA_CHANNEL_INDEX


@channel_index(AnalogInChannelProvider_pb2, METADATA_CHANNEL_INDEX)
class AnalogInChannelProvider(AnalogInChannelProvider_pb2_grpc.AnalogInChannelProviderServicer):
    """
    The SiLA 2 driver for Qmix I/O Devices
    """
    implementation: Union[AnalogInChannelProviderSimulation, AnalogInChannelProviderReal]
    simulation_mode: bool

    def __init__(self, channels: List[AnalogInChannel], simulation_mode: bool = True):
        """
        Class initialiser.

        :param channels: The channels that this feature can operate on
        :param simulation_mode: Sets whether at initialisation the simulation mode is active or the real mode.
        """

        self.channels = channels
        self.num_channels = len(self.channels)

        self.simulation_mode = simulation_mode
        if simulation_mode:
            self.switch_to_simulation_mode()
        else:
            self.switch_to_real_mode()

    def _inject_implementation(self,
                               implementation: Union[AnalogInChannelProviderSimulation,
                                                     AnalogInChannelProviderReal]
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
        self._inject_implementation(AnalogInChannelProviderSimulation())

    def switch_to_real_mode(self):
        """Method that will automatically be called by the server when the real mode is requested."""
        self.simulation_mode = False
        self._inject_implementation(AnalogInChannelProviderReal())

    def Get_NumberOfChannels(self, request, context: grpc.ServicerContext) \
            -> AnalogInChannelProvider_pb2.Get_NumberOfChannels_Responses:
        """
        Requests the unobservable property Number Of Channels
            The number of analog input channels. This value is 0-indexed, i.e. the first channel has index 0, the second one index 1 and so on.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            NumberOfChannels (Number Of Channels): The number of analog input channels. This value is 0-indexed, i.e. the first channel has index 0, the second one index 1 and so on.
        """

        logging.debug(
            "Property NumberOfChannels requested in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )
        return AnalogInChannelProvider_pb2.Get_NumberOfChannels_Responses(
            NumberOfChannels=silaFW_pb2.Integer(value=self.num_channels)
        )

    def Subscribe_Value(self, request, context: grpc.ServicerContext) \
            -> AnalogInChannelProvider_pb2.Subscribe_Value_Responses:
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
            channel = self._get_channel(context.invocation_metadata(), "Property")
            for value in self.implementation.Subscribe_Value(request, channel, context):
                yield value
        except (SiLAError, DeviceError, DecoratorInvalidChannelIndex) as err:
            if isinstance(err, DeviceError):
                err = QmixSDKSiLAError(err)
            elif isinstance(err, DecoratorInvalidChannelIndex):
                err = InvalidChannelIndexError(
                    err.invalid_index,
                    f"The index has to be between 0 and {self.num_channels - 1}."
                )
            err.raise_rpc_error(context=context)


    def Get_FCPAffectedByMetadata_ChannelIndex(self, request, context: grpc.ServicerContext) \
            -> AnalogInChannelProvider_pb2.Get_FCPAffectedByMetadata_ChannelIndex_Responses:
        """
        Requests the unobservable property FCPAffectedByMetadata Channel Index
            Specifies which Features/Commands/Properties of the SiLA server are affected by the Channel Index Metadata.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            AffectedCalls (AffectedCalls): A string containing a list of Fully Qualified Identifiers of Features, Commands and Properties for which the SiLA Client Metadata is expected as part of the respective RPCs.
        """

        logging.debug(
            "Property FCPAffectedByMetadata_ChannelIndex requested in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )
        return AnalogInChannelProvider_pb2.Get_FCPAffectedByMetadata_ChannelIndex_Responses(
            AffectedCalls=[
                silaFW_pb2.String(value="de.cetoni/io/AnalogInChannelProvider/v1/Property/Value"),
            ]
        )

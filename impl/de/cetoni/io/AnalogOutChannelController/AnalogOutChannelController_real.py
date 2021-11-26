"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Analog Out Channel Controller*

:details: AnalogOutChannelController:
    Allows to control one analog output channel of an I/O module

:file:    AnalogOutChannelController_real.py
:authors: Florian Meinicke

:date: (creation)          2020-12-09T09:15:03.175515
:date: (last modification) 2021-07-08T11:44:11.611138

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

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2

from impl.common.errors import SystemNotOperationalError

# import gRPC modules for this feature
from .gRPC import AnalogOutChannelController_pb2 as AnalogOutChannelController_pb2
# from .gRPC import AnalogOutChannelController_pb2_grpc as AnalogOutChannelController_pb2_grpc

# import default arguments
from .AnalogOutChannelController_default_arguments import default_dict

from qmixsdk.qmixanalogio import AnalogOutChannel

from application.system import ApplicationSystem, SystemState


# noinspection PyPep8Naming,PyUnusedLocal
class AnalogOutChannelControllerReal:
    """
    Implementation of the *Analog Out Channel Controller* in *Real* mode
        The SiLA 2 driver for Qmix I/O Devices
    """

    def __init__(self):
        """
        Class initialiser
        """

        self.system = ApplicationSystem()

        logging.debug('Started server in mode: {mode}'.format(mode='Real'))

    def SetOutputValue(self, request, channel: AnalogOutChannel, context: grpc.ServicerContext) \
            -> AnalogOutChannelController_pb2.SetOutputValue_Responses:
        """
        Executes the unobservable command "Set Output Value"
            Set the value of the analog output channel.

        :param request: gRPC request containing the parameters passed:
            request.Value (Value): The value to set.
        :param channel: The channel to operate on
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        if not self.system.state.is_operational():
            raise SystemNotOperationalError('de.cetoni/io/AnalogOutChannelController/v1/Command/SetOutputValue')

        value = request.Value.value
        logging.info(f"Setting output value to {value}")
        channel.write_output(value)

        return AnalogOutChannelController_pb2.SetOutputValue_Responses()

    def Subscribe_Value(self, request, channel: AnalogOutChannel, context: grpc.ServicerContext) \
            -> AnalogOutChannelController_pb2.Subscribe_Value_Responses:
        """
        Requests the observable property Value
            The value of the analog output channel.

        :param request: An empty gRPC request object (properties have no parameters)
        :param channel: The channel to operate on
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            Value (Value): The value of the analog output channel.
        """

        new_value = channel.get_output_value()
        value = new_value + 1 # force sending the first value
        while context.is_active():
            new_value = channel.get_output_value() if self.system.state.is_operational() else 0
            if not math.isclose(new_value, value):
                value = new_value
                yield AnalogOutChannelController_pb2.Subscribe_Value_Responses(
                    Value=silaFW_pb2.Real(value=value)
                )
            time.sleep(0.1) # give client some time to catch up

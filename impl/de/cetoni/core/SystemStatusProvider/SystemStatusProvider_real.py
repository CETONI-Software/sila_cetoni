"""
________________________________________________________________________

:PROJECT: SiLA2_python

*System Status Provider*

:details: SystemStatusProvider:
    Provides information about the overall system, e.g. if the system is operational or not

:file:    SystemStatusProvider_real.py
:authors: Florian Meinicke

:date: (creation)          2021-07-15T09:24:06.645473
:date: (last modification) 2021-07-15T09:24:06.645473

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
from .gRPC import SystemStatusProvider_pb2 as SystemStatusProvider_pb2
# from .gRPC import SystemStatusProvider_pb2_grpc as SystemStatusProvider_pb2_grpc

# import default arguments
from .SystemStatusProvider_default_arguments import default_dict

from application.system import ApplicationSystem, SystemState


# noinspection PyPep8Naming,PyUnusedLocal
class SystemStatusProviderReal:
    """
    Implementation of the *System Status Provider* in *Real* mode
        Provides status information about the overall system
    """

    def __init__(self):
        """Class initialiser"""

        self.system = ApplicationSystem()

        logging.debug('Started server in mode: {mode}'.format(mode='Real'))


    def Subscribe_SystemState(self, request, context: grpc.ServicerContext) \
            -> SystemStatusProvider_pb2.Subscribe_SystemState_Responses:
        """
        Requests the observable property System State
            The state of the system, e.g. if the system is operational or not. 'Operational' means that the system can process Commands and that all Property values are read from the device. 'Stopped' means that the system is unable to process Commands (i.e. all Execution will result in errors) and that Property values are not read from the device and might have outdated values.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            SystemState (System State): The state of the system, e.g. if the system is operational or not. 'Operational' means that the system can process Commands and that all Property values are read from the device. 'Stopped' means that the system is unable to process Commands (i.e. all Execution will result in errors) and that Property values are not read from the device and might have outdated values.
        """

        new_state = self.system.state.value
        state = "" # force sending the first value
        while True:
            new_state = self.system.state.value
            if new_state != state:
                state = new_state
                yield SystemStatusProvider_pb2.Subscribe_SystemState_Responses(
                        SystemState=silaFW_pb2.String(value=state)
                )
            time.sleep(0.1) # give client some time to catch up


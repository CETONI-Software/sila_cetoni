"""
________________________________________________________________________

:PROJECT: SiLA2_python

*Balance Service*

:details: BalanceService:
    Provides an interface to a balance to read its current value and tare the balance if necessary

:file:    BalanceService_real.py
:authors: Florian Meinicke

:date: (creation)          2021-11-24T15:23:15.536557
:date: (last modification) 2021-11-24T15:23:15.536557

.. note:: Code generated by sila2codegenerator 0.3.7

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

# import gRPC modules for this feature
from .gRPC import BalanceService_pb2 as BalanceService_pb2
# from .gRPC import BalanceService_pb2_grpc as BalanceService_pb2_grpc

# import default arguments
from .BalanceService_default_arguments import default_dict

from application.system import ApplicationSystem, SystemState

from device_drivers.balance import SartoriusBalance


# noinspection PyPep8Naming,PyUnusedLocal
class BalanceServiceReal:
    """
    Implementation of the *Balance Service* in *Real* mode
        Allows to control a balance
    """

    def __init__(self, balance: SartoriusBalance = None):
        """Class initialiser"""

        self.balance = balance
        self.system = ApplicationSystem()

        logging.debug('Started server in mode: {mode}'.format(mode='Real'))

    def Tare(self, request, context: grpc.ServicerContext) \
            -> BalanceService_pb2.Tare_Responses:
        """
        Executes the unobservable command "Tare"
            Tare the balance

        :param request: gRPC request containing the parameters passed:
            request.EmptyParameter (Empty Parameter): An empty parameter data type used if no parameter is required.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            request.EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        self.balance.tare()
        return BalanceService_pb2.Tare_Responses()


    def Subscribe_Value(self, request, context: grpc.ServicerContext) \
            -> BalanceService_pb2.Subscribe_Value_Responses:
        """
        Requests the observable property Value
            The current value

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            request.Value (Value): The current value
        """
        new_value = self.balance.value()
        value = new_value + 1 # force sending the first value
        while not self.system.state.shutting_down():
            if self.system.state.is_operational():
                new_value = self.balance.value()
            # consider a value different from the one before if they differ in
            # the first 4 decimal places (which is the precision we get from the
            # balance) to reduce the load of value updates
            if not math.isclose(new_value, value, rel_tol=1.0e-4):
                value = new_value
                yield BalanceService_pb2.Subscribe_Value_Responses(
                    Value=silaFW_pb2.Real(value=value)
                )
        # we add a small delay to give the client a chance to keep up.
            time.sleep(0.1)
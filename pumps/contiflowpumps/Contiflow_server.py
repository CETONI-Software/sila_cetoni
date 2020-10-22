#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: SiLA2_python

*Contiflow*

:details: Contiflow:
    Allows to control a continuous flow pumps that is made up of two syringe pumps

:file:    Contiflow_server.py
:authors: Florian Meinicke

:date: (creation)          2020-10-22T07:15:55.315248
:date: (last modification) 2020-10-22T07:15:55.315248

.. note:: Code generated by sila2codegenerator 0.3.2.dev

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
__version__ = "0.1.0"

import os
import logging
import argparse

# import qmixsdk
from qmixsdk import qmixbus
from qmixsdk import qmixpump

# Import the main SiLA library
from sila2lib.sila_server import SiLA2Server

# Import gRPC libraries of features
from impl.de.cetoni.pumps.contiflowpumps.ContinuousFlowConfigurationService.gRPC import ContinuousFlowConfigurationService_pb2
from impl.de.cetoni.pumps.contiflowpumps.ContinuousFlowConfigurationService.gRPC import ContinuousFlowConfigurationService_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.pumps.contiflowpumps.ContinuousFlowConfigurationService.ContinuousFlowConfigurationService_default_arguments import default_dict as ContinuousFlowConfigurationService_default_dict
from impl.de.cetoni.pumps.contiflowpumps.ContinuousFlowInitializationController.gRPC import ContinuousFlowInitializationController_pb2
from impl.de.cetoni.pumps.contiflowpumps.ContinuousFlowInitializationController.gRPC import ContinuousFlowInitializationController_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.pumps.contiflowpumps.ContinuousFlowInitializationController.ContinuousFlowInitializationController_default_arguments import default_dict as ContinuousFlowInitializationController_default_dict

# Import the servicer modules for each feature
from impl.de.cetoni.pumps.contiflowpumps.ContinuousFlowConfigurationService.ContinuousFlowConfigurationService_servicer import ContinuousFlowConfigurationService
from impl.de.cetoni.pumps.contiflowpumps.ContinuousFlowInitializationController.ContinuousFlowInitializationController_servicer import ContinuousFlowInitializationController

from local_ip import LOCAL_IP

class ContiflowServer(SiLA2Server):
    """
    Allows to control a continuous flow pumps that is made up of two syringe pumps
    """

    def __init__(self, cmd_args, qmix_pump, simulation_mode: bool = True):
        """Class initialiser"""
        super().__init__(
            name=cmd_args.server_name,
            description=cmd_args.description,
            server_type=cmd_args.server_type,
            server_uuid=None,
            version=__version__,
            vendor_url="cetoni.de",
            ip=LOCAL_IP, port=int(cmd_args.port),
            key_file=cmd_args.encryption_key, cert_file=cmd_args.encryption_cert
        )

        logging.info(
            "Starting SiLA2 server with server name: {server_name}".format(
                server_name=cmd_args.server_name
            )
        )

        data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..',
                                 'features', 'de', 'cetoni', 'pumps', 'contiflowpumps')

        # registering features
        #  Register de.cetoni.pumps.contiflowpumps.ContinuousFlowConfigurationService
        self.ContinuousFlowConfigurationService_servicer = \
            ContinuousFlowConfigurationService(
                pump=qmix_pump,
                simulation_mode=self.simulation_mode
            )
        ContinuousFlowConfigurationService_pb2_grpc.add_ContinuousFlowConfigurationServiceServicer_to_server(
            self.ContinuousFlowConfigurationService_servicer,
            self.grpc_server
        )
        self.add_feature(feature_id='ContinuousFlowConfigurationService',
                         servicer=self.ContinuousFlowConfigurationService_servicer,
                         data_path=data_path)
        #  Register de.cetoni.pumps.contiflowpumps.ContinuousFlowInitializationController
        self.ContinuousFlowInitializationController_servicer = \
            ContinuousFlowInitializationController(
                pump=qmix_pump,
                simulation_mode=self.simulation_mode
            )
        ContinuousFlowInitializationController_pb2_grpc.add_ContinuousFlowInitializationControllerServicer_to_server(
            self.ContinuousFlowInitializationController_servicer,
            self.grpc_server
        )
        self.add_feature(feature_id='ContinuousFlowInitializationController',
                         servicer=self.ContinuousFlowInitializationController_servicer,
                         data_path=data_path)

        self.simulation_mode = simulation_mode


def parse_command_line():
    """
    Just looking for commandline arguments
    """
    parser = argparse.ArgumentParser(description="A SiLA2 service: Contiflow")

    # Simple arguments for the server identification
    parser.add_argument('-s', '--server-name', action='store',
                        default="Contiflow", help='start SiLA server with [server-name]')
    parser.add_argument('-t', '--server-type', action='store',
                        default="Unknown Type", help='start SiLA server with [server-type]')
    parser.add_argument('-d', '--description', action='store',
                        default="Allows to control a continuous flow pumps that is made up of two syringe pumps", help='SiLA server description')

    # Encryption
    parser.add_argument('-X', '--encryption', action='store', default=None,
                        help='The name of the private key and certificate file (without extension).')
    parser.add_argument('--encryption-key', action='store', default=None,
                        help='The name of the encryption key (*with* extension). Can be used if key and certificate '
                             'vary or non-standard file extensions are used.')
    parser.add_argument('--encryption-cert', action='store', default=None,
                        help='The name of the encryption certificate (*with* extension). Can be used if key and '
                             'certificate vary or non-standard file extensions are used.')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    parsed_args = parser.parse_args()

    # validate/update some settings
    #   encryption
    if parsed_args.encryption is not None:
        # only overwrite the separate keys if not given manually
        if parsed_args.encryption_key is None:
            parsed_args.encryption_key = parsed_args.encryption + '.key'
        if parsed_args.encryption_cert is None:
            parsed_args.encryption_cert = parsed_args.encryption + '.cert'

    return parsed_args


if __name__ == '__main__':
    # or use logging.ERROR for less output
    logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)

    args = parse_command_line()

    # generate SiLA2Server
    sila_server = ContiflowServer(cmd_args=args, simulation_mode=True)
#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Battery*

:details: Battery:
    A device that is powered by a battery

:file:    Battery_server.py
:authors: Florian Meinicke

:date: (creation)          2021-04-20T09:23:16.458839
:date: (last modification) 2021-04-20T09:23:16.458839

.. note:: Code generated by sila2codegenerator 0.3.6

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

# Import our server base class
from ..core.SystemStatusProvider_server import SystemStatusProviderServer

# Import gRPC libraries of features
from impl.de.cetoni.core.BatteryProvider.gRPC import BatteryProvider_pb2
from impl.de.cetoni.core.BatteryProvider.gRPC import BatteryProvider_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.core.BatteryProvider.BatteryProvider_default_arguments import default_dict as BatteryProvider_default_dict

# Import the servicer modules for each feature
from impl.de.cetoni.core.BatteryProvider.BatteryProvider_servicer import BatteryProvider

from application.application import ApplicationSystem

class BatteryServer(SystemStatusProviderServer):
    """
    A device that is powered by a battery
    """

    def __init__(self, cmd_args, simulation_mode: bool = True):
        """
        Class initialiser

        Registers the BatteryProvider feature if Zero2Go is available
        """
        super().__init__(cmd_args=cmd_args, simulation_mode=simulation_mode)

        self.simulation_mode = simulation_mode

        logging.info(
            "Starting SiLA2 server with server name: {server_name}".format(
                server_name=cmd_args.server_name
            )
        )

        if not ApplicationSystem().device_config.has_battery:
            logging.debug("This device does not have a battery")
            return

        meta_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..',
                                                 'features', 'de', 'cetoni', 'core'))

        # registering features
        #  Register BatteryProvider
        self.BatteryProvider_servicer = BatteryProvider(simulation_mode=self.simulation_mode)
        BatteryProvider_pb2_grpc.add_BatteryProviderServicer_to_server(
            self.BatteryProvider_servicer,
            self.grpc_server
        )
        self.add_feature(feature_id='de.cetoni/core/BatteryProvider/v1',
                         servicer=self.BatteryProvider_servicer,
                         meta_path=meta_path)

def parse_command_line():
    """
    Just looking for commandline arguments
    """
    parser = argparse.ArgumentParser(description="A SiLA2 service: Battery")

    # simple arguments for the server identification
    parser.add_argument('-s', '--server-name', action='store',
                        default="Battery", help='start SiLA server with SiLA server name [server-name]')
    parser.add_argument('-t', '--server-type', action='store',
                        default="Unknown Type", help='start SiLA server with SiLA server type [server-type]')
    parser.add_argument('-d', '--description', action='store',
                        default="A device that is powered by a battery", help='SiLA server description')

    # connection parameters
    parser.add_argument('-i', '--server-ip-address', action='store', default='127.0.0.1',
                        help='SiLA server IP address')
    parser.add_argument('--server-hostname', action='store', default='localhost',
                        help='SiLA server hostname')
    parser.add_argument('-p', '--server-port', action='store', default=50052,
                        help='SiLA server port')

    # encryption
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
    sila_server = BatteryServer(cmd_args=args, simulation_mode=True)
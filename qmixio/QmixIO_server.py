#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: SiLA2_python

*QmixIO*

:details: QmixIO:
    The SiLA 2 driver for Qmix I/O Devices

:file:    QmixIO_server.py
:authors: Florian Meinicke

:date: (creation)          2020-12-08T12:28:28.282760
:date: (last modification) 2020-12-08T12:28:28.282760

.. note:: Code generated by sila2codegenerator 0.2.0

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
from typing import Union

# Import the main SiLA library
from sila2lib.sila_server import SiLA2Server

# Import gRPC libraries of features
from impl.de.cetoni.io.DigitalInChannelProvider.gRPC import DigitalInChannelProvider_pb2
from impl.de.cetoni.io.DigitalInChannelProvider.gRPC import DigitalInChannelProvider_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.io.DigitalInChannelProvider.DigitalInChannelProvider_default_arguments import default_dict as DigitalInChannelProvider_default_dict
from impl.de.cetoni.io.DigitalOutChannelController.gRPC import DigitalOutChannelController_pb2
from impl.de.cetoni.io.DigitalOutChannelController.gRPC import DigitalOutChannelController_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.io.DigitalOutChannelController.DigitalOutChannelController_default_arguments import default_dict as DigitalOutChannelController_default_dict
from impl.de.cetoni.io.AnalogInChannelProvider.gRPC import AnalogInChannelProvider_pb2
from impl.de.cetoni.io.AnalogInChannelProvider.gRPC import AnalogInChannelProvider_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.io.AnalogInChannelProvider.AnalogInChannelProvider_default_arguments import default_dict as DigitalInChannelProvider_default_dict
from impl.de.cetoni.io.AnalogOutChannelController.gRPC import AnalogOutChannelController_pb2
from impl.de.cetoni.io.AnalogOutChannelController.gRPC import AnalogOutChannelController_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.io.AnalogOutChannelController.AnalogOutChannelController_default_arguments import default_dict as AnalogOutChannelController_default_dict

# Import the servicer modules for each feature
from impl.de.cetoni.io.DigitalInChannelProvider.DigitalInChannelProvider_servicer import DigitalInChannelProvider
from impl.de.cetoni.io.DigitalOutChannelController.DigitalOutChannelController_servicer import DigitalOutChannelController
from impl.de.cetoni.io.AnalogInChannelProvider.AnalogInChannelProvider_servicer import AnalogInChannelProvider
from impl.de.cetoni.io.AnalogOutChannelController.AnalogOutChannelController_servicer import AnalogOutChannelController

from qmixsdk.qmixanalogio import AnalogInChannel, AnalogOutChannel
from qmixsdk.qmixdigio import DigitalInChannel, DigitalOutChannel

from local_ip import LOCAL_IP

class QmixIOServer(SiLA2Server):
    """
    The SiLA 2 driver for Qmix I/O Devices
    """

    def __init__(self,
                 cmd_args,
                 io_channel: Union[AnalogInChannel, AnalogOutChannel, DigitalInChannel, DigitalOutChannel],
                 simulation_mode: bool = True
        ):
        """
        Class initialiser

        :param cmd_args: The arguments specified on the command line
        :param io_channel: The I/O channel that this server represents
        :param simulation_mode: Sets whether at initialisation the simulation mode is active or the real mode.
        """
        super().__init__(
            name=cmd_args.server_name, description=cmd_args.description,
            server_type=cmd_args.server_type, server_uuid=None,
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

        meta_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..',
                                 'features', 'de', 'cetoni', 'io')

        # registering features
        if isinstance(io_channel, AnalogInChannel):
            logging.warning(f"{cmd_args.server_name}: SW Scaling: {io_channel.get_scaling_param()}")

            #  Register de.cetoni.io.AnalogInChannelProvider
            self.AnalogInChannelProvider_servicer = AnalogInChannelProvider(
                channel=io_channel,
                simulation_mode=self.simulation_mode
            )
            AnalogInChannelProvider_pb2_grpc.add_AnalogInChannelProviderServicer_to_server(
                self.AnalogInChannelProvider_servicer,
                self.grpc_server
            )
            self.add_feature(feature_id='AnalogInChannelProvider',
                             servicer=self.AnalogInChannelProvider_servicer,
                             data_path=meta_path)
        elif isinstance(io_channel, AnalogOutChannel):
            logging.warning(f"{cmd_args.server_name}: SW Scaling: {io_channel.get_scaling_param()}")

            #  Register de.cetoni.io.AnalogOutChannelController
            self.AnalogOutChannelController_servicer = AnalogOutChannelController(
                channel=io_channel,
                simulation_mode=self.simulation_mode
            )
            AnalogOutChannelController_pb2_grpc.add_AnalogOutChannelControllerServicer_to_server(
                self.AnalogOutChannelController_servicer,
                self.grpc_server
            )
            self.add_feature(feature_id='AnalogOutChannelController',
                             servicer=self.AnalogOutChannelController_servicer,
                             data_path=meta_path)
        elif isinstance(io_channel, DigitalInChannel):
            #  Register de.cetoni.io.DigitalInChannelProvider
            self.DigitalInChannelProvider_servicer = DigitalInChannelProvider(
                channel=io_channel,
                simulation_mode=self.simulation_mode
            )
            DigitalInChannelProvider_pb2_grpc.add_DigitalInChannelProviderServicer_to_server(
                self.DigitalInChannelProvider_servicer,
                self.grpc_server
            )
            self.add_feature(feature_id='DigitalInChannelProvider',
                             servicer=self.DigitalInChannelProvider_servicer,
                             data_path=meta_path)
        elif isinstance(io_channel, DigitalOutChannel):
            #  Register de.cetoni.io.DigitalOutChannelController
            self.DigitalOutChannelController_servicer = DigitalOutChannelController(
                channel=io_channel,
                simulation_mode=self.simulation_mode
            )
            DigitalOutChannelController_pb2_grpc.add_DigitalOutChannelControllerServicer_to_server(
                self.DigitalOutChannelController_servicer,
                self.grpc_server
            )
            self.add_feature(feature_id='DigitalOutChannelController',
                             servicer=self.DigitalOutChannelController_servicer,
                             data_path=meta_path)
        else:
            logging.info(f"Unknown I/O channel type {type(io_channel)}")

        self.simulation_mode = simulation_mode


def parse_command_line():
    """
    Just looking for commandline arguments
    """
    parser = argparse.ArgumentParser(description="A SiLA2 service: QmixIO")

    # Simple arguments for the server identification
    parser.add_argument('-s', '--server-name', action='store',
                        default="QmixIO", help='start SiLA server with [server-name]')
    parser.add_argument('-t', '--server-type', action='store',
                        default="Unknown Type", help='start SiLA server with [server-type]')
    parser.add_argument('-d', '--description', action='store',
                        default="The SiLA 2 driver for Qmix I/O Devices", help='SiLA server description')

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
    sila_server = QmixIOServer(cmd_args=args, simulation_mode=True)

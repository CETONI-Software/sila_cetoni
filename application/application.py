"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Application*

:details: Application:
    The main application class containing all logic of the sila_cetoni.py

:file:    application.py
:authors: Florian Meinicke

:date: (creation)          2021-07-19
:date: (last modification) 2021-07-15

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

import os
import sys
import time
import logging
import argparse
from typing import List
from OpenSSL import crypto

from sila2.server import SilaServer

from . import CETONI_SDK_PATH
# adjust PATH variable to point to the SDK
sys.path.append(CETONI_SDK_PATH)
sys.path.append(os.path.join(CETONI_SDK_PATH, "lib", "python"))

# only used for type hinting
from qmixsdk import qmixpump

from .system import ApplicationSystem
from .singleton import Singleton

from util.local_ip import LOCAL_IP

DEFAULT_BASE_PORT = 50052

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Application(metaclass=Singleton):
    """
    Encompasses the main application logic
    """

    system: ApplicationSystem

    key_cert_path: str
    base_port: int
    servers: List[SilaServer]

    def __init__(self, device_config_path: str = "",
                 base_port: int = DEFAULT_BASE_PORT):

        self.system = ApplicationSystem(device_config_path)
        self._generate_self_signed_cert()

        self.base_port = base_port

    def _generate_self_signed_cert(self):
        """
        Generates a self-signed SSL key/certificate pair on the fly
        """

        self.key_cert_path = os.path.join(os.path.dirname(__file__), '..', '.ssl', 'sila_cetoni.{}')
        os.makedirs(os.path.dirname(self.key_cert_path), exist_ok=True)

        private_key = crypto.PKey()
        private_key.generate_key(crypto.TYPE_RSA, 4096)

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = 'DE'
        cert.get_subject().ST = 'TH'
        cert.get_subject().O = 'CETONI'
        cert.get_subject().CN = 'SiLA2'
        cert.set_serial_number(1)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(365*24*60*60)
        cert.set_issuer(cert.get_subject())

        cert.set_pubkey(private_key)
        cert.sign(private_key, 'sha512') # signing certificate with public key

        # writing key / cert pair
        with open(self.key_cert_path.format('crt'), "wt") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
        with open(self.key_cert_path.format('key'), "wt") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, private_key).decode("utf-8"))

    def run(self):
        """
        Run the main application loop

        Starts the whole system (i.e. all devices) and all SiLA 2 servers
        Runs until Ctrl-C is pressed on the command line or `stop()` has been called
        """
        self.system.start()
        
        logging.debug("Creating SiLA 2 servers...")
        self.servers = self.create_servers()

        if not self.servers:
            logging.info("No SiLA Servers to run")
            return

        self.start_servers()

        print("Press Ctrl-C to stop...", flush=True)
        try:
            while not self.system.state.shutting_down():
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            print()
            self.stop()

    def stop(self):
        """
        Stops the application

        Shuts down all SiLA 2 servers and stops the whole system
        """
        self.stop_servers()
        self.system.stop()

    def start_servers(self):
        """
        Starts all SiLA 2 servers
        """
        logging.debug("Starting SiLA 2 servers...")
        for server in self.servers:
            port = self.base_port - 1
            server.start_insecure(LOCAL_IP, port)
        logging.info("All servers started!")

    def stop_servers(self):
        """
        Stops all SiLA 2 servers
        """
        logging.debug("Shutting down servers...")
        for server in self.servers:
            server.stop()
        logging.info("Done!")

    def create_servers(self):
        """
        Creates a corresponding SiLA 2 server for every device connected to the bus
        """

        servers = []
        # common args for all servers
        server_type="TestServer"
        encryption_key=self.key_cert_path.format('key')
        encryption_cert=self.key_cert_path.format('crt')

        #---------------------------------------------------------------------
        # pumps
        for pump in self.system.pumps:
            # server_port += 1
            server_name = pump.name.replace("_", " ")

            if isinstance(pump, qmixpump.ContiFlowPump):
                from new.pumps.contiflowpumps.contiflowpump_service.server import Server
                server = Server(pump, server_name, server_type) #, server_uuid=)
            else:
                from new.pumps.syringepumps.syringepump_service import Server
                server = Server(pump, pump.valves[0], pump.io_channels, server_name, server_type) #, server_uuid=)
            servers += [server]

        #---------------------------------------------------------------------
        # axis systems
        for axis_system in self.system.axis_systems:
            # server_port += 1
            server_name = axis_system.name.replace("_", " ")

            from new.motioncontrol.axis_service.server import Server
            server = Server(axis_system, axis_system.io_channels, server_name, server_type) #, server_uuid=)
            servers += [server]

        #---------------------------------------------------------------------
        # valves
        for valve_device in self.system.valves:
            # server_port += 1
            server_name = valve_device.name.replace("_", " ")

            from new.valves.valve_service.server import Server
            server = Server(valve_device.valves, server_name, server_type) #, server_uuid=)
            servers += [server]

        #---------------------------------------------------------------------
        # controller
        for controller_device in self.system.controllers:
            # server_port += 1
            server_name = controller_device.name.replace("_", " ")

            from new.controllers.control_loop_service.server import Server
            server = Server(controller_device.controller_channels, server_name, server_type) #, server_uuid=)
            servers += [server]

        #---------------------------------------------------------------------
        # I/O
        for io_device in self.system.io_devices:
            # server_port += 1
            server_name = io_device.name.replace("_", " ")

            from new.io.io_service.server import Server
            server = Server(io_device.io_channels, server_name, server_type) #, server_uuid=)
            servers += [server]

        #---------------------------------------------------------------------
        # balance
        for balance in self.system.balances:
            # server_port += 1
            server_name = balance.name.replace("_", " ")

            from new.balance.balance_service.server import Server
            server = Server(balance.device, server_name, server_type) #, server_uuid=)
            servers += [server]

        return servers

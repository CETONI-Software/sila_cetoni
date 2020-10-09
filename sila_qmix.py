#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: sila_qmix

*SiLA Qmix*

:details: SiLA Qmix:
    A wrapper script that starts as many individual SiLA2 servers as there are devices in the given configuration.

:file:    sila_qmix.py
:authors: Florian Meinicke

:date: (creation)          2020-10-08
:date: (last modification) 2020-10-08

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

__version__ = "0.0.1"

import time
import argparse
import logging
try:
    import coloredlogs
except ModuleNotFoundError:
    print("Cannot find coloredlogs! Please install coloredlogs, if you'd like to have nicer logging output:")
    print("`pip install coloredlogs`")
from typing import List

# import Qmix servers
from pump.impl.neMESYS_server import neMESYSServer
from controller.QmixControl_server import QmixControlServer

# import qmixsdk
from qmixsdk import qmixbus, qmixpump, qmixcontroller

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def open_bus(config_path: str) -> qmixbus.Bus:
    """
    Opens the given device config and starts the bus communication

        :param config_path: Path to a valid Qmix device configuration
        :type config_path: str
        :return: The bus that was just opened
        :rtype: qmixbus.Bus
    """
    logging.debug("Opening bus")
    bus = qmixbus.Bus()
    try:
        bus.open(config_path, 0)
    except qmixbus.DeviceError as err:
        logging.error("could not open the bus communication: %s", err)
        pass
    else:
        return bus

def get_availabe_pumps() -> List[qmixpump.Pump]:
    """
    Looks up all pumps from the current configuration and constructs a list of
    all found pumps

        :return: A list of all found pumps connected to the bus
        :rtype: [qmixpump.Pump]
    """
    pump_count = qmixpump.Pump.get_no_of_pumps()
    logging.debug("Number of pumps: %s", pump_count)

    pumps = []

    for i in range(pump_count):
        pump = qmixpump.Pump()
        pump.lookup_by_device_index(i)
        logging.debug("Found pump %d named %s", i, pump.get_device_name())
        pumps.append(pump)

    return pumps

def enable_pumps(pumps: List[qmixpump.Pump]):
    """
    Enables all given pumps

        :param pumps: A list of pumps to enable
        :type pumps: list(qmixpump.Pump)
    """
    for pump in pumps:
        if pump.is_in_fault_state():
            pump.clear_fault()
        if not pump.is_enabled():
            pump.enable(True)

def get_availabe_controllers() -> List[qmixcontroller.ControllerChannel]:
    """
    Looks up all controller channels from the current configuration and constructs
    a list of all found channels

        :return: A list of all found controller channels connected to the bus
        :rtype: [qmixcontroller.ControllerChannel]
    """
    channel_count = qmixcontroller.ControllerChannel.get_no_of_channels()
    logging.debug("Number of controller channels: %s", channel_count)

    channels = []

    for i in range(channel_count):
        channel = qmixcontroller.ControllerChannel()
        channel.lookup_channel_by_index(i)
        logging.debug("Found channel %d named %s", i, channel.get_name())
        channels.append(channel)

    return channels

def stop_and_close_bus(bus: qmixbus.Bus):
    """
    Stops and closes the bus communication

        :param bus: The bus to stop and close
        :type bus: qmixbus.Bus
    """
    logging.debug("Closing bus...")
    bus.stop()
    bus.close()

def parse_command_line():
    """
    Just looking for command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Launches as many SiLA 2 servers as there are Qmix devices in the configuration")
    parser.add_argument('config_path', metavar='configuration_path', type=str,
                        help="""a path to a valid Qmix configuration folder
                             (If you don't have a configuration yet,
                             create one with the QmixElements software first.)""")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    return parser.parse_args()


if __name__ == '__main__':
    logging_level = logging.DEBUG # or use logging.ERROR for less output
    try:
        coloredlogs.install(fmt='%(asctime)s %(levelname)s| %(module)s.%(funcName)s: %(message)s',
                            level=logging_level)
    except NameError:
        logging.basicConfig(format='%(levelname)s| %(module)s.%(funcName)s: %(message)s', level=logging_level)

    parsed_args = parse_command_line()

    logging.debug("Starting bus...")
    bus = open_bus(parsed_args.config_path)
    logging.debug("Looking up devices...")
    pumps = get_availabe_pumps()
    controllers = get_availabe_controllers()
    # TODO get more devices ...
    bus.start()
    enable_pumps(pumps)

    # common args for all servers
    args = argparse.Namespace(
        port=50051, # base port
        server_type="TestServer",
        encryption_key=None,
        encryption_cert=None
    )
    # generate SiLA2Server processes
    servers = []
    for pump in pumps:
        args.port = args.port + len(servers)
        args.server_name = pump.get_device_name().replace("_", " ")
        args.description = "Allows to control a neMESYS syringe pump"

        server = neMESYSServer(cmd_args=args, qmix_pump=pump, simulation_mode=False)
        server.run(block=False)
        servers += [server]
    for channel in controllers:
        args.port = args.port + len(servers)
        args.server_name = channel.get_name().replace("_", " ")
        args.description = "Allows to control a Qmix Controller Channel"

        server = QmixControlServer(cmd_args=args, qmix_controller=channel, simulation_mode=False)
        server.run(block=False)
        servers += [server]

    logging.info("All servers started!")
    print("Press Ctrl-C to stop...")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print()
        logging.debug("shutting down servers...")
        for server in servers:
            server.stop_grpc_server()

    stop_and_close_bus(bus)

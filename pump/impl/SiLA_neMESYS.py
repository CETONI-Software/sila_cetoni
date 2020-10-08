"""
________________________________________________________________________

:PROJECT: SiLA2_neMESYS

*SiLA neMESYS Server*

:details: SiLA neMESYS:
    A wrapper script that starts as many individual SiLA2 servers as there are devices in the given configuration.

:file:    SiLA_neMESYS.py
:authors: Florian Meinicke

:date: (creation)          2019-07-17
:date: (last modification) 2020-05-07

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

# import neMESYS server
from neMESYS_server import neMESYSServer

# import qmixsdk
from qmixsdk import qmixbus
from qmixsdk import qmixpump

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

def get_availabe_pumps() -> [qmixpump.Pump]:
    """
    Looks up all pumps from the current configuration and constructs a list of
    all found pumps

        :return: A list of all found pumps connected to the bus
        :rtype: [qmixpump.Pump]
    """
    logging.debug("Looking up devices...")

    pumpcount = qmixpump.Pump.get_no_of_pumps()
    logging.debug("Number of pumps: %s", pumpcount)

    pumps = []

    for i in range(pumpcount):
        pump = qmixpump.Pump()
        pump.lookup_by_device_index(i)
        logging.debug("Found pump %d named %s", i, pump.get_device_name())
        pumps.append(pump)

    return pumps

def start_bus_and_enable_pumps(bus: qmixbus.Bus, pumps: [qmixpump.Pump]):
    """
    Starts the bus communication and enables all given pumps

        :param bus: The bus to start
        :type bus: qmixbus.Bus
        :param pumps: A list of pumps to enable
        :type pumps: list(qmixpump.Pump)
    """
    bus.start()

    for pump in pumps:
        if pump.is_in_fault_state():
            pump.clear_fault()
        if not pump.is_enabled():
            pump.enable(True)

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
    Just looking for commandline arguments
    """
    parser = argparse.ArgumentParser(
        description="Launches as many SiLA2 neMESYS servers as there are pumps in the configuration")
    parser.add_argument('config_path', metavar='configuration_path', type=str,
                        help="""a path to a valid Qmix configuration folder
                             (If you don't have a configuration yet,
                             create one with the QmixElements software first.)""")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    return parser.parse_args()


if __name__ == '__main__':
    logging_level = logging.INFO # or use logging.ERROR for less output
    try:
        coloredlogs.install(fmt='%(asctime)s %(levelname)s| %(module)s.%(funcName)s: %(message)s',
                            level=logging_level)
    except NameError:
        logging.basicConfig(format='%(levelname)s| %(module)s.%(funcName)s: %(message)s', level=logging_level)

    parsed_args = parse_command_line()

    bus = open_bus(parsed_args.config_path)
    pumps = get_availabe_pumps()
    start_bus_and_enable_pumps(bus, pumps)

    # generate SiLA2Server processes
    BASE_PORT = 50051
    servers = []
    for pump in pumps:
        args = argparse.Namespace(
            port=BASE_PORT + pumps.index(pump),
            server_name=pump.get_device_name().replace("_", " "),
            server_type="TestServer",
            description="This is a sample service for controlling neMESYS syringe pumps via SiLA2",
            encryption_key=None,
            encryption_cert=None
        )
        server = neMESYSServer(cmd_args=args, qmix_pump=pump, simulation_mode=False)
        server.run(block=False)
        servers += [server]

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print()
        logging.debug("shutting down servers...")
        for server in servers:
            server.stop_grpc_server()

        stop_and_close_bus(bus)

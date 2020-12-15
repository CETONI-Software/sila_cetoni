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

import os
import sys
import time
import argparse
import logging
try:
    import coloredlogs
except ModuleNotFoundError:
    print("Cannot find coloredlogs! Please install coloredlogs, if you'd like to have nicer logging output:")
    print("`pip install coloredlogs`")
from typing import Dict, List, Union

from lxml import etree, objectify

# adjust PATH to point to QmixSDK
sys.path.append("C:/QmixSDK/lib/python")

# import Qmix servers
from pumps.syringepumps.neMESYS_server import neMESYSServer
from pumps.contiflowpumps.Contiflow_server import ContiflowServer
from controllers.QmixControl_server import QmixControlServer
from qmixio.QmixIO_server import QmixIOServer
from motioncontrol.MotionControl_server import MotionControlServer

# import qmixsdk
from qmixsdk import qmixbus, qmixpump, qmixcontroller, qmixanalogio, qmixdigio, qmixmotion

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

#-----------------------------------------------------------------------------
# Devices
def parse_device_config(config_path: str) -> List[str]:
    """
    Parses the device configuration files located in the folder given by the config_path
    parameter.

        :param config_path: Path to a valid Qmix device configuration
        :return: A list with the names of all devices
        :rtype: List[str]
    """
    logging.debug("Parsing device configuration")
    device_list: List[str] = []

    tree: etree.ElementTree
    with open(os.path.join(config_path, 'device_properties.xml')) as f:
        tree = objectify.parse(f)
    root = tree.getroot()
    for plugin in root.Core.PluginList.iterchildren():
        if plugin.text in ('qmixelements', 'scriptingsystem', 'labbcanservice',
                           'canopentools', 'qmixdevices', 'datalogger'):
            # these files are the only ones with UTF-8 w/ BOM which leads to an error
            # while parsing the file; since we don't need it anyway we can skip it
            continue

        logging.debug(f"Parsing configuration for {plugin.text} plugin")
        # we need to create a new parser that parses our 'broken' XML files
        # (they are regarded as 'broken' because they contain multiple root tags)
        parser = objectify.makeparser(recover=True)
        with open(os.path.join(config_path, plugin.text + '.xml')) as f:
            plugin_tree: etree.ElementTree = objectify.parse(f, parser)
            plugin_root = plugin_tree.getroot()
            try:
                for device in plugin_root.labbCAN.DeviceList.iterchildren():
                    device_list += [device.get('Name')]
            except AttributeError:
                pass

    # Filter the device_list as it contains more than the actual physical modules that we're after
    def unneeded_devices(device_name):
        for e in ('Epos', 'Valve'):
            if e in device_name:
                return False
        return True

    # Some devices are represented as '<device>_ChipF40' but we only want it to be '<device>'
    device_list = [device.split('_ChipF40', 1)[0] for device in filter(unneeded_devices, device_list)]

    logging.debug(f"Found the following devices: {device_list}")

    return device_list

def devices_to_channels(devices: List[str], channels: List) -> Dict:
    """
    Constructs the relationship device -> channel(s)

        :param devices: A list of all devices connected to the bus
        :param channels: A list of channels that should be mapped to their corresponding devices
        :return: A dictionary of all devices with their corresponding channels
        :rtype: Dict
    """
    device_to_channels = {}

    for channel in channels:
        for device in devices:
            channel_name = channel.get_name()
            if device.rsplit('_Pump', 1)[0] in channel_name:
                logging.debug(f"Channel {channel_name} belongs to device {device}")
                if device in device_to_channels:
                    device_to_channels[device] += [channel]
                else:
                    device_to_channels[device] = [channel]

    return device_to_channels

#-----------------------------------------------------------------------------
# Bus
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

def stop_and_close_bus(bus: qmixbus.Bus):
    """
    Stops and closes the bus communication

        :param bus: The bus to stop and close
        :type bus: qmixbus.Bus
    """
    logging.debug("Closing bus...")
    bus.stop()
    bus.close()

#-----------------------------------------------------------------------------
# Pumps
def get_availabe_pumps() -> List[qmixpump.Pump]:
    """
    Looks up all pumps from the current configuration and constructs a list of
    all found pumps

        :return: A list of all found pumps connected to the bus
        :rtype: List[qmixpump.Pump]
    """
    pump_count = qmixpump.Pump.get_no_of_pumps()
    logging.debug("Number of pumps: %s", pump_count)

    pumps = []

    for i in range(pump_count):
        pump = qmixpump.Pump()
        pump.lookup_by_device_index(i)
        logging.debug("Found pump %d named %s", i, pump.get_device_name())
        try:
            pump.get_device_property(qmixpump.ContiFlowProperty.SWITCHING_MODE)
            pump = qmixpump.ContiFlowPump(pump.handle)
            logging.debug("Pump %s i contiflow pump", pump.get_device_name())
        except qmixbus.DeviceError as err:
            pass
        pumps.append(pump)

    return pumps

def enable_pumps(pumps: List[qmixpump.Pump]):
    """
    Enables all given pumps

        :param pumps: A list of pumps to enable
        :type pumps: List[qmixpump.Pump]
    """
    for pump in pumps:
        if pump.is_in_fault_state():
            pump.clear_fault()
        if not pump.is_enabled():
            pump.enable(True)

#-----------------------------------------------------------------------------
# Controllers
def get_availabe_controllers(devices: List[str]) -> List[qmixcontroller.ControllerChannel]:
    """
    Looks up all controller channels from the current configuration and maps them
    to their corresponding device

        :param devices: A list of all devices connected to the bus
        :return: A dictionary of all devices with their corresponding controller channels
        :rtype: Dict[str, qmixcontroller.ControllerChannel]
    """
    channel_count = qmixcontroller.ControllerChannel.get_no_of_channels()
    logging.debug("Number of controller channels: %s", channel_count)

    channels = []

    for i in range(channel_count):
        channel = qmixcontroller.ControllerChannel()
        channel.lookup_channel_by_index(i)
        logging.debug("Found channel %d named %s", i, channel.get_name())
        channels.append(channel)

    return devices_to_channels(devices, channels)


#-----------------------------------------------------------------------------
# I/O
def get_availabe_io_channels(devices: List[str]) \
    -> Dict[str, Union[qmixanalogio.AnalogChannel, qmixdigio.DigitalChannel]]:
    """
    Looks up all analog and digital I/O channels from the current configuration
    and maps them to their corresponding device

        :param devices: A list of all devices connected to the bus
        :return: A dictionary of all devices with their corresponding I/O channels
        :rtype: Dict[str, Union[qmixanalogio.AnalogChannel, qmixdigio.DigitalChannel]]
    """

    channels = []

    for (description, ChannelType) in {
        'analog in': qmixanalogio.AnalogInChannel,
        'analog out': qmixanalogio.AnalogOutChannel,
        'digital in': qmixdigio.DigitalInChannel,
        'digital out': qmixdigio.DigitalOutChannel}.items():

        channel_count = ChannelType.get_no_of_channels()
        logging.debug("Number of %s channels: %s", description, channel_count)

        for i in range(channel_count):
            channel = ChannelType()
            channel.lookup_channel_by_index(i)
            channel_name = channel.get_name()
            logging.debug("Found %s channel %d named %s", description, i, channel_name)
            channels.append(channel)

    return devices_to_channels(devices, channels)

#-----------------------------------------------------------------------------
# Motion Control
def get_availabe_axis_systems() -> List[qmixmotion.AxisSystem]:
    """
    Looks up all axis systems connected to the bus

        :param devices: A list of all devices connected to the bus
        :return: A dictionary of all devices with their corresponding I/O channels
        :rtype: Dict[str, Union[qmixanalogio.AnalogChannel, qmixdigio.DigitalChannel]]
    """

    system_count = qmixmotion.AxisSystem.get_axis_system_count()
    logging.debug("Number of axis systems: %s", system_count)

    systems = []

    for i in range(system_count):
        system = qmixmotion.AxisSystem()
        system.lookup_by_device_index(i)
        logging.debug("Found axis system %d named %s", i, system.get_device_name())
        systems.append(system)

    return systems

#-----------------------------------------------------------------------------
# main program
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
        coloredlogs.install(fmt='%(asctime)s %(levelname)-8s| %(module)s.%(funcName)s: %(message)s',
                            level=logging_level)
    except NameError:
        logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging_level)

    parsed_args = parse_command_line()

    qmix_devices = parse_device_config(parsed_args.config_path)

    logging.debug("Starting bus...")
    bus = open_bus(parsed_args.config_path)
    logging.debug("Looking up devices...")
    pumps = get_availabe_pumps()
    device_to_controllers = get_availabe_controllers(qmix_devices)
    device_to_io_channels = get_availabe_io_channels(qmix_devices)
    axis_systems = get_availabe_axis_systems()
    # TODO get more devices ...
    bus.start()
    enable_pumps(pumps)
    [axis_system.enable(True) for axis_system in axis_systems]

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
        args.port += 1
        pump_name = pump.get_device_name()
        args.server_name = pump_name.replace("_", " ")
        args.description = "Allows to control a {contiflow_descr} neMESYS syringe pump".format(
            contiflow_descr="contiflow pump made up of two" if isinstance(pump, qmixpump.ContiFlowPump) else ""
        )

        PumpServer = ContiflowServer if isinstance(pump, qmixpump.ContiFlowPump) else neMESYSServer

        # a pump can have built in I/O channels
        io_channels = []
        if pump_name in device_to_io_channels:
            io_channels = device_to_io_channels[pump_name]
            del device_to_io_channels[pump_name]

        server = PumpServer(cmd_args=args, qmix_pump=pump, io_channels=io_channels, simulation_mode=False)
        server.run(block=False)
        servers += [server]

    for device, channels in device_to_controllers.items():
        args.port += 1
        args.server_name = device.replace("_", " ")
        args.description = "Allows to control Qmix Controller Channels"
        server = QmixControlServer(cmd_args=args, controller_channels=channels, simulation_mode=False)
        server.run(block=False)
        servers += [server]

    for device, channels in device_to_io_channels.items():
        args.port += 1
        args.server_name = device.replace("_", " ")
        args.description = "Allows to control Qmix I/O Channels"
        server = QmixIOServer(cmd_args=args, io_channels=channels, simulation_mode=False)
        server.run(block=False)
        servers += [server]

    for system in axis_systems:
        args.port += 1
        system_name = system.get_device_name()
        args.server_name = system_name.replace("_", " ")
        args.description = "Allows to control motion systems like axis systems"

        # an axis system can have built in I/O channels
        io_channels = []
        if system_name in device_to_io_channels:
            io_channels = device_to_io_channels[system_name]
            del device_to_io_channels[system_name]

        server = MotionControlServer(cmd_args=args, axis_system=system, io_channels=io_channels, simulation_mode=False)
        server.run(block=False)
        servers += [server]

    logging.info("All servers started!")
    print("Press Ctrl-C to stop...")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print()
        logging.debug("Shutting down servers...")
        for server in servers:
            server.stop_grpc_server()

    stop_and_close_bus(bus)

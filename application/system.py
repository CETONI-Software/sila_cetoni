"""
________________________________________________________________________

:PROJECT: sila_cetoni

*System*

:details: System:
    The whole application system representing all physical devices

:file:    system.py
:authors: Florian Meinicke

:date: (creation)          2021-07-19
:date: (last modification) 2021-07-19

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
import threading
from typing import List

from enum import Enum

# import qmixsdk
from qmixsdk import qmixbus, qmixpump, qmixcontroller, qmixanalogio, qmixdigio, qmixmotion, qmixvalve

from .device import DeviceConfiguration, Device, PumpDevice, AxisSystemDevice, \
                    ValveDevice, ControllerDevice, IODevice

from .singleton import Singleton

from . import CETONI_SDK_PATH

class SystemState(Enum):
    """
    The state of the overall application system
    """
    OPERATIONAL = "Operational"
    STOPPED = "Stopped"
    SHUTDOWN = "Shutting Down"

    def is_operational(self):
        return self.value == self.OPERATIONAL.value

    def is_stopped(self):
        return self.value == self.STOPPED.value

    def shutting_down(self):
        return self.value == self.SHUTDOWN.value


class ApplicationSystem(metaclass=Singleton):
    """
    The whole application system containing all devices and all configuration
    """

    device_config: DeviceConfiguration
    bus: qmixbus.Bus
    monitoring_thread: threading.Thread

    pumps: List[PumpDevice]
    axis_systems: List[AxisSystemDevice]
    valves: List[ValveDevice]
    controllers: List[ControllerDevice]
    io_devices: List[IODevice]

    state: SystemState

    MAX_SECONDS_WITHOUT_BATTERY = 20

    def __init__(self, device_config_path: str = ""):
        if not device_config_path:
            return

        self.device_config = DeviceConfiguration(device_config_path)

        self.bus = qmixbus.Bus()
        self.open_bus()

        self.controller_devices = []
        self.io_devices = []
        self.valve_devices = []

        logging.debug("Looking up devices...")
        # The order is important here! Many devices have I/O channels but are not
        # pure I/O devices (similarly, pumps might have a valve but they're not a
        # valve device). That's why valves have to be detected after pumps and I/O
        # devices have to be detected last (since then we can guarantee that there
        # is no possibility for an I/O channel to belong to an I/O device).
        self.pumps = self.get_availabe_pumps()
        self.axis_systems = self.get_availabe_axis_systems()
        self.valves = self.get_availabe_valves()
        self.controller_devices = self.get_availabe_controllers()
        self.io_devices = self.get_availabe_io_channels()

        logging.debug(f"Pumps: {repr(self.pumps)}")
        logging.debug(f"axis: {repr(self.axis_systems)}")
        logging.debug(f"valve devices: {repr(self.valves)}")
        logging.debug(f"controller devices: {repr(self.controller_devices)}")
        logging.debug(f"io devices: {repr(self.io_devices)}")

        self.state = SystemState.OPERATIONAL

    def start(self):
        """
        Starts the CAN bus communications and the bus monitoring and enables devices
        """
        self.start_bus_and_enable_devices()
        self._start_bus_monitoring()

    def stop(self):
        """
        Stops the CAN bus monitoring and the bus communication
        """
        logging.debug("Stopping application system...")
        self.state = SystemState.SHUTDOWN
        self.stop_and_close_bus()

    def shutdown(self):
        """
        Stops the application and shuts down the operating system if we are
        battery powered otherwise it only stops the application
        """
        self.stop()
        if self.device_config.has_battery:
            logging.debug("Shutting down...")
            os.system("sudo shutdown now")

    def _start_bus_monitoring(self):
        """
        Starts monitoring the CAN bus for events (esp. emergency and error events)
        """
        self.monitoring_thread = threading.Thread(target=self.monitor_events)
        self.monitoring_thread.start()

    #-------------------------------------------------------------------------
    # Bus
    def open_bus(self):
        """
        Opens the given device config and starts the bus communication
        """
        logging.debug("Opening bus...")
        try:
            # If we're executed through python.exe the application dir is the
            # directory where python.exe is located. In order for the SDK to find
            # all plugins, nonetheless, we need to give it it's expected plugin
            # path.
            self.bus.open(self.device_config.path,
                          os.path.join(CETONI_SDK_PATH, 'plugins', 'labbcan'))
        except qmixbus.DeviceError as err:
            logging.error("Could not open the bus communication: %s", err)
            sys.exit(1)

    def start_bus_and_enable_devices(self):
        """
        Starts the bus communication and enables all devices
        """
        logging.debug("Starting bus and enabling devices...")
        self.bus.start()
        self.enable_pumps()
        self.enable_axis_systems()

    def stop_and_close_bus(self):
        """
        Stops and closes the bus communication
        """
        logging.debug("Closing bus...")
        self.bus.stop()
        self.bus.close()

    def monitor_events(self):
        """
        Runs an infinite loop that polls the bus for any events.

        If an emergency event is received that suggests that the controller was turned
        off (i.e. DC link under-voltage and a heartbeat error) all SiLA servers will
        be stopped.
        If a "heartbeat error resolved" event is received after the controller was turned
        off it is interpreted to mean that the controller is up and running again and
        the SiLA servers are attempted to start.
        """

        DC_LINK_UNDER_VOLTAGE = 0x3220

        def is_dc_link_under_voltage_event(event: qmixbus.Event):
            return event.event_id == qmixbus.EventId.device_emergency.value \
                and event.data[0] == DC_LINK_UNDER_VOLTAGE

        def is_heartbeat_err_occurred_event(event: qmixbus.Event):
            return event.event_id == qmixbus.EventId.device_guard.value \
                and event.data[0] == qmixbus.GuardEventId.heartbeat_err_occurred.value

        def is_heartbeat_err_resolved_event(event: qmixbus.Event):
            return event.event_id == qmixbus.EventId.device_guard.value \
                and event.data[0] == qmixbus.GuardEventId.heartbeat_err_resolved.value

        seconds_stopped = 0
        while not self.state.shutting_down():
            time.sleep(1)

            event = self.bus.read_event()
            if not event.is_valid():
                continue
            logging.debug(f"event id: {event.event_id}, device: {event.device}, "
                          f"data: {event.data}, message: {event.string}")

            if self.state.is_operational() and (is_dc_link_under_voltage_event(event) \
                or is_heartbeat_err_occurred_event(event)):
                self.state = SystemState.STOPPED
                logging.debug("System entered 'Stopped' state")

            if self.device_config.has_battery and self.state.is_stopped():
                seconds_stopped += 1

            if seconds_stopped > self.MAX_SECONDS_WITHOUT_BATTERY:
                self.shutdown()

            if self.state.is_stopped() and is_heartbeat_err_resolved_event(event):
                self.state = SystemState.OPERATIONAL
                logging.debug("System entered 'Operational' state")
                for device in self.device_config.devices:
                    device.set_operational()

    #-------------------------------------------------------------------------
    # Pumps
    def get_availabe_pumps(self) -> List[PumpDevice]:
        """
        Looks up all pumps from the current configuration and constructs a list of
        all found pumps

        :return: A list of all found pumps
        """
        pump_count = qmixpump.Pump.get_no_of_pumps()
        logging.debug("Number of pumps: %s", pump_count)

        pumps = []

        for i in range(pump_count):
            pump = qmixpump.Pump()
            pump.lookup_by_device_index(i)
            pump_name = pump.get_device_name()
            logging.debug("Found pump %d named %s", i, pump_name)
            try:
                pump.get_device_property(qmixpump.ContiFlowProperty.SWITCHING_MODE)
                pump = qmixpump.ContiFlowPump(pump.handle)
                logging.debug("Pump %s is contiflow pump", pump_name)
            except qmixbus.DeviceError:
                pass
            pump_device = self.device_config.device_by_name(pump_name)
            PumpDevice.convert_to_class(pump_device, handle=pump.handle)
            pumps += [pump_device]

        return pumps

    def enable_pumps(self):
        """
        Enables all pumps
        """
        for pump in self.pumps:
            if pump.is_in_fault_state():
                pump.clear_fault()
            if not pump.is_enabled():
                pump.enable(True)

    #-------------------------------------------------------------------------
    # Motion Control
    def get_availabe_axis_systems(self) -> List[AxisSystemDevice]:
        """
        Looks up all axis systems connected to the bus

        :return: A list of all axis systems
        """

        system_count = qmixmotion.AxisSystem.get_axis_system_count()
        logging.debug("Number of axis systems: %s", system_count)

        axis_systems = []

        for i in range(system_count):
            axis_system = qmixmotion.AxisSystem()
            axis_system.lookup_by_device_index(i)
            axis_system_name = axis_system.get_device_name()
            logging.debug("Found axis system %d named %s", i, axis_system.get_device_name())
            axis_system_device = self.device_config.device_by_name(axis_system_name)
            AxisSystemDevice.convert_to_class(axis_system_device, handle=axis_system.handle)
            axis_systems += [axis_system_device]

        return axis_systems

    def enable_axis_systems(self):
        """
        Enables all axis systems
        """
        for axis_system in self.axis_systems:
            axis_system.enable(True)

    #-------------------------------------------------------------------------
    # Valves
    def get_availabe_valves(self) -> List[ValveDevice]:
        """
        Looks up all valves from the current configuration and maps them to their
        corresponding device

        :return: A list of all valves
        """

        valve_count = qmixvalve.Valve.get_no_of_valves()
        logging.debug("Number of valves: %s", valve_count)

        valves = []

        for i in range(valve_count):
            valve = qmixvalve.Valve()
            valve.lookup_by_device_index(i)
            try:
                valve_name = valve.get_device_name()
            except OSError:
                # When there are contiflow pumps in the config the corresponding
                # valves from the original syringe pumps are duplicated internally.
                # I.e. with one contiflow pump made up of two low pressure pumps
                # with their corresponding valves the total number of valves is
                # 4 despite of the actual 2 physical valves available. This leads
                # to an access violation error inside QmixSDK in case the device
                # name of one of the non-existent contiflow valves is requested.
                # We can fortunately mitigate this with this try-except here.
                continue
            logging.debug("Found valve %d named %s", i, valve_name)

            for device in self.device_config.devices:
                if device.name.rsplit('_Pump', 1)[0] in valve_name:
                    logging.debug(f"Valve {valve_name} belongs to device {device}")
                    if 'QmixIO' in device.name:
                        # These valve devices are actually just convenience devices
                        # that operate on digital I/O channels. Hence, they can be
                        # just used via their corresponding I/O channel.
                        continue
                    device.valves += [valve]
                    if type(device) == Device:
                        ValveDevice.convert_to_class(device)
                        valves += [device]
        return valves

    #-------------------------------------------------------------------------
    # Controllers
    def get_availabe_controllers(self) -> List[ControllerDevice]:
        """
        Looks up all controller channels from the current configuration and maps
        them to their corresponding device

        :return: A list of all controller devices
        """
        channel_count = qmixcontroller.ControllerChannel.get_no_of_channels()
        logging.debug("Number of controller channels: %s", channel_count)

        channels = []

        for i in range(channel_count):
            channel = qmixcontroller.ControllerChannel()
            channel.lookup_channel_by_index(i)
            logging.debug("Found controller channel %d named %s", i, channel.get_name())
            channels.append(channel)

        return self.device_config.add_channels_to_device(channels)

    #-------------------------------------------------------------------------
    # I/O
    def get_availabe_io_channels(self) -> List[IODevice]:
        """
        Looks up all analog and digital I/O channels from the current configuration
        and maps them to their corresponding device

        :return: A list of all I/O channels
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

        return self.device_config.add_channels_to_device(channels)

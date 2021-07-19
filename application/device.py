"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Device*

:details: Device:
    Helper and wrapper classes for the Application class

:file:    application.py
:authors: Florian Meinicke

:date: (creation)          2021-07-15
:date: (last modification) 2021-07-15

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

import os
import logging
from typing import Any, Dict, List, Union
from lxml import etree, objectify

# import qmixsdk
from qmixsdk import qmixbus, qmixpump, qmixcontroller, qmixanalogio, qmixdigio, \
                    qmixmotion, qmixvalve


class Device():
    """
    Simple data class that holds information about a single device on the CAN bus
    """
    name: str
    properties: Dict[str, Any]

    # a device *might* have any combination and number of the following
    io_channels: List[Union[qmixanalogio.AnalogChannel, qmixdigio.DigitalChannel]]
    controller_channels: List[qmixcontroller.ControllerChannel]
    valves: List[qmixvalve.Valve]

    def __init__(self, name):
        self.name = name
        self.properties = {}

        self.valves = []
        self.controller_channels = []
        self.io_channels = []

    def __str__(self) -> str:
        return f"{self.name} {self.properties if self.properties else ''}"

    def __repr__(self) -> str:
        return f"{self.name} {self.properties if self.properties else ''} " \
               f"{[v.get_device_name() for v in self.valves]} " \
               f"{[c.get_name() for c in self.controller_channels]} " \
               f"{[c.get_name() for c in self.io_channels]}"

    def set_device_property(self, name: str, value: Any):
        """
        Set the device property `name` to the given value `value`
        If the property is not present yet it will be added automatically
        """
        self.properties[name] = value

    def set_operational(self):
        """
        Set the device (and all of its valves, if present) into operational state
        """
        for valve in self.valves:
            valve.set_communication_state(qmixbus.CommState.operational)

    @classmethod
    def convert_to_class(cls, obj, **kwargs):
        """
        Convert this general device to a specific device (e.g. a `PumpDevice`)
        `kwargs` are passed to the new class to initialize any additional members
        that this class might have
            >>> device = Device("pump")
                pump = qmixpump.Pump()
                pump.lookup_by_device_index(0)
                PumpDevice.convert_to_class(device, handle=pump.handle)

        :param cls: The class to convert `obj` to
        :param obj: The object to convert
        :param kwargs: Additional arguments used to initialize members of the new class
        """
        obj.__class__ = cls
        for name, value in kwargs.items():
            obj.__setattr__(name, value)

class PumpDevice(qmixpump.Pump, Device):
    """
    Simple wrapper around `qmixpump.Pump` with additional information from the
    `Device` class
    """
    def __init__(self, name: str):
        super().__init__(name)

    def set_operational(self):
        super().set_operational()
        self.set_communication_state(qmixbus.CommState.operational)
        self.clear_fault()
        self.enable(True)

class AxisSystemDevice(qmixmotion.AxisSystem, Device):
    """
    Simple wrapper around `qmixmotion.AxisSystem` with additional information
    from the `Device` class
    """
    def __init__(self, name: str):
        super().__init__(name)

    def set_operational(self):
        super().set_operational()
        self.set_communication_state(qmixbus.CommState.operational)
        self.enable(True)

class ValveDevice(Device):
    """
    Simple class to represent a valve device that has an arbitrary number of
    valves (inherited from the `Device` class)
    """
    def __init__(self, name: str):
        super().__init__(name)

class ControllerDevice(Device):
    """
    Simple class to represent a controller device that has an arbitrary number of
    controller channels (inherited from the `Device` class)
    """
    def __init__(self, name: str):
        super().__init__(name)

class IODevice(Device):
    """
    Simple class to represent an I/O device that has an arbitrary number of analog
    and digital I/O channels (inherited from the `Device` class)
    """
    def __init__(self, name: str):
        super().__init__(name)

class DeviceConfiguration:
    """
    Contains specific parts of the device configuration that is also used by the
    `qmixbus.Bus`.
    Provides means to parse the configuration from a given configuration folder
    """

    path: str
    devices: List[Device]
    has_battery: bool

    def __init__(self, path: str):
        """
        Parses the device configuration files located in the folder given by the
        `config_path` parameter.

        :param config_path: Path to a valid device configuration
        """
        logging.debug(f"Parsing device configuration {path}")
        self.path = path
        self.devices = []

        self._parse()

    def _parse(self):
        """
        Parses the device configuration
        """
        tree: objectify.ObjectifiedElement
        with open(os.path.join(self.path, 'device_properties.xml')) as f:
            tree = objectify.parse(f)
        root = tree.getroot()
        for plugin in root.Core.PluginList.iterchildren():
            if plugin.text in ('qmixelements', 'scriptingsystem', 'labbcanservice',
                               'canopentools', 'qmixdevices', 'datalogger'):
                # these files are the only ones with UTF-8 w/ BOM which leads to
                # an error while parsing the file; since we don't need them anyway
                # we can skip them
                continue

            self._parse_plugin(plugin.text)

        filtered_devices = [device for device in filter(self.__unneeded_devices, self.devices)]
        self.devices = [device for device in map(self.__fix_device_name, filtered_devices)]

        logging.debug(f"Found the following devices: {self.devices}")

        try:
            self.has_battery = bool(root.SiLA.BatteryPowered)
        except AttributeError:
            self.has_battery = False


    def _parse_plugin(self, plugin_name: str):
        """
        Parses the configuration for the plugin named `plugin_name`

        :param plugin_name: The name of the plugin to parse
        """
        logging.debug(f"Parsing configuration for {plugin_name} plugin")
        # we need to create a new parser that parses our 'broken' XML files
        # (they are regarded as 'broken' because they contain multiple root tags)
        parser = objectify.makeparser(recover=True)
        with open(os.path.join(self.path, plugin_name + '.xml')) as f:
            # wrap the 'broken' XML in a new <root> so that we can parse the
            # whole document instead of just the first root
            lines = f.readlines()
            fixed_xml = bytes(lines[0] + '<root>' + ''.join(lines[1:]) + '</root>', 'utf-8')

            plugin_tree: objectify.ObjectifiedElement = objectify.fromstring(fixed_xml, parser)
            plugin_root = plugin_tree.Plugin
            try:
                for device in plugin_root.labbCAN.DeviceList.iterchildren():
                    self.devices += [Device(device.get('Name'))]
            except AttributeError:
                pass

            if 'rotaxys' in plugin_name:
                # no possibility to find the jib length elsewhere
                for device in plugin_root.DeviceList.iterchildren():
                    self.device_by_name(device.get('Name')).set_device_property(
                        'jib_length', abs(int(device.JibLength.text)))

    @staticmethod
    def __unneeded_devices(device: Device):
        """
        Filter the devices as they contains more than the actual physical modules that we're after
        """
        for exclude in ('Epos', 'Valve'):
            if exclude in device.name:
                return False
        return True

    @staticmethod
    def __fix_device_name(device: Device):
        """
        Some devices are represented as '<device>_ChipF40' but we only want it to be '<device>'
        """
        device.name = device.name.split('_ChipF40', 1)[0]
        return device

    def device_by_name(self, name: str):
        """
        Retrieves a Device by its name

        Raises ValueError if there is no Device with the `name` present.

        :param name: The name of the device to get
        :return: The Device with the given `name`
        """
        for device in self.devices:
            if name == device.name:
                return device
        raise ValueError(f"No device with name {name}")


    def add_channels_to_device(self, channels: List[Union[qmixcontroller.ControllerChannel,
                                                          qmixanalogio.AnalogChannel,
                                                          qmixdigio.DigitalChannel]]) \
        -> List[Device]:
        """
        A device might have controller or I/O channels. This relationship between
        a device and its channels is constructed here.
        If a device is not of a specific type yet (i.e. it's not a `PumpDevice`,
        `AxisSystemDevice` or `ValveDevice`) it is converted to either a `ControllerDevice`
        or an `IODevice` depending on the type of the channel.

        :param channels: A list of channels that should be mapped to their corresponding devices
        :return: A list of all devices where a channel has been added
        """
        devices = set()

        for channel in channels:
            channel_name = channel.get_name()
            for device in self.devices:
                if device.name.rsplit('_Pump', 1)[0] in channel_name:
                    logging.debug(f"Channel {channel_name} belongs to device {device}")
                    if isinstance(channel, qmixcontroller.ControllerChannel):
                        device.controller_channels += [channel]
                        if type(device) == Device:
                            ControllerDevice.convert_to_class(device)
                            devices.add(device)
                    else:
                        device.io_channels += [channel]
                        if type(device) == Device:
                            IODevice.convert_to_class(device)
                            devices.add(device)
        return list(devices)

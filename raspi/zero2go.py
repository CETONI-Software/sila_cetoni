#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Zero2Go*

:details: Zero2Go:
    Provides a Python interface in form of a class to read data from the Zero2Go's I²C address

:file:    zero2go.py
:authors: Florian Meinicke

:date: (creation)          2021-04-20
:date: (last modification) 2021-04-20

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

import subprocess
import logging
class Zero2Go:
    def __init__(self) -> None:
        try:
            from smbus2 import SMBus
        except ModuleNotFoundError:
            print("Zero2Go requires smbus2 module and python-smbus package:")
            print("`sudo apt install python-smbus`")
            print("`pip install smbus2`")
            return

        self.bus = SMBus(1)
        self._I2C_ADDRESS = 0x29
        self._channel_to_int_registers = {
            'A': 1,
            'B': 3,
            'C': 5,
        }
        self._channel_to_dec_registers = {
            'A': 2,
            'B': 4,
            'C': 6,
        }

    @staticmethod
    def is_available() -> bool:
        """
        Whether this device uses Zero2Go
        """
        try:
            from smbus2 import SMBus
        except ModuleNotFoundError:
            return False

        return subprocess.call(['service', 'zero2go_daemon', 'status'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0


    def voltage_for_channel(self, channel: str) -> float:
        """
        Reads the current voltage value for the given channel

        :param channel: The channel to read from (either 'A', 'B', or 'C')
        """

        if channel not in self._channel_to_int_registers.keys():
            raise ValueError("Channel has to be either 'A', 'B', or 'C'!")


        int_voltage = self.bus.read_byte_data(
            self._I2C_ADDRESS, self._channel_to_int_registers[channel])
        dec_voltage = self.bus.read_byte_data(
            self._I2C_ADDRESS, self._channel_to_dec_registers[channel]) * 0.01

        return int_voltage + dec_voltage

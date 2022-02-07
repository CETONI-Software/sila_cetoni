from __future__ import annotations

import time, math
from threading import Event
from concurrent.futures import Executor

from typing import Any, Dict

from sila2.framework import FullyQualifiedIdentifier

from ....application.system import ApplicationSystem
from qmixsdk.qmixanalogio import AnalogInChannel

from ..generated.batteryprovider import BatteryProviderBase


class BatteryProviderImpl(BatteryProviderBase):
    __system: ApplicationSystem
    __stop_event: Event

    def __init__(self, executor: Executor):
        super().__init__()
        self.__system = ApplicationSystem()
        self.__stop_event = Event()

        def update_voltage(stop_event: Event):
            # The only battery powered device we have is our mobile dosage unit (MobDos).
            # This will always only have a single pump where the first analog in channel
            # provides the current voltage of the system (i.e. the voltage of the battery).
            channel: AnalogInChannel = self.__system.pumps[0].io_channels[0]
            # The value we get from the analog in channel has been divided by
            # a voltage divider so we have to multiply by this factor to get
            # the actual voltage value.
            VOLTAGE_DIVIDER_FACTOR = 0.00558

            new_voltage = channel.read_input() * VOLTAGE_DIVIDER_FACTOR if self.__system.state.is_operational() else 0
            voltage = 0  # force sending the first value
            while not stop_event.is_set():
                new_voltage = (
                    channel.read_input() * VOLTAGE_DIVIDER_FACTOR if self.__system.state.is_operational() else 0
                )
                if not math.isclose(new_voltage, voltage):
                    voltage = new_voltage
                    self.update_BatteryVoltage(voltage)
                time.sleep(0.1)

        executor.submit(update_voltage, self.__stop_event)

    def stop(self) -> None:
        self.__stop_event.set()

from __future__ import annotations

import time, math
from concurrent.futures import Executor
from threading import Event
from typing import Any, Dict, List, Union

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property

from application.system import ApplicationSystem
from qmixsdk.qmixanalogio import AnalogInChannel

from ..generated.analoginchannelprovider import (
    AnalogInChannelProviderBase,
    AnalogInChannelProviderFeature,
)


class AnalogInChannelProviderImpl(AnalogInChannelProviderBase):
    __system: ApplicationSystem
    __channels: List[AnalogInChannel]
    __stop_event: Event

    def __init__(self, channels: List[AnalogInChannel], executor: Executor):
        super().__init__()
        self.__system = ApplicationSystem()
        self.__channels = channels
        self.__stop_event = Event()

        def update_value(stop_event: Event):
            new_value = self.__channels[0].read_input()  # TODO channel from metadata
            value = -1  # force sending first value
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_value = self.__channels[0].read_input()  # TODO channel from metadata
                if not math.isclose(new_value, value):
                    value = new_value
                    self.update_Value(value)
                time.sleep(0.1)

        executor.submit(update_value, self.__stop_event)

    def get_NumberOfChannels(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> int:
        return len(self.__channels)

    def get_calls_affected_by_ChannelIndex(self) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        return [AnalogInChannelProviderFeature["Value"]]

    def stop(self) -> None:
        self.__stop_event.set()

from __future__ import annotations

import time
from concurrent.futures import Executor
from threading import Event
from typing import Any, Dict, List, Union

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property

from application.system import ApplicationSystem
from qmixsdk.qmixdigio import DigitalInChannel

from ..generated.digitalinchannelprovider import (
    DigitalInChannelProviderBase,
    DigitalInChannelProviderFeature,
    State,
)


class DigitalInChannelProviderImpl(DigitalInChannelProviderBase):
    __system: ApplicationSystem
    __channels: List[DigitalInChannel]
    __stop_event: Event

    def __init__(self, channels: List[DigitalInChannel], executor: Executor):
        super().__init__()
        self.__system = ApplicationSystem()
        self.__channels = channels
        self.__stop_event = Event()

        def update_value(stop_event: Event):
            new_is_on = self.__channels[0].is_on() # TODO channel from metadata
            is_on = not new_is_on # force sending first value
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_is_on = self.__channels[0].is_on() # TODO channel from metadata
                if new_is_on != is_on:
                    is_on = new_is_on
                    self.update_State('On' if is_on else 'Off')
                time.sleep(0.1)

        executor.submit(update_value, self.__stop_event)

    def get_NumberOfChannels(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> int:
        return len(self.__channels)

    def get_calls_affected_by_ChannelIndex(self) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        return [DigitalInChannelProviderFeature["State"]]

    def stop(self) -> None:
        self.__stop_event.set()

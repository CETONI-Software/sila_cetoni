from __future__ import annotations
from queue import Queue

import time, math
from concurrent.futures import Executor
from threading import Event
from typing import Any, Dict, List, Union, Optional

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property

from ....application.system import ApplicationSystem
from qmixsdk.qmixanalogio import AnalogInChannel

from ..generated.analoginchannelprovider import (
    AnalogInChannelProviderBase,
    AnalogInChannelProviderFeature,
    InvalidChannelIndex,
)


class AnalogInChannelProviderImpl(AnalogInChannelProviderBase):
    __system: ApplicationSystem
    __channels: List[AnalogInChannel]
    __channel_index_identifier: FullyQualifiedIdentifier
    __value_queues: List[Queue[float]]  # same number of items and order as `__channels`
    __stop_event: Event

    def __init__(self, channels: List[AnalogInChannel], executor: Executor):
        super().__init__()
        self.__system = ApplicationSystem()
        self.__channels = channels
        self.__channel_index_identifier = AnalogInChannelProviderFeature["ChannelIndex"].fully_qualified_identifier
        self.__stop_event = Event()

        self.__value_queues = []
        for i in range(len(self.__channels)):
            self.__value_queues += [Queue()]
            self.update_Value(self.__channels[i].read_input(), queue=self.__value_queues[i])
            executor.submit(self.__make_value_updater(i), self.__stop_event)

    def __make_value_updater(self, i: int):
        def update_value(stop_event: Event):
            new_value = value = self.__channels[i].read_input()
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_value = self.__channels[i].read_input()
                if not math.isclose(new_value, value):
                    value = new_value
                    self.update_Value(value, queue=self.__value_queues[i])
                time.sleep(0.1)

        return update_value

    def get_NumberOfChannels(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> int:
        return len(self.__channels)

    def Value_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Optional[Queue[float]]:
        channel_index: int = metadata.pop(self.__channel_index_identifier)
        try:
            return self.__value_queues[channel_index]
        except IndexError:
            raise InvalidChannelIndex(
                message=f"The sent channel index {channel_index} is invalid. The index must be between 0 and {len(self.__channels) - 1}.",
            )

    def get_calls_affected_by_ChannelIndex(
        self,
    ) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        return [AnalogInChannelProviderFeature["Value"]]

    def stop(self) -> None:
        self.__stop_event.set()

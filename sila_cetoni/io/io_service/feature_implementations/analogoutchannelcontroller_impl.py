from __future__ import annotations

import logging
import math
import time
from concurrent.futures import Executor
from queue import Queue
from threading import Event
from typing import Any, Dict, List, Optional, Union

from qmixsdk.qmixanalogio import AnalogOutChannel
from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property
from sila2.framework.errors.framework_error import FrameworkError, FrameworkErrorType

from ....application.system import ApplicationSystem
from ..generated.analogoutchannelcontroller import (
    AnalogOutChannelControllerBase,
    AnalogOutChannelControllerFeature,
    InvalidChannelIndex,
    SetOutputValue_Responses,
)


class AnalogOutChannelControllerImpl(AnalogOutChannelControllerBase):
    __system: ApplicationSystem
    __channels: List[AnalogOutChannel]
    __channel_index_identifier: FullyQualifiedIdentifier
    __value_queues: List[Queue[float]]  # same number of items and order as `__channels`
    __stop_event: Event

    def __init__(self, channels: List[AnalogOutChannel], executor: Executor):
        super().__init__()
        self.__system = ApplicationSystem()
        self.__channels = channels
        self.__channel_index_identifier = AnalogOutChannelControllerFeature["ChannelIndex"].fully_qualified_identifier
        self.__stop_event = Event()

        self.__value_queues = []
        for i in range(len(self.__channels)):
            self.__value_queues += [Queue()]

            # initial value
            self.update_Value(self.__channels[i].get_output_value(), queue=self.__value_queues[i])

            executor.submit(self.__make_value_updater(i), self.__stop_event)

    def __make_value_updater(self, i: int):
        def update_value(stop_event: Event):
            new_value = value = self.__channels[i].get_output_value()
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_value = self.__channels[i].get_output_value()
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

    def SetOutputValue(
        self, Value: float, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SetOutputValue_Responses:
        channel_index: int = metadata.pop(self.__channel_index_identifier)
        logging.debug(f"channel index: {channel_index}")
        try:
            self.__channels[channel_index].write_output(Value)
        except IndexError:
            raise InvalidChannelIndex(
                message=f"The sent channel index {channel_index} is invalid. The index must be between 0 and {len(self.__channels) - 1}.",
            )

    def get_calls_affected_by_ChannelIndex(
        self,
    ) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        return [
            AnalogOutChannelControllerFeature["Value"],
            AnalogOutChannelControllerFeature["SetOutputValue"],
        ]

    def stop(self) -> None:
        self.__stop_event.set()

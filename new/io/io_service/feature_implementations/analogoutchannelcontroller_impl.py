from __future__ import annotations
import logging

import time, math
from concurrent.futures import Executor
from threading import Event
from typing import Any, Dict, List, Union

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property

from application.system import ApplicationSystem
from qmixsdk.qmixanalogio import AnalogOutChannel

from ..generated.analogoutchannelcontroller import (
    AnalogOutChannelControllerBase,
    AnalogOutChannelControllerFeature,
    SetOutputValue_Responses,
)


class AnalogOutChannelControllerImpl(AnalogOutChannelControllerBase):
    __system: ApplicationSystem
    __channels: List[AnalogOutChannel]
    __channel_index_identifier: FullyQualifiedIdentifier
    __stop_event: Event

    def __init__(self, channels: List[AnalogOutChannel], executor: Executor):
        super().__init__()
        self.__system = ApplicationSystem()
        self.__channels = channels
        self.__channel_index_identifier = AnalogOutChannelControllerFeature["ChannelIndex"].fully_qualified_identifier
        self.__stop_event = Event()

        def update_value(stop_event: Event):
            new_value = self.__channels[0].get_output_value()  # TODO channel from metadata
            value = -1  # force sending first value
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_value = self.__channels[0].get_output_value()  # TODO channel from metadata
                if not math.isclose(new_value, value):
                    value = new_value
                    self.update_Value(value)
                time.sleep(0.1)

        executor.submit(update_value, self.__stop_event)

    def get_NumberOfChannels(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> int:
        return len(self.__channels)

    def SetOutputValue(
        self, Value: float, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SetOutputValue_Responses:
        channel_identifier: int = metadata.pop(self.__channel_index_identifier)
        logging.debug(f"channel id: {channel_identifier}")
        self.__channels[channel_identifier].write_output(Value)

    def get_calls_affected_by_ChannelIndex(self) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        return [
            AnalogOutChannelControllerFeature["Value"],
            AnalogOutChannelControllerFeature["SetOutputValue"],
        ]

    def stop(self) -> None:
        self.__stop_event.set()

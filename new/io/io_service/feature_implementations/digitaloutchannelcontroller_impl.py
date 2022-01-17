from __future__ import annotations
import logging

import time
from concurrent.futures import Executor
from threading import Event
from typing import Any, Dict, List, Union

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property

from application.system import ApplicationSystem
from qmixsdk.qmixdigio import DigitalOutChannel

from ..generated.digitaloutchannelcontroller import (
    DigitalOutChannelControllerBase,
    DigitalOutChannelControllerFeature,
    SetOutput_Responses,
    State,
)


class DigitalOutChannelControllerImpl(DigitalOutChannelControllerBase):
    __system: ApplicationSystem
    __channels: List[DigitalOutChannel]
    __channel_index_identifier: FullyQualifiedIdentifier
    __stop_event: Event

    def __init__(self, channels: List[DigitalOutChannel], executor: Executor):
        super().__init__()
        self.__system = ApplicationSystem()
        self.__channels = channels
        self.__channel_index_identifier = DigitalOutChannelControllerFeature["ChannelIndex"].fully_qualified_identifier
        self.__stop_event = Event()

        def update_value(stop_event: Event):
            new_is_on = self.__channels[0].is_output_on() # TODO channel from metadata
            is_on = not new_is_on # force sending first value
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_is_on = self.__channels[0].is_output_on() # TODO channel from metadata
                if new_is_on != is_on:
                    is_on = new_is_on
                    self.update_State('On' if is_on else 'Off')
                time.sleep(0.1)

        executor.submit(update_value, self.__stop_event)

    def get_NumberOfChannels(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> int:
        return len(self.__channels)

    def SetOutput(self, State: State, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> SetOutput_Responses:
        channel_identifier: int = metadata.pop(self.__channel_index_identifier)
        logging.debug(f"channel id: {channel_identifier}")
        self.__channels[channel_identifier].write_on(State == "On")

    def get_calls_affected_by_ChannelIndex(self) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        return [
            DigitalOutChannelControllerFeature["State"],
            DigitalOutChannelControllerFeature["SetOutput"],
        ]

    def stop(self) -> None:
        self.__stop_event.set()

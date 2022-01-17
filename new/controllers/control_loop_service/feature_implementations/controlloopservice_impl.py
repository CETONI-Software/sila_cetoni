from __future__ import annotations
import logging

import time
from concurrent.futures import Executor
from threading import Event
from typing import Any, Dict, List, Union

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property
from sila2.server import ObservableCommandInstance

from qmixsdk.qmixcontroller import ControllerChannel

from ..generated.controlloopservice import (
    ControlLoopServiceBase,
    RunControlLoop_Responses,
    StopControlLoop_Responses,
    WriteSetPoint_Responses,
    ControlLoopServiceFeature,
)


class ControlLoopServiceImpl(ControlLoopServiceBase):
    __controller_channels: List[ControllerChannel]
    __channel_index_identifier: FullyQualifiedIdentifier
    __stop_event: Event

    def __init__(self, controller_channels: List[ControllerChannel], executor: Executor):
        super().__init__()
        self.__controller_channels = controller_channels
        self.__channel_index_identifier = ControlLoopServiceFeature["ChannelIndex"].fully_qualified_identifier

        def update_set_point(stop_event: Event):
            while not stop_event.is_set():
                self.update_SetPointValue(self.__controller_channels[0].get_setpoint()) # TODO: channel from metadata
                # TODO: smart update
                time.sleep(0.1)

        def update_controller_value(stop_event: Event):
            while not stop_event.is_set():
                self.update_ControllerValue(self.__controller_channels[0].read_actual_value()) # TODO: channel from metadata
                # TODO: smart update
                time.sleep(0.1)

        executor.submit(update_set_point, self.__stop_event)
        executor.submit(update_controller_value, self.__stop_event)


    def get_NumberOfChannels(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> int:
        return len(self.__controller_channels)

    def WriteSetPoint(
        self, SetPointValue: float, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> WriteSetPoint_Responses:
        channel_identifier: int = metadata.pop(self.__channel_index_identifier)
        logging.debug(f"channel id: {channel_identifier}")
        self.__controller_channels[channel_identifier].write_setpoint(SetPointValue)

    def StopControlLoop(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> StopControlLoop_Responses:
        channel_identifier: int = metadata.pop(self.__channel_index_identifier)
        logging.debug(f"channel id: {channel_identifier}")
        self.__controller_channels[channel_identifier].enable_control_loop(False)

    def RunControlLoop(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any], instance: ObservableCommandInstance
    ) -> RunControlLoop_Responses:
        channel_identifier: int = metadata.pop(self.__channel_index_identifier)
        logging.debug(f"channel id: {channel_identifier}")
        self.__controller_channels[channel_identifier].enable_control_loop(True)

    def get_calls_affected_by_ChannelIndex(self) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
            return [
                ControlLoopServiceFeature["WriteSetPoint"].fully_qualified_identifier,
                ControlLoopServiceFeature["RunControlLoop"].fully_qualified_identifier,
                ControlLoopServiceFeature["StopControlLoop"].fully_qualified_identifier,
                ControlLoopServiceFeature["ControllerValue"].fully_qualified_identifier,
                ControlLoopServiceFeature["SetPointValue"].fully_qualified_identifier,
            ]

    def stop(self) -> None:
        self.__stop_event.set()

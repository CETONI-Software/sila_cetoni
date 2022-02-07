from __future__ import annotations
import logging
import math
from queue import Queue

import time
from concurrent.futures import Executor
from threading import Event
from typing import Any, Dict, List, Optional, Union

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property
from sila2.server import ObservableCommandInstance

from qmixsdk.qmixcontroller import ControllerChannel

from ..generated.controlloopservice import (
    ControlLoopServiceBase,
    RunControlLoop_Responses,
    StopControlLoop_Responses,
    WriteSetPoint_Responses,
    ControlLoopServiceFeature,
    InvalidChannelIndex,
)


class ControlLoopServiceImpl(ControlLoopServiceBase):
    __controller_channels: List[ControllerChannel]
    __channel_index_identifier: FullyQualifiedIdentifier
    __set_point_queues: List[Queue[float]]  # same number of items and order as `__controller_channels`
    __controller_value_queues: List[Queue[float]]  # same number of items and order as `__controller_channels`
    __stop_event: Event

    def __init__(self, controller_channels: List[ControllerChannel], executor: Executor):
        super().__init__()
        self.__controller_channels = controller_channels
        self.__channel_index_identifier = ControlLoopServiceFeature["ChannelIndex"].fully_qualified_identifier

        self.__stop_event = Event()

        self.__set_point_queues = []
        self.__controller_value_queues = []
        for i in range(len(self.__controller_channels)):
            self.__set_point_queues += [Queue()]
            self.__controller_value_queues += [Queue()]

            # initial values
            self.update_SetPointValue(
                self.__controller_channels[i].get_setpoint(),
                queue=self.__set_point_queues[i],
            )
            self.update_ControllerValue(
                self.__controller_channels[i].read_actual_value(),
                queue=self.__controller_value_queues[i],
            )

            executor.submit(self.__make_set_point_updater(i), self.__stop_event)
            executor.submit(self.__make_controller_value_updater(i), self.__stop_event)

    def __make_set_point_updater(self, i: int):
        def update_set_point(stop_event: Event):
            new_set_point = set_point = self.__controller_channels[i].get_setpoint()
            while not stop_event.is_set():
                new_set_point = self.__controller_channels[i].get_setpoint()
                if not math.isclose(new_set_point, set_point):
                    set_point = new_set_point
                    self.update_SetPointValue(set_point, queue=self.__set_point_queues[i])
                time.sleep(0.1)

        return update_set_point

    def __make_controller_value_updater(self, i: int):
        def update_set_point(stop_event: Event):
            new_controller_value = controller_value = self.__controller_channels[i].read_actual_value()
            while not stop_event.is_set():
                new_controller_value = self.__controller_channels[i].read_actual_value()
                if not math.isclose(new_controller_value, controller_value):
                    controller_value = new_controller_value
                    self.update_ControllerValue(controller_value, queue=self.__controller_value_queues[i])
                time.sleep(0.1)

        return update_set_point

    def get_NumberOfChannels(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> int:
        return len(self.__controller_channels)

    def SetPointValue_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Optional[Queue[float]]:
        channel_index = metadata[self.__channel_index_identifier]
        try:
            return self.__set_point_queues[channel_index]
        except IndexError:
            raise InvalidChannelIndex(
                message=f"The sent channel index {channel_index} is invalid. The index must be between 0 and {len(self.__controller_channels) - 1}.",
            )

    def ControllerValue_on_subscription(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> Optional[Queue[float]]:
        channel_index = metadata[self.__channel_index_identifier]
        try:
            return self.__controller_value_queues[channel_index]
        except IndexError:
            raise InvalidChannelIndex(
                message=f"The sent channel index {channel_index} is invalid. The index must be between 0 and {len(self.__controller_channels) - 1}.",
            )

    def __controller_channel_for_index(self, channel_index: int) -> ControllerChannel:
        try:
            return self.__controller_channels[channel_index]
        except IndexError:
            raise InvalidChannelIndex(
                message=f"The sent channel index {channel_index} is invalid. The index must be between 0 and {len(self.__controller_channels) - 1}.",
            )

    def WriteSetPoint(
        self, SetPointValue: float, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> WriteSetPoint_Responses:
        channel_identifier: int = metadata.pop(self.__channel_index_identifier)
        logging.debug(f"channel id: {channel_identifier}")
        self.__controller_channel_for_index(channel_identifier).write_setpoint(SetPointValue)

    def StopControlLoop(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> StopControlLoop_Responses:
        channel_identifier: int = metadata.pop(self.__channel_index_identifier)
        logging.debug(f"channel id: {channel_identifier}")
        self.__controller_channel_for_index(channel_identifier).enable_control_loop(False)

    def RunControlLoop(
        self,
        *,
        metadata: Dict[FullyQualifiedIdentifier, Any],
        instance: ObservableCommandInstance,
    ) -> RunControlLoop_Responses:
        channel_identifier: int = metadata.pop(self.__channel_index_identifier)
        logging.debug(f"channel id: {channel_identifier}")
        self.__controller_channel_for_index(channel_identifier).enable_control_loop(True)

    def get_calls_affected_by_ChannelIndex(
        self,
    ) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        return [
            ControlLoopServiceFeature["WriteSetPoint"].fully_qualified_identifier,
            ControlLoopServiceFeature["RunControlLoop"].fully_qualified_identifier,
            ControlLoopServiceFeature["StopControlLoop"].fully_qualified_identifier,
            ControlLoopServiceFeature["ControllerValue"].fully_qualified_identifier,
            ControlLoopServiceFeature["SetPointValue"].fully_qualified_identifier,
        ]

    def stop(self) -> None:
        self.__stop_event.set()

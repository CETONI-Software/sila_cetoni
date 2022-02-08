from __future__ import annotations

import datetime
import time
from concurrent.futures import Executor
from threading import Event
from typing import Any, Dict

from qmixsdk.qmixbus import PollingTimer
from qmixsdk.qmixpump import ContiFlowPump
from sila2.framework import CommandExecutionStatus, FullyQualifiedIdentifier
from sila2.framework.errors.validation_error import ValidationError
from sila2.server import ObservableCommandInstance

from ..generated.continuousflowinitializationcontroller import (
    ContinuousFlowInitializationControllerBase,
    InitializeContiflow_Responses,
)


class ContinuousFlowInitializationControllerImpl(ContinuousFlowInitializationControllerBase):
    __pump: ContiFlowPump
    __stop_event: Event

    def __init__(self, pump: ContiFlowPump, executor: Executor):
        super().__init__()
        self.__pump = pump
        self.__stop_event = Event()

        def update_is_initialized(stop_event: Event):
            new_is_initialized = is_initialized = self.__pump.is_initialized()
            while not stop_event.is_set():
                new_is_initialized = self.__pump.is_initialized()
                if new_is_initialized != is_initialized:
                    is_initialized = new_is_initialized
                    self.update_IsInitialized(is_initialized)
                time.sleep(0.1)

        # initial value
        self.update_IsInitialized(self.__pump.is_initialized())

        executor.submit(update_is_initialized, self.__stop_event)

    def InitializeContiflow(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any], instance: ObservableCommandInstance
    ) -> InitializeContiflow_Responses:
        MAX_WAIT_TIME = datetime.timedelta(seconds=30)
        timer = PollingTimer(MAX_WAIT_TIME.seconds * 1000)

        # send first info immediately
        instance.status = CommandExecutionStatus.running
        instance.progress = 0
        instance.estimated_remaining_time = datetime.timedelta(seconds=timer.get_msecs_to_expiration() / 1000)

        self.__pump.initialize()

        while self.__pump.is_initializing() and not timer.is_expired():
            instance.status = CommandExecutionStatus.running
            instance.estimated_remaining_time = datetime.timedelta(seconds=timer.get_msecs_to_expiration() / 1000)
            instance.progress = 100 * instance.estimated_remaining_time / MAX_WAIT_TIME
            time.sleep(0.5)

    def stop(self) -> None:
        self.__stop_event.set()

from __future__ import annotations

import time
from threading import Event
from concurrent.futures import Executor

from typing import Any, Dict

from sila2.framework import FullyQualifiedIdentifier

from ....application.system import ApplicationSystem

from ..generated.systemstatusprovider import SystemStatusProviderBase


class SystemStatusProviderImpl(SystemStatusProviderBase):
    __system: ApplicationSystem
    __stop_event: Event

    def __init__(self, executor: Executor):
        super().__init__()
        self.__system = ApplicationSystem()
        self.__stop_event = Event()

        def update_state(stop_event: Event):
            new_state = self.__system.state.value
            state = ""  # force sending the first value
            while not stop_event.is_set():
                new_state = self.__system.state.value
                if new_state != state:
                    state = new_state
                    self.update_SystemState(state)
                time.sleep(0.1)

        executor.submit(update_state, self.__stop_event)

    def stop(self) -> None:
        self.__stop_event.set()

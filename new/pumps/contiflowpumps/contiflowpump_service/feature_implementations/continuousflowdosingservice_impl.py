from __future__ import annotations

import time
from threading import Event
from concurrent.futures import Executor
from typing import Any, Dict

from sila2.framework import FullyQualifiedIdentifier, CommandExecutionStatus
from sila2.server import ObservableCommandInstance
from sila2.framework.errors.validation_error import ValidationError

from qmixsdk.qmixpump import ContiFlowPump

from ....validate import validate

from ..generated.continuousflowdosingservice import (
    ContinuousFlowDosingServiceBase,
    ContinuousFlowDosingServiceFeature,
    GenerateFlow_Responses,
    StopDosage_Responses,
)


class ContinuousFlowDosingServiceImpl(ContinuousFlowDosingServiceBase):
    __pump: ContiFlowPump
    __stop_event: Event

    def __init__(self, pump: ContiFlowPump, executor: Executor):
        super().__init__()
        self.__pump = pump
        self.__stop_event = Event()

        def update_flow_rate(stop_event: Event):
            while not stop_event.is_set():
                self.update_FlowRate(self.__pump.get_flow_is())
                # TODO smart update
                time.sleep(0.1)

        def update_max_flow_rate(stop_event: Event):
            while not stop_event.is_set():
                self.update_MaxFlowRate(self.__pump.get_flow_rate_max())
                # TODO smart update
                time.sleep(0.1)

        executor.submit(update_flow_rate, self.__stop_event)
        executor.submit(update_max_flow_rate, self.__stop_event)

    def StopDosage(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> StopDosage_Responses:
        self.__pump.stop_pumping()

    def GenerateFlow(
        self, FlowRate: float, *, metadata: Dict[FullyQualifiedIdentifier, Any], instance: ObservableCommandInstance
    ) -> GenerateFlow_Responses:
        validate(self.__pump, ContinuousFlowDosingServiceFeature["GenerateFlow"], FlowRate)
        # self.__pump.stop_pumping() # only one dosage allowed
        # time.sleep(0.25) # wait for the currently running dosage to catch up

        self.__pump.generate_flow(FlowRate)

        # send first info immediately
        instance.status = CommandExecutionStatus.running

        is_pumping = True
        while is_pumping:
            time.sleep(0.5)
            instance.status = CommandExecutionStatus.running
            is_pumping = self.__pump.is_pumping()

        if not is_pumping and not self.__pump.is_in_fault_state():
            instance.status = CommandExecutionStatus.finishedSuccessfully
        else:
            instance.status = CommandExecutionStatus.finishedWithError
            # raise QmixSDKSiLAError(self.__pump.read_last_error())

    def stop(self) -> None:
        self.__stop_event.set()

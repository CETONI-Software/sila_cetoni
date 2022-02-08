from __future__ import annotations

import math
import time
from concurrent.futures import Executor
from threading import Event
from typing import Any, Dict

from qmixsdk.qmixpump import ContiFlowPump
from sila2.framework import CommandExecutionStatus, FullyQualifiedIdentifier
from sila2.framework.errors.validation_error import ValidationError
from sila2.server import ObservableCommandInstance

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
            new_flow_rate = flow_rate = self.__pump.get_flow_is()
            while not stop_event.is_set():
                new_flow_rate = self.__pump.get_flow_is()
                if not math.isclose(new_flow_rate, flow_rate):
                    flow_rate = new_flow_rate
                    self.update_FlowRate(flow_rate)
                time.sleep(0.1)

        def update_max_flow_rate(stop_event: Event):
            new_max_flow_rate = max_flow_rate = self.__pump.get_flow_rate_max()
            while not stop_event.is_set():
                new_max_flow_rate = self.__pump.get_flow_rate_max()
                if not math.isclose(new_max_flow_rate, max_flow_rate):
                    max_flow_rate = new_max_flow_rate
                    self.update_MaxFlowRate(max_flow_rate)
                time.sleep(0.1)

        # initial values
        self.update_FlowRate(self.__pump.get_flow_is())
        self.update_MaxFlowRate(self.__pump.get_flow_rate_max())

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

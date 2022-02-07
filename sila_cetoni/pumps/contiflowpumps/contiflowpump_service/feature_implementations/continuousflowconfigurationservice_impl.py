from __future__ import annotations

import time
from threading import Event
from concurrent.futures import Executor
from typing import Any, Dict

from sila2.framework import FullyQualifiedIdentifier
from sila2.framework.errors.validation_error import ValidationError

from qmixsdk.qmixpump import ContiFlowProperty, ContiFlowPump, ContiFlowSwitchingMode

from ..generated.continuousflowconfigurationservice import (
    ContinuousFlowConfigurationServiceBase,
    ContinuousFlowConfigurationServiceFeature,
    SetCrossFlowDuration_Responses,
    SetOverlapDuration_Responses,
    SetRefillFlowRate_Responses,
    SetSwitchingMode_Responses,
)


class ContinuousFlowConfigurationServiceImpl(ContinuousFlowConfigurationServiceBase):
    __pump: ContiFlowPump
    __ALLOWED_SWITCHING_MODES = {
        "SwitchingCrossFlow": ContiFlowSwitchingMode.CROSS_FLOW
        # more to come
    }
    __stop_event: Event

    def __init__(self, pump: ContiFlowPump, executor: Executor):
        super().__init__()
        self.__pump = pump
        self.__stop_event = Event()

        # TODO restore drive position counter + contiflow params

        def update_cross_flow_duration(stop_event: Event):
            while not stop_event.is_set():
                self.update_CrossFlowDuration(self.__pump.get_device_property(ContiFlowProperty.CROSSFLOW_DURATION_S))
                # TODO smart update
                time.sleep(0.1)

        def update_max_refill_flow(stop_event: Event):
            while not stop_event.is_set():
                self.update_MaxRefillFlowRate(self.__pump.get_device_property(ContiFlowProperty.MAX_REFILL_FLOW))
                # TODO smart update
                time.sleep(0.1)

        def update_min_flow_rate(stop_event: Event):
            while not stop_event.is_set():
                self.update_MinFlowRate(self.__pump.get_device_property(ContiFlowProperty.MIN_PUMP_FLOW))
                # TODO smart update
                time.sleep(0.1)

        def update_overlap_duration(stop_event: Event):
            while not stop_event.is_set():
                self.update_OverlapDuration(self.__pump.get_device_property(ContiFlowProperty.OVERLAP_DURATION_S))
                # TODO smart update
                time.sleep(0.1)

        def update_refill_flow_rate(stop_event: Event):
            while not stop_event.is_set():
                self.update_RefillFlowRate(self.__pump.get_device_property(ContiFlowProperty.REFILL_FLOW))
                # TODO smart update
                time.sleep(0.1)

        def update_switching_mode(stop_event: Event):
            while not stop_event.is_set():
                self.update_SwitchingMode(self.__pump.get_device_property(ContiFlowProperty.SWITCHING_MODE))
                # TODO smart update
                time.sleep(0.1)

        executor.submit(update_cross_flow_duration, self.__stop_event)
        executor.submit(update_max_refill_flow, self.__stop_event)
        executor.submit(update_min_flow_rate, self.__stop_event)
        executor.submit(update_overlap_duration, self.__stop_event)
        executor.submit(update_refill_flow_rate, self.__stop_event)
        executor.submit(update_switching_mode, self.__stop_event)

    def SetSwitchingMode(
        self, SwitchingMode: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SetSwitchingMode_Responses:
        try:
            self.__pump.set_device_property(
                ContiFlowProperty.SWITCHING_MODE, self.__ALLOWED_SWITCHING_MODES.get(SwitchingMode)
            )
        except KeyError:
            raise ValidationError(
                ContinuousFlowConfigurationServiceFeature["SetSwitchingMode"].parameters.fields[0],
                "The given value for the Contiflow Switching Mode is invalid. Allowed values are: {}".format(
                    ", ".join(self.__ALLOWED_SWITCHING_MODES.keys())
                ),
            )

    def SetRefillFlowRate(
        self, RefillFlowRate: float, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SetRefillFlowRate_Responses:
        self.__pump.set_device_property(ContiFlowProperty.REFILL_FLOW, RefillFlowRate)

    def SetCrossFlowDuration(
        self, CrossFlowDuration: float, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SetCrossFlowDuration_Responses:
        self.__pump.set_device_property(ContiFlowProperty.CROSSFLOW_DURATION_S, CrossFlowDuration)

    def SetOverlapDuration(
        self, OverlapDuration: float, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SetOverlapDuration_Responses:
        self.__pump.set_device_property(ContiFlowProperty.OVERLAP_DURATION_S, OverlapDuration)

    def stop(self) -> None:
        self.__stop_event.set()

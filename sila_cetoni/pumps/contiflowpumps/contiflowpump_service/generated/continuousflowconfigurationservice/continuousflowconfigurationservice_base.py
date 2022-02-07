from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase

from .continuousflowconfigurationservice_types import (
    SetCrossFlowDuration_Responses,
    SetOverlapDuration_Responses,
    SetRefillFlowRate_Responses,
    SetSwitchingMode_Responses,
)


class ContinuousFlowConfigurationServiceBase(FeatureImplementationBase, ABC):

    _SwitchingMode_producer_queue: Queue[str]

    _MaxRefillFlowRate_producer_queue: Queue[float]

    _RefillFlowRate_producer_queue: Queue[float]

    _MinFlowRate_producer_queue: Queue[float]

    _CrossFlowDuration_producer_queue: Queue[float]

    _OverlapDuration_producer_queue: Queue[float]

    def __init__(self):
        """
        Allows to configure the parameters of a continuous flow pump.
        """

        self._SwitchingMode_producer_queue = Queue()

        self._MaxRefillFlowRate_producer_queue = Queue()

        self._RefillFlowRate_producer_queue = Queue()

        self._MinFlowRate_producer_queue = Queue()

        self._CrossFlowDuration_producer_queue = Queue()

        self._OverlapDuration_producer_queue = Queue()

    def update_SwitchingMode(self, SwitchingMode: str):
        """
        Get the switching mode for syringe pump switchover if one syringe pump runs empty.

        This method updates the observable property 'SwitchingMode'.
        """
        self._SwitchingMode_producer_queue.put(SwitchingMode)

    def SwitchingMode_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        Get the switching mode for syringe pump switchover if one syringe pump runs empty.

        This method is called when a client subscribes to the observable property 'SwitchingMode'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass

    def update_MaxRefillFlowRate(self, MaxRefillFlowRate: float):
        """
        Get the maximum possible refill flow rate for the continuous flow pump.

        This method updates the observable property 'MaxRefillFlowRate'.
        """
        self._MaxRefillFlowRate_producer_queue.put(MaxRefillFlowRate)

    def MaxRefillFlowRate_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        Get the maximum possible refill flow rate for the continuous flow pump.

        This method is called when a client subscribes to the observable property 'MaxRefillFlowRate'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass

    def update_RefillFlowRate(self, RefillFlowRate: float):
        """
        Get the refill flow rate for the continuous flow pump.

        This method updates the observable property 'RefillFlowRate'.
        """
        self._RefillFlowRate_producer_queue.put(RefillFlowRate)

    def RefillFlowRate_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        Get the refill flow rate for the continuous flow pump.

        This method is called when a client subscribes to the observable property 'RefillFlowRate'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass

    def update_MinFlowRate(self, MinFlowRate: float):
        """
        Get the minimum flow rate that is theoretically possible with the continuous flow pump.

        This method updates the observable property 'MinFlowRate'.
        """
        self._MinFlowRate_producer_queue.put(MinFlowRate)

    def MinFlowRate_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        Get the minimum flow rate that is theoretically possible with the continuous flow pump.

        This method is called when a client subscribes to the observable property 'MinFlowRate'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass

    def update_CrossFlowDuration(self, CrossFlowDuration: float):
        """
        Get the cross flow duration for the continuous flow pump.

        This method updates the observable property 'CrossFlowDuration'.
        """
        self._CrossFlowDuration_producer_queue.put(CrossFlowDuration)

    def CrossFlowDuration_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        Get the cross flow duration for the continuous flow pump.

        This method is called when a client subscribes to the observable property 'CrossFlowDuration'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass

    def update_OverlapDuration(self, OverlapDuration: float):
        """
        Get the overlap duration for the continuous flow pump.

        This method updates the observable property 'OverlapDuration'.
        """
        self._OverlapDuration_producer_queue.put(OverlapDuration)

    def OverlapDuration_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        Get the overlap duration for the continuous flow pump.

        This method is called when a client subscribes to the observable property 'OverlapDuration'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass

    @abstractmethod
    def SetSwitchingMode(
        self, SwitchingMode: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SetSwitchingMode_Responses:
        """
        Sets the switching mode for syringe pump switchover if one syringe pump runs empty.


        :param SwitchingMode: The new switching mode to set

        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def SetRefillFlowRate(
        self, RefillFlowRate: float, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SetRefillFlowRate_Responses:
        """
        Set the refill flow rate for the continuous flow pump. The refill flow speed limits the maximum flow that is possible with a contiflow pump.


        :param RefillFlowRate: The refill flow rate to set

        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def SetCrossFlowDuration(
        self, CrossFlowDuration: float, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SetCrossFlowDuration_Responses:
        """
        Set the cross flow duration for the continuous flow pump. The cross flow duration is the time the pump running empty decelerates while the filled pump accelerates.


        :param CrossFlowDuration: The cross flow duration to set

        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def SetOverlapDuration(
        self, OverlapDuration: float, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SetOverlapDuration_Responses:
        """
        Set the overlap duration for the continuous flow pump. The overlap duration is a time the refilled pump will start earlier than the empty pump stops. You can use this time to ensure that the system is already pressurized when switching over.


        :param OverlapDuration: The overlap duration to set

        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

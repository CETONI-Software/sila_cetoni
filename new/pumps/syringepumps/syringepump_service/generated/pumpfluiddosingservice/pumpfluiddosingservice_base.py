from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict, Optional

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase, ObservableCommandInstance

from .pumpfluiddosingservice_types import (
    DoseVolume_Responses,
    GenerateFlow_Responses,
    SetFillLevel_Responses,
    StopDosage_Responses,
)


class PumpFluidDosingServiceBase(FeatureImplementationBase, ABC):

    _MaxSyringeFillLevel_producer_queue: Queue[float]

    _SyringeFillLevel_producer_queue: Queue[float]

    _MaxFlowRate_producer_queue: Queue[float]

    _FlowRate_producer_queue: Queue[float]

    def __init__(self):
        """
        Allows to dose a specified fluid. There are commands for absolute dosing (SetFillLevel) and relative dosing (DoseVolume and GenerateFlow) available.

        The flow rate can be negative. In this case the pump aspirates the fluid instead of dispensing. The flow rate has to be a value between MaxFlowRate and MinFlowRate. If the value is not within this range (hence is invalid) a ValidationError will be thrown.
        At any time the property CurrentSyringeFillLevel can be queried to see how much fluid is left in the syringe. Similarly the property CurrentFlowRate can be queried to get the current flow rate at which the pump is dosing.
        """

        self._MaxSyringeFillLevel_producer_queue = Queue()

        self._SyringeFillLevel_producer_queue = Queue()

        self._MaxFlowRate_producer_queue = Queue()

        self._FlowRate_producer_queue = Queue()

    def update_MaxSyringeFillLevel(self, MaxSyringeFillLevel: float, queue: Optional[Queue[float]] = None):
        """
        The maximum amount of fluid that the syringe can hold.

        This method updates the observable property 'MaxSyringeFillLevel'.
        """
        if queue is None:
            queue = self._MaxSyringeFillLevel_producer_queue
        queue.put(MaxSyringeFillLevel)

    def MaxSyringeFillLevel_on_subscription(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> Optional[Queue[float]]:
        """
        The maximum amount of fluid that the syringe can hold.

        This method is called when a client subscribes to the observable property 'MaxSyringeFillLevel'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    def update_SyringeFillLevel(self, SyringeFillLevel: float, queue: Optional[Queue[float]] = None):
        """
        The current amount of fluid left in the syringe.

        This method updates the observable property 'SyringeFillLevel'.
        """
        if queue is None:
            queue = self._SyringeFillLevel_producer_queue
        queue.put(SyringeFillLevel)

    def SyringeFillLevel_on_subscription(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> Optional[Queue[float]]:
        """
        The current amount of fluid left in the syringe.

        This method is called when a client subscribes to the observable property 'SyringeFillLevel'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    def update_MaxFlowRate(self, MaxFlowRate: float, queue: Optional[Queue[float]] = None):
        """
        The maximum value of the flow rate at which this pump can dose a fluid.

        This method updates the observable property 'MaxFlowRate'.
        """
        if queue is None:
            queue = self._MaxFlowRate_producer_queue
        queue.put(MaxFlowRate)

    def MaxFlowRate_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Optional[Queue[float]]:
        """
        The maximum value of the flow rate at which this pump can dose a fluid.

        This method is called when a client subscribes to the observable property 'MaxFlowRate'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    def update_FlowRate(self, FlowRate: float, queue: Optional[Queue[float]] = None):
        """
        The current value of the flow rate. It is 0 if the pump does not dose any fluid.

        This method updates the observable property 'FlowRate'.
        """
        if queue is None:
            queue = self._FlowRate_producer_queue
        queue.put(FlowRate)

    def FlowRate_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Optional[Queue[float]]:
        """
        The current value of the flow rate. It is 0 if the pump does not dose any fluid.

        This method is called when a client subscribes to the observable property 'FlowRate'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    @abstractmethod
    def StopDosage(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> StopDosage_Responses:
        """
        Stops a currently running dosage immediately.


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def SetFillLevel(
        self,
        FillLevel: float,
        FlowRate: float,
        *,
        metadata: Dict[FullyQualifiedIdentifier, Any],
        instance: ObservableCommandInstance,
    ) -> SetFillLevel_Responses:
        """
        Pumps fluid with the given flow rate until the requested fill level is reached.
                Depending on the requested fill level given in the FillLevel parameter this function may cause aspiration or dispension of fluid.


        :param FillLevel: The requested fill level. A level of 0 indicates a completely empty syringe. The value has to be between 0 and MaxSyringeFillLevel. Depending on the requested fill level this may cause aspiration or dispension of fluid.

        :param FlowRate: The flow rate at which the pump should dose the fluid.

        :param metadata: The SiLA Client Metadata attached to the call
        :param instance: The command instance, enabling sending status updates to subscribed clients

        """
        pass

    @abstractmethod
    def DoseVolume(
        self,
        Volume: float,
        FlowRate: float,
        *,
        metadata: Dict[FullyQualifiedIdentifier, Any],
        instance: ObservableCommandInstance,
    ) -> DoseVolume_Responses:
        """
        Dose a certain amount of volume with the given flow rate.


        :param Volume: The amount of volume to dose. This value can be negative. In that case the pump aspirates the fluid.

        :param FlowRate: The flow rate at which the pump should dose the fluid.

        :param metadata: The SiLA Client Metadata attached to the call
        :param instance: The command instance, enabling sending status updates to subscribed clients

        """
        pass

    @abstractmethod
    def GenerateFlow(
        self, FlowRate: float, *, metadata: Dict[FullyQualifiedIdentifier, Any], instance: ObservableCommandInstance
    ) -> GenerateFlow_Responses:
        """
        Generate a continuous flow with the given flow rate. Dosing continues until it gets stopped manually by calling StopDosage or until the pusher reached one of its limits.


        :param FlowRate: The flow rate at which the pump should dose the fluid. This value can be negative. In that case the pump aspirates the fluid.

        :param metadata: The SiLA Client Metadata attached to the call
        :param instance: The command instance, enabling sending status updates to subscribed clients

        """
        pass

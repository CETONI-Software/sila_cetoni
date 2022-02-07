from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase, ObservableCommandInstance

from .continuousflowdosingservice_types import GenerateFlow_Responses, StopDosage_Responses


class ContinuousFlowDosingServiceBase(FeatureImplementationBase, ABC):

    _MaxFlowRate_producer_queue: Queue[float]

    _FlowRate_producer_queue: Queue[float]

    def __init__(self):
        """

                Allows to continuously dose a specified fluid.
        The continuous flow mode is meant for dispensing volumes or generating flows and works only in one direction. That means using negative flow rates or negative volumes for aspiration is not possible.

        """

        self._MaxFlowRate_producer_queue = Queue()

        self._FlowRate_producer_queue = Queue()

    def update_MaxFlowRate(self, MaxFlowRate: float):
        """
        The maximum value of the flow rate at which this pump can dose a fluid.

        This method updates the observable property 'MaxFlowRate'.
        """
        self._MaxFlowRate_producer_queue.put(MaxFlowRate)

    def MaxFlowRate_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        The maximum value of the flow rate at which this pump can dose a fluid.

        This method is called when a client subscribes to the observable property 'MaxFlowRate'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass

    def update_FlowRate(self, FlowRate: float):
        """
        The current value of the flow rate. It is 0 if the pump does not dose any fluid.

        This method updates the observable property 'FlowRate'.
        """
        self._FlowRate_producer_queue.put(FlowRate)

    def FlowRate_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        The current value of the flow rate. It is 0 if the pump does not dose any fluid.

        This method is called when a client subscribes to the observable property 'FlowRate'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
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
    def GenerateFlow(
        self, FlowRate: float, *, metadata: Dict[FullyQualifiedIdentifier, Any], instance: ObservableCommandInstance
    ) -> GenerateFlow_Responses:
        """
        Generate a continuous flow with the given flow rate. Dosing continues until it gets stopped manually by calling StopDosage.



        :param FlowRate: The flow rate at which the pump should dose the fluid. This value cannot be negative since dosing is meant to only work in one direction.


        :param metadata: The SiLA Client Metadata attached to the call
        :param instance: The command instance, enabling sending status updates to subscribed clients

        """
        pass

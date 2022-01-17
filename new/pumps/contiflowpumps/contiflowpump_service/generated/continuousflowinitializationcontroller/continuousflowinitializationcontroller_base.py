from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase, ObservableCommandInstance

from .continuousflowinitializationcontroller_types import InitializeContiflow_Responses


class ContinuousFlowInitializationControllerBase(FeatureImplementationBase, ABC):

    _IsInitialized_producer_queue: Queue[bool]

    def __init__(self):
        """
        Allows to initialize a contiflow pump before starting the continuous flow.
        """

        self._IsInitialized_producer_queue = Queue()

    def update_IsInitialized(self, IsInitialized: bool):
        """
                Returns true, if the continuous fow pump is initialized and ready for continuous flow start.
        Use this function to check if the pump is initialized before you start a continuous flow. If you change and continuous flow parameter, like valve settings, cross flow duration and so on, the pump will leave the initialized state. That means, after each parameter change, an initialization is required. Changing the flow rate or the dosing volume does not require and initialization.


                This method updates the observable property 'IsInitialized'.
        """
        self._IsInitialized_producer_queue.put(IsInitialized)

    def IsInitialized_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
                Returns true, if the continuous fow pump is initialized and ready for continuous flow start.
        Use this function to check if the pump is initialized before you start a continuous flow. If you change and continuous flow parameter, like valve settings, cross flow duration and so on, the pump will leave the initialized state. That means, after each parameter change, an initialization is required. Changing the flow rate or the dosing volume does not require and initialization.


                This method is called when a client subscribes to the observable property 'IsInitialized'

                :param metadata: The SiLA Client Metadata attached to the call
                :return:
        """
        pass

    @abstractmethod
    def InitializeContiflow(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any], instance: ObservableCommandInstance
    ) -> InitializeContiflow_Responses:
        """
                Initialize the continuous flow pump.
        Call this command after all parameters have been set, to prepare the conti flow pump for the start of the continuous flow. The initialization procedure ensures, that the syringes are sufficiently filled to start the continuous flow. So calling this command may cause a syringe refill if the syringes are not sufficiently filled. So before calling this command you should ensure, that syringe refilling properly works an can be executed. If you have a certain syringe refill procedure, you can also manually refill the syringes with the normal syringe pump functions. If the syringes are sufficiently filled if you call this function, no refilling will take place.



                :param metadata: The SiLA Client Metadata attached to the call
                :param instance: The command instance, enabling sending status updates to subscribed clients

        """
        pass

from __future__ import annotations

from typing import Iterable, Optional

from continuousflowinitializationcontroller_types import InitializeContiflow_Responses
from sila2.client import ClientMetadataInstance, ClientObservableCommandInstance, ClientObservableProperty

class ContinuousFlowInitializationControllerClient:
    """
    Allows to initialize a contiflow pump before starting the continuous flow.
    """

    IsInitialized: ClientObservableProperty[bool]
    """
    Returns true, if the continuous fow pump is initialized and ready for continuous flow start.
Use this function to check if the pump is initialized before you start a continuous flow. If you change and continuous flow parameter, like valve settings, cross flow duration and so on, the pump will leave the initialized state. That means, after each parameter change, an initialization is required. Changing the flow rate or the dosing volume does not require and initialization.
        
    """
    def InitializeContiflow(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> ClientObservableCommandInstance[None, InitializeContiflow_Responses]:
        """
                Initialize the continuous flow pump.
        Call this command after all parameters have been set, to prepare the conti flow pump for the start of the continuous flow. The initialization procedure ensures, that the syringes are sufficiently filled to start the continuous flow. So calling this command may cause a syringe refill if the syringes are not sufficiently filled. So before calling this command you should ensure, that syringe refilling properly works an can be executed. If you have a certain syringe refill procedure, you can also manually refill the syringes with the normal syringe pump functions. If the syringes are sufficiently filled if you call this function, no refilling will take place.

        """
        ...

from __future__ import annotations

from typing import Iterable, Optional

from balanceservice_types import Tare_Responses
from sila2.client import ClientMetadataInstance, ClientObservableProperty

class BalanceServiceClient:
    """
    Provides an interface to a balance to read its current value and tare the balance if necessary
    """

    Value: ClientObservableProperty[float]
    """
    The current value
    """
    def Tare(self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None) -> Tare_Responses:
        """
        Tare the balance
        """
        ...

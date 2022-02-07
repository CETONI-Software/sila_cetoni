from __future__ import annotations

from sila2.client import ClientMetadata, ClientUnobservableProperty

class ValveGatewayServiceClient:
    """
    Provides means to access individual valves of a valve terminal
    """

    NumberOfValves: ClientUnobservableProperty[int]
    """
    The number of valves of a terminal
    """

    ValveIndex: ClientMetadata[int]
    """
    The index of a single valve of a valve terminal. This value is 0-indexed, i.e. the first valve has index 0, the second one index 1 and so on.
    """

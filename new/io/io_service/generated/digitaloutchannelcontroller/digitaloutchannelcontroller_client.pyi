from __future__ import annotations

from typing import Iterable, Optional

from digitaloutchannelcontroller_types import SetOutput_Responses
from sila2.client import ClientMetadata, ClientMetadataInstance, ClientObservableProperty, ClientUnobservableProperty

from .digitaloutchannelcontroller_types import State

class DigitalOutChannelControllerClient:
    """
    Allows to control one digital output channel of an I/O module
    """

    NumberOfChannels: ClientUnobservableProperty[int]
    """
    The number of digital output channels.
    """

    State: ClientObservableProperty[State]
    """
    The state of the channel.
    """

    ChannelIndex: ClientMetadata[int]
    """
    The index of the channel that should be used. This value is 0-indexed, i.e. the first channel has index 0, the second one index 1 and so on.
    """
    def SetOutput(
        self, State: State, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> SetOutput_Responses:
        """
        Switch a digital output channel on or off.
        """
        ...

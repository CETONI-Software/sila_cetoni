"""
________________________________________________________________________

:PROJECT: SiLA2_python

*Qmix Error*

:details: Qmix Error:
    Provides a bridge from a DeviceError from QmixSDK to a SiLA Execution Error

:file:    qmix_error.py
:authors: Florian Meinicke
:date (creation)          2020-10-09
:date (last modification) 2020-10-09
________________________________________________________________________
"""

from sila2lib.error_handling.server_err import *

from qmixsdk.qmixbus import DeviceError


#-----------------------------------------------------------------------------
# Common
class QmixSDKSiLAError(SiLAExecutionError):
    """
    An unexpected error that was thrown by the QmixSDK during the execution of a command.
    Basically maps an error from QmixSDK to a SiLA Undefined Execution Error.
    """

    def __init__(self, qmixsdk_error: DeviceError = None):
        msg = f"The QmixSDK threw an unexpected error {qmixsdk_error}"

        super().__init__(msg=msg, error_identifier=None)

#-----------------------------------------------------------------------------
# Valves
class ValvePositionOutOfRangeError(SiLAValidationError):
    """
    The requested valve position is not in the valid range for this valve.
    """

    def __init__(self, msg: str = None):
        super().__init__(
            parameter="sila2.de.cetoni.valves.valvepositioncontroller.v1.Position",
            msg=msg
        )

class ValveNotToggleableError(SiLAExecutionError):
    """
    The current valve does not support toggling because it has more than only two possible positions.
    """

    def __init__(self):
        msg = "The current valve does not support toggling because it has more than only two possible positions."
        super().__init__(error_identifier="ValveNotToggleable", msg=msg)

class ValvePositionNotAvailableError(SiLAExecutionError):
    """
    The actual position of the current valve cannot be retrieved. This is most
    likely a temporary error that can be fixed by setting a specific valve position.
    """

    def __init__(self):
        msg = "The actual position of the current valve cannot be retrieved. " \
              "This is most likely a temporary error that can be fixed by setting a specific valve position."
        super().__init__(error_identifier="ValvePositionNotAvailable", msg=msg)


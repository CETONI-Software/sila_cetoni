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

from sila2lib.error_handling.server_err import SiLAExecutionError

from qmixsdk.qmixbus import DeviceError


class QmixSDKError(SiLAExecutionError):
    """
    An unexpected error that was thrown by the QmixSDK during the execution of a command.
    """

    def __init__(self, qmixsdk_error: DeviceError = None):
        msg = f"The QmixSDK threw an unexpected error {qmixsdk_error}"

        super().__init__(msg=msg, error_identifier=None)


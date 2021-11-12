"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Shutdown Controller_defined_errors*

:details: ShutdownController Defined SiLA Error factories:
    Provides a generic way of telling a SiLA2 server that it is about to be shut down. The server implements a routine
    to be executed before the hardware is shut down (e.g. saving device parameters or bringing the device into a safe
    position).

:file:    ShutdownController_defined_errors.py
:authors: Florian Meinicke

:date: (creation)          2021-07-09T10:33:28.765642
:date: (last modification) 2021-07-09T10:33:28.765642

.. note:: Code generated by sila2codegenerator 0.3.6

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

__version__ = "0.1.0"

# import general packages
from sila2lib.error_handling.server_err import SiLAExecutionError

class ShutdownFailedError(SiLAExecutionError):
    """
    The shutdown routine could not be executed properly.
    Thus the server might not be ready to be physically shutdown.
    """

    def __init__(self, extra_message: str = ""):
        """

        :param extra_message: extra message, that can be added to the default message
        :returns: SiLAExecutionError
        """

        msg = "The shutdown routine could not be executed properly." \
              "Thus the server might not be ready to be physically shutdown." \
              + (f'\n{extra_message}' if extra_message else "")
        super().__init__(error_identifier="de.cetoni/core/ShutdownController/v1/DefinedError/ShutdownFailed",
                        msg=msg)


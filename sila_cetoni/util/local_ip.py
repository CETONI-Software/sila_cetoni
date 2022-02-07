"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Local IP*

:details: Local IP:
    A helper script that retrieves the local IP address of the device in its network

:file:    local_ip.py
:authors: Florian Meinicke

:date: (creation)          2020-10-15
:date: (last modification) 2020-10-15

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
import socket

LOCAL_IP: str

# get local IP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect(('1.2.3.4', 80))
    LOCAL_IP = s.getsockname()[0]


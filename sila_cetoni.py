#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: sila_cetoni

*SiLA CETONI*

:details: SiLA CETONI:
    A wrapper script that starts as many individual SiLA2 servers as there are devices in the given configuration.

:file:    sila_cetoni.py
:authors: Florian Meinicke

:date: (creation)          2020-10-08
:date: (last modification) 2021-07-15

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

__version__ = "0.1.0"

import sys
import argparse
import logging
try:
    import coloredlogs
except ModuleNotFoundError:
    print("Cannot find coloredlogs! Please install coloredlogs, if you'd like to have nicer logging output:")
    print("`pip install coloredlogs`")

# adjust PATH to point to QmixSDK
sys.path.append("C:/QmixSDK/lib/python")
sys.path.append("C:/CETONI_SDK/lib/python")

from application.application import Application

#-----------------------------------------------------------------------------
# main program
def parse_command_line():
    """
    Just looking for command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Launches as many SiLA 2 servers as there are Qmix devices in the configuration")
    parser.add_argument('config_path', metavar='configuration_path', type=str,
                        help="""a path to a valid Qmix configuration folder
                             (If you don't have a configuration yet,
                             create one with the QmixElements software first.)""")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    return parser.parse_args()


if __name__ == '__main__':
    logging_level = logging.DEBUG # or use logging.ERROR for less output
    try:
        coloredlogs.install(fmt='%(asctime)s %(levelname)-8s| %(module)s.%(funcName)s: %(message)s',
                            level=logging_level)
    except NameError:
        logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging_level)

    parsed_args = parse_command_line()

    app = Application(parsed_args.config_path)
    app.run()

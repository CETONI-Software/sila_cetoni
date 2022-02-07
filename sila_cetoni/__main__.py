__version__ = "0.1.0"

import argparse
import logging
try:
    import coloredlogs
except ModuleNotFoundError:
    print("Cannot find coloredlogs! Please install coloredlogs, if you'd like to have nicer logging output:")
    print("`pip install coloredlogs`")

from .application.application import Application, DEFAULT_BASE_PORT

#-----------------------------------------------------------------------------
# main program
def parse_command_line():
    """
    Just looking for command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Launches as many SiLA 2 servers as there are CETONI devices in the configuration")
    parser.add_argument('-c', '--config_path', type=str, default='',
                        help="Path to a valid CETONI device configuration folder \
                             (This is only necessary if you want to control CETONI \
                             devices. Controlling other devices that have their \
                             own drivers in the 'device_drivers' subdirectory don't \
                             need a configuration.If you don't have a configuration \
                             yet, create one with the CETONI Elements software first.)")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-p', '--server-base-port', action='store', default=DEFAULT_BASE_PORT,
                        help='The port number for the first SiLA server (default: %d)' % DEFAULT_BASE_PORT)
    return parser.parse_args()


if __name__ == '__main__':
    logging_level = logging.DEBUG # or use logging.ERROR for less output
    LOGGING_FORMAT = '%(asctime)s [%(threadName)-12.12s] %(levelname)-8s| %(module)s.%(funcName)s: %(message)s'
    try:
        coloredlogs.install(fmt=LOGGING_FORMAT, level=logging_level)
    except NameError:
        logging.basicConfig(format=LOGGING_FORMAT, level=logging_level)

    parsed_args = parse_command_line()

    app = Application(parsed_args.config_path, int(parsed_args.server_base_port))
    app.run()

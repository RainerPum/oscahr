#!/usr/bin/env python3

"""Proxy main of the OSCAHR proxy scenario.

This module is the main wrapper to start the OSCAHR proxy scenario proxy (server). 

Version: 0.3.2
Date: 13.07.2021
Author: Simon Birngruber (IoT-Lab, University of Applied Sciences Upper Austria, Campus Hagenberg)
License: MIT
"""

# Standard library imports
import argparse
import logging
import sys
import traceback
import os

# define library locations
script_dir = os.path.dirname(__file__)
project_root = os.path.join(script_dir, '..')
sys.path.append(project_root)

# Local application imports
from common.config import OscahrConfig
from proxy import Proxy

# Module variables
_log = logging.getLogger()  # get root logger


def main():
    """Main function to start the OSCAHR proxy of the proxy scenario."""

    parser = argparse.ArgumentParser(description="Start OSCAHR proxy scenario in proxy mode.")
    parser.add_argument("-m", "--manage", action="store_true",
                        help="manage smart home devices (add/delete/modify)")
    parser.add_argument("-o", "--orbot", action="store_true", help="start automatically in orbot mode")
    logging_group = parser.add_mutually_exclusive_group()
    logging_group.add_argument("-v", "--verbose", action="store_true",
                               help="increase output verbosity to debug level")
    logging_group.add_argument("-s", "--silent", action="store_true",
                               help="deactivate console log output")
    args = parser.parse_args()

    try:
        # When started in management mode, enable client log mode (simply pass args value)
        oscahr_config = OscahrConfig("proxy", verbose=args.verbose, client=args.manage, silent=args.silent)

        if args.manage:
            Proxy(oscahr_config).manage_devices()
        elif args.orbot:
            Proxy(oscahr_config).orbot_mode()
        else:
            Proxy(oscahr_config).start_proxy()

    except KeyboardInterrupt:
        _log.debug("Interrupted by user!")
    except Exception as error:
        _log.error(f"A {type(error).__name__} occured: {error} in {traceback.print_exc()}")
    finally:
        oscahr_config.cleanup()
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())

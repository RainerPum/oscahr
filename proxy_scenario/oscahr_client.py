#!/usr/bin/env python3

"""Client main of the OSCAHR proxy scenario.

This module is the main wrapper to start the OSCAHR proxy scenario client. 

Version: 0.3.2
Date: 13.07.2021
Author: Simon Birngruber (IoT-Lab, University of Applied Sciences Upper Austria, Campus Hagenberg)
License: MIT
"""

# Standard library imports
import argparse
import logging
import sys

# Local application imports
from client import Client
from common.config import OscahrConfig

# Module variables
_log = logging.getLogger()  # get root logger


def main():
    """Main function to start the OSCAHR client of the proxy scenario."""

    parser = argparse.ArgumentParser(description="Start OSCAHR proxy scenario in client mode.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity to debug level")
    args = parser.parse_args()

    try:
        oscahr_config = OscahrConfig("proxy_client", verbose=args.verbose, client=True)
        
        Client(oscahr_config).start_client()

    except KeyboardInterrupt:
        _log.debug("Interrupted by user!")
    except Exception as error:
        _log.error(f"A {type(error).__name__} occured: {error}")
    finally:
        oscahr_config.cleanup()
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())

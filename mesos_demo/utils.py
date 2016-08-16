#!/usr/bin/env python

import sys
import logging
import coloredlogs

logger = logging.getLogger("mesos_demo")
coloredlogs.install(level="DEBUG")


def gracefully_exit(signal, frame):
    logger.warn("You have pressed Ctrl + C, and I will exit...")
    sys.exit(130)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import argh

from executor import run_shell, run_docker, run_hadoop
from utils import gracefully_exit, logger


ONE_LEVEL_COMMANDS = [
    run_shell,
    run_docker,
    run_hadoop,
]


def main():
    signal.signal(signal.SIGINT, gracefully_exit)

    logger.debug("Demo >>> start...")
    parser = argh.ArghParser()
    parser.add_commands(ONE_LEVEL_COMMANDS)
    parser.dispatch()
    logger.debug("Demo >>> finish...")


if __name__ == "__main__":
    main()

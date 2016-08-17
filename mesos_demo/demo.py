#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argh

from subcommands import run_shell, run_docker, run_hadoop
from utils import logger


ONE_LEVEL_COMMANDS = [
    run_shell,
    run_docker,
    run_hadoop,
]


def main():
    logger.debug("Demo >>> start...")
    parser = argh.ArghParser()
    parser.add_commands(ONE_LEVEL_COMMANDS)
    parser.dispatch()
    logger.debug("Demo >>> finish...")


if __name__ == "__main__":
    main()

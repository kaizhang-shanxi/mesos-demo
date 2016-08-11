#!/usr/bin/env python

import sys


def gracefully_exit(signal, frame):
    print("You have pressed Ctrl + C, and I will exit...")
    sys.exit(130)

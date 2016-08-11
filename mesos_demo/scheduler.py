#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mesos.interface
import mesos.native
from mesos.interface import mesos_pb2


class Scheduler(mesos.interface.Scheduler):
    def __init__(self):
        logger.debug("Scheduler >>> initiating...")
        self.__driver = mesos.native.MesosSchedulerDriver()


    framework = mesos_pb2.FrameworkInfo()
    framework.user = ""     # Mesos 填写
    framework.name = "Mesos Demo"

    driver = mesos.native.MesosSchedulerDriver(framework, mesos_addr)

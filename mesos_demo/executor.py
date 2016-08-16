#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argh
import mesos.native
from mesos.interface import mesos_pb2

from scheduler import Scheduler
from utils import logger


@argh.arg("-m", "--mesos-master",
          default="zk://192.168.78.21:2181,192.168.78.22:2181,192.168.78.25:2181/mesos",
          help="the address of mesos masters")
@argh.arg("--cpus", default=0.1, type=float, help="the cpus task needed")
@argh.arg("--mem", default=32, type=float, help="the memory task needed")
def run_shell(**kwargs):
    logger.debug("run_shell >>> begin...")
    logger.debug("mesos_master >>> {}".format(kwargs["mesos_master"]))

    framework = mesos_pb2.FrameworkInfo()
    framework.user = ""     # Mesos 填写
    framework.name = "Mesos Demo Run Shell"

    driver = mesos.native.MesosSchedulerDriver(Scheduler(), framework,
                                               kwargs["mesos_master"])
    driver.run()


def run_hadoop():
    pass


def run_docker():
    pass

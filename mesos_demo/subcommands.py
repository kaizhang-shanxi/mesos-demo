#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argh
import signal
import mesos.native
from mesos.interface import mesos_pb2

import os
import sys
import time
from threading import Thread

from scheduler import Scheduler
from utils import logger


@argh.arg("-m", "--mesos-master",
          default="zk://192.168.78.21:2181,192.168.78.22:2181,192.168.78.25:2181/mesos",
          help="the address of mesos masters")
@argh.arg("--cpus", default=0.1, type=float, help="the cpus task needed")
@argh.arg("--mem", default=32, type=float, help="the memory task needed")
@argh.arg("--ip", help="host ip")
def run_shell(**kwargs):
    logger.debug("run_shell >>> start...")
    logger.debug("mesos_master >>> {}".format(kwargs["mesos_master"]))

    framework = mesos_pb2.FrameworkInfo()
    framework.user = ""     # Mesos 填写
    framework.name = "Mesos Demo Run Shell"

    # os.environ["LIBPROCESS_IP"] = "192.168.78.21"
    os.environ["LIBPROCESS_IP"] = kwargs["ip"]
    # logger.debug("LIBPROCESS_IP >>> {}".format(os.environ["LIBPROCESS_IP"]))

    # baseUri = "/app/mesos-demo/mesos_demo/"
    baseUri = os.path.dirname(os.path.realpath(__file__))
    # baseUri = "https://github.com/kaizhang-shanxi/mesos-demo/tree/master/mesos_demo"
    # logger.debug("baseUri >>> {}".format(baseUri))
    # logger.debug("file >>> {}".format(__file__))
    # logger.debug("realpath >>> {}".format(os.path.realpath(__file__)))
    # logger.debug("dirname >>> {}".format(os.path.dirname(os.path.realpath(__file__))))
    uris = ["executor.py", "utils.py"]
    uris = [os.path.join(baseUri, uri) for uri in uris]

    executor = mesos_pb2.ExecutorInfo()
    executor.executor_id.value = "default"
    executor.command.value = "python executor.py"
    executor.name = "Mesos Demo Executor"

    for uri in uris:
        uri_proto = executor.command.uris.add()
        uri_proto.value = uri
        uri_proto.extract = False

    driver = mesos.native.MesosSchedulerDriver(Scheduler(executor), framework,
                                               kwargs["mesos_master"])

    framework_thread = Thread(target=run_driver_async, args=(driver,))
    framework_thread.start()

    def gracefully_exit(signal, frame):
        logger.warn("You have pressed Ctrl + C, and I will exit...")
        # logger.debug("frame >>> {}".format(frame.__dict__))
        driver.stop()
        sys.exit(130)

    logger.debug("Listen for Ctrl + C...")
    signal.signal(signal.SIGINT, gracefully_exit)

    while framework_thread.is_alive():
        time.sleep(1)
    '''
    '''


def run_hadoop():
    pass


def run_docker():
    pass


def run_driver_async(driver):
    status = 0 if driver.run() == mesos_pb2.DRIVER_STOPPED else 1
    driver.stop()
    sys.exit(status)

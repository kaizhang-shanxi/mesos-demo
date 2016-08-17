#!/usr/bin/env python
# -*- coding: utf-8 -*-


import mesos.interface
from mesos.interface import mesos_pb2
import mesos.native

import threading
import sys

from utils import logger


class Executor(mesos.interface.Executor):
    def __init__(self):
        pass

    def launchTask(self, driver, task):
        def run_task():
            logger.info("Running task >>> {}".format(task.task_id.value))
            update = mesos_pb2.TaskStatus()
            update.task_id.value = task.task_id.value
            update.state = mesos_pb2.TASK_RUNNING
            update.data = "kai >>> demo >>> running"
            driver.sendStatusUpdate(update)

            logger.debug("Hello, world.")
            print("Hello, world.")

            logger.info("Sending status update...")
            update = mesos_pb2.TaskStatus()
            update.task_id.value = task.task_id.value
            update.state = mesos_pb2.TASK_FINISHED
            update.data = "kai >>> demo >>> finished"
            driver.sendStatusUpdate(update)
            logger.info("Sent status update")

        thread = threading.Thread(target=run_task)
        thread.start()

    def frameworkMessage(self, driver, message):
        logger.info("Executor >>> frameworkMessage >>> start...")
        driver.sendFrameworkMessage(message)

    def registered(self, driver, executorInfo, frameworkInfo, slaveInfo):
        logger.info("RenderExecutor registered")

    def reregistered(self, driver, slaveInfo):
        logger.info("RenderExecutor reregistered")

    def disconnected(self, driver):
        logger.info("RenderExecutor disconnected")


if __name__ == "__main__":
    logger.info("executor >>> start...")
    driver = mesos.native.MesosExecutorDriver(Executor())
    sys.exit(0 if driver.run() == mesos_pb2.DRIVER_STOPPED else 1)

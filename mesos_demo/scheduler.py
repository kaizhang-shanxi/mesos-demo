#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mesos.interface
import mesos.native
from mesos.interface import mesos_pb2
from collections import namedtuple

from utils import logger

TASKS_NUM = 3
TASK_CPUS = 0.1
TASK_MEM = 32

class Scheduler(mesos.interface.Scheduler):
    Resource = namedtuple("Resource", ["cpus", "mem"])

    def __init__(self):
        logger.debug("Scheduler >>> initiating...")
        self.__tasksData = {}
        self.__tasksLaunched = 0
        self.__tasksFinished = 0

    def registered(self, driver, frameworkId, masterInfo):
        logger.info("Registered with framework ID {}".
                    format(frameworkId.value))
        logger.debug("registered >>> masterInfo >>> {}".format(masterInfo))

    def resourceOffers(self, driver, offers):
        logger.info("resourceOffers >>> begin...")
        logger.debug("Received resource offers: {}".
                     format([o.id.value for o in offers]))
        for offer in offers:
            tasks = []
            resource = self.__calculate_resource(offer)
            logger.info("Received offer: {}".format(resource))
            if self.__tasksLaunched < TASKS_NUM:
                task = self.__new_task(offer)
                tasks.append(task)

            operation = mesos_pb2.Offer.Operation()
            operation.type = mesos_pb2.Offer.Operation.LAUNCH
            operation.launch.task_infos.extend(tasks)
            driver.acceptOffers([offer.id], [operation])

    def statusUpdate(self, driver, update):
        logger.info("Task {} is in state {}".
                    format(update.task_id.value,
                           mesos_pb2.TaskState.Name(update.state)))
        logger.debug("update >>> {}".format(update))

    def frameworkMessage(self, driver, executorId, slaveId, message):
        logger.info("Received message: {}".format(message))

    def __calculate_resource(self, offer):
        offerCpus = 0
        offerMem = 0

        for resource in offer.resources:
            if resource.name == "cpus":
                offerCpus += resource.scalar.value
            elif resource.name == "mes":
                offerMem += resource.scalar.value

        return self.Resource(offerCpus, offerMem)

    def __new_task(self, offer):
        task_id = self.__tasksLaunched
        task = mesos_pb2.TaskInfo()
        task.task_id.value = str(task_id)
        task.slave_id.value = offer.slave_id.value
        task.name = "task {}".format(task_id)

        cpus = task.resources.add()
        cpus.name = "cpus"
        cpus.type = mesos_pb2.Value.SCALAR
        cpus.scalar.value = TASK_CPUS

        mem = task.resources.add()
        mem.name = "mem"
        mem.type = mesos_pb2.Value.SCALAR
        mem.scalar.value = TASK_MEM

        task.command.value = "echo hello world"

        return task

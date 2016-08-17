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

    def __init__(self, executor):
        logger.debug("Scheduler >>> initiating...")
        self.__executor = executor
        self.__tasksData = {}
        self.__tasksLaunched = 0
        self.__tasksFinished = 0
        self.__messagesReceived = 0

    def registered(self, driver, frameworkId, masterInfo):
        logger.info("Registered with framework ID {}".
                    format(frameworkId.value))
        # logger.debug("registered >>> masterInfo >>> {}".format(masterInfo))

    def resourceOffers(self, driver, offers):
        logger.info("resourceOffers >>> start...")
        logger.debug("Received resource offers: {}".
                     format([o.id.value for o in offers]))
        for offer in offers:
            tasks = []
            resource = self.__calculate_resource(offer)
            logger.info("Received offer: {}".format(resource))
            if self.__tasksLaunched < TASKS_NUM:
                task = self.__new_task(offer)
                tasks.append(task)
                self.__tasksData[task.task_id.value] = (offer.slave_id,
                                                        task.executor.executor_id)
                self.__tasksLaunched += 1
                logger.debug("tasks launched >>> {}".format(self.__tasksLaunched))

            if tasks:
                logger.info("Accepting offer {} on {}".format(offer.id,
                                                              offer.hostname))
                driver.launchTasks(offer.id, tasks)
            else:
                logger.info("Declining offer {} on {}".format(offer.id,
                                                              offer.hostname))
                driver.declineOffer(offer.id)

    def statusUpdate(self, driver, update):
        logger.info("Task {} is in state {}".
                    format(update.task_id.value,
                           mesos_pb2.TaskState.Name(update.state)))
        if update.state == mesos_pb2.TASK_FINISHED:
            self.__tasksFinished += 1
            logger.debug("tasks finished >>> {}".format(self.__tasksFinished))
            slave_id, executor_id = self.__tasksData[update.task_id.value]
            # logger.debug("slave_id >>> {}".format(slave_id))
            # logger.debug("executor_id >>> {}".format(executor_id))
            driver.sendFrameworkMessage(executor_id, slave_id, "Scheduler >>> statusUpdate >>> end.")

    def frameworkMessage(self, driver, executorId, slaveId, message):
        logger.info("Received message: {}".format(message))
        self.__messagesReceived += 1
        if self.__messagesReceived == TASKS_NUM:
            logger.info("Tasks finished.")
            driver.stop()

    def __calculate_resource(self, offer):
        offerCpus = 0
        offerMem = 0

        for resource in offer.resources:
            if resource.name == "cpus":
                offerCpus += resource.scalar.value
            elif resource.name == "mem":
                offerMem += resource.scalar.value

        return self.Resource(offerCpus, offerMem)

    def __new_task(self, offer):
        task_id = self.__tasksLaunched
        task = mesos_pb2.TaskInfo()
        task.task_id.value = str(task_id)
        task.slave_id.value = offer.slave_id.value
        task.name = "task {}".format(task_id)
        task.executor.MergeFrom(self.__executor)

        cpus = task.resources.add()
        cpus.name = "cpus"
        cpus.type = mesos_pb2.Value.SCALAR
        cpus.scalar.value = TASK_CPUS

        mem = task.resources.add()
        mem.name = "mem"
        mem.type = mesos_pb2.Value.SCALAR
        mem.scalar.value = TASK_MEM

        return task

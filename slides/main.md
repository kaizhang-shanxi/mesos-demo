% Mesos 介绍
% 张凯
% 2016 年 8 月 18 日

# Mesos 概述

## Mesos 是什么

- 官方说：它是一个分布式系统内核

- 我说：
    - 它能告诉外界有多少资源
    - 它能提供使用这些资源的接口

## 为什么要用 Mesos

- 性能方面
    - 线性扩容 --> 10, 000 个节点
    - 高可用性 --> 配合 Zookeeper 构成主备集群

- 与 LAIN 的结合方面
    - 原生支持 docker
    - 支持容器之外的应用 --> Hadoop

- 特色
    - 资源隔离 --> cpu，内存，硬盘，端口……
    - 跨平台

# Mesos 细究

## Mesos 的架构

![][mesos_architecture]

## Mesos 的工作过程

![][mesos_work_flow]

## 写 framework

## 重写 `Scheduler`

```python
class MyScheduler(mesos.interface.Scheduler):
    def __init__(self, executor):
        self.__executor = executor

    def registered(self, driver, frameworkId, masterInfo):
        pass

    def resourceOffers(self, driver, offers):
        pass

    def statusUpdate(self, driver, update):
        pass

    def frameworkMessage(self, driver, executorId, slaveId, message):
        pass
```

## 处理 `offer`

```python
    def resourceOffers(self, driver, offers):
        for offer in offers:
            tasks = []
            if self.__tasksLaunched < TASKS_NUM:
                # task = self.__new_task(offer)
                task = self.__new_docker_task(offer)
                tasks.append(task)
                self.__tasksLaunched += 1

            if tasks:
                driver.launchTasks(offer.id, tasks)
            else:
                driver.declineOffer(offer.id)
```

## 新建任务 -- 非 docker

```python
    def __new_task(self, offer):
        task_id = str(uuid.uuid4())
        task = mesos_pb2.TaskInfo()
        task.task_id.value = task_id
        task.slave_id.value = offer.slave_id.value
        task.executor.MergeFrom(self.__executor)

        cpus = task.resources.add()
        cpus.name = "cpus"
        cpus.type = mesos_pb2.Value.SCALAR
        cpus.scalar.value = TASK_CPUS

        mem = task.resources.add()
        # ...
        return task
```

## Executor

```python
    executor = mesos_pb2.ExecutorInfo()
    executor.command.value = "python executor.py"
```

`executor.py`

```python
class Executor(mesos.interface.Executor):
    def launchTask(self, driver, task):
        def run_task():
            print("Hello, task {}.".format(task.task_id.value))
        thread = threading.Thread(target=run_task)
        thread.start()

if __name__ == "__main__":
    driver = mesos.native.MesosExecutorDriver(Executor())
    sys.exit(0 if driver.run() == mesos_pb2.DRIVER_STOPPED else 1)
```

## 新建任务 -- docker

```python
    def __new_docker_task(self, offer):
        task = mesos_pb2.TaskInfo()
        task.slave_id.value = offer.slave_id.value

        container = mesos_pb2.ContainerInfo()
        container.type = 1  # mesos_pb2.ContainerInfo.Type.DOCKER

        docker = mesos_pb2.ContainerInfo.DockerInfo()
        docker.image = "python:3"
        docker.network = 2  # mesos_pb2.ContainerInfo.DockerInfo.Network.BRIDGE
        docker.force_pull_image = True

        docker_port = docker.port_mappings.add()
        docker_port.host_port = host_port
        docker_port.container_port = 8080

        container.docker.MergeFrom(docker)
        task.container.MergeFrom(container)

        command = mesos_pb2.CommandInfo()
        command.value = "python3 -m http.server 8080"
        task.command.MergeFrom(command)

        return task
```

## 一个演示

# Mesos 与 LAIN

## 与 LAIN 的结合

- Mesos <---> Swarm

- Mesos <--> LAIN framework for mesos <--> deployd <--> console

- 官方支持 C++、Java 和 Python 的接口

- 有 Golang 的非官方库，不确定是否最新

## Hadoop on mesos

未完待续。。。

# 谢谢大家 :)

[mesos_architecture]: ../img/mesos-architecture.jpg { width=80% }
[mesos_work_flow]: ../img/mesos-work-flow.jpg

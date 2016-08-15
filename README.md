# Moses Demo

## 安装与配置

### Master 节点（node1，node2）

#### 添加源

```
$ sudo rpm -Uvh http://repos.mesosphere.com/el/7/noarch/RPMS/mesosphere-el-repo-7-1.noarch.rpm
$ sudo yum update
```

#### 安装 Mesos、Zookeeper

```
$ sudo yum install mesos
$ sudo yum install mesosphere-zookeeper
```

#### 配置

##### Zookeeper

```
[vagrant@node1 ~]$ echo "1" | sudo tee /var/lib/zookeeper/myid  # 节点 1
[vagrant@node2 ~]$ echo "2" | sudo tee /var/lib/zookeeper/myid  # 节点 2
```

```
# 节点 1
[vagrant@node1 ~]$ sudo cp -i /etc/zookeeper/conf/zoo.cfg /etc/zookeeper/conf/zoo.cfg.origin
[vagrant@node1 ~]$ sudo tee -a /etc/zookeeper/conf/zoo.cfg <<EOF
# Custom Setup
server.1=192.168.78.21:2888:3888
server.2=192.168.78.22:2888:3888
EOF

# 节点 2
[vagrant@node2 ~]$ sudo cp -i /etc/zookeeper/conf/zoo.cfg /etc/zookeeper/conf/zoo.cfg.origin
[vagrant@node2 ~]$ sudo tee -a /etc/zookeeper/conf/zoo.cfg <<EOF
# Custom Setup
server.1=192.168.78.21:2888:3888
server.2=192.168.78.22:2888:3888
EOF
```

##### Mesos

```
# 节点 1
[vagrant@node1 ~]$ sudo cp -i /etc/mesos/zk /etc/mesos/zk.origin
[vagrant@node1 ~]$ echo "zk://192.168.78.21:2181,192.168.78.22:2181/mesos"|sudo tee /etc/mesos/zk

# 节点 2
[vagrant@node2 ~]$ sudo cp -i /etc/mesos/zk /etc/mesos/zk.origin
[vagrant@node2 ~]$ echo "zk://192.168.78.21:2181,192.168.78.22:2181/mesos"|sudo tee /etc/mesos/zk
```

```
# 节点 1
[vagrant@node1 ~]$ sudo cp -i /etc/mesos-master/quorum /etc/mesos-master/quorum.origin
[vagrant@node1 ~]$ echo $N | sudo tee /etc/mesos-master/quorum  # $N >= #{Master 节点}/2

# 节点 2
[vagrant@node2 ~]$ sudo cp -i /etc/mesos-master/quorum /etc/mesos-master/quorum.origin
[vagrant@node2 ~]$ echo $N | sudo tee /etc/mesos-master/quorum  # $N >= #{Master 节点}/2
```

#### 运行

```
# 节点 1
# 禁止 slave 服务
[vagrant@node1 ~]$ sudo systemctl stop mesos-slave
[vagrant@node1 ~]$ sudo systemctl disable mesos-slave

# 重启
[vagrant@node1 ~]$ sudo systemctl restart zookeeper
[vagrant@node1 ~]$ sudo systemctl restart mesos-master

# 节点 2
# 禁止 slave 服务
[vagrant@node2 ~]$ sudo systemctl stop mesos-slave
[vagrant@node2 ~]$ sudo systemctl disable mesos-slave

# 重启
[vagrant@node2 ~]$ sudo systemctl restart zookeeper
[vagrant@node2 ~]$ sudo systemctl restart mesos-master
```

### Agent 节点（node3，node4）

#### 添加源

```
$ sudo rpm -Uvh http://repos.mesosphere.com/el/7/noarch/RPMS/mesosphere-el-repo-7-1.noarch.rpm
$ sudo yum update
```

#### 安装 Mesos

```
$ sudo yum install mesos
```

#### 配置

```
# 节点 3
[vagrant@node3 ~]$ sudo cp -i /etc/mesos/zk /etc/mesos/zk.origin
[vagrant@node3 ~]$ echo "zk://192.168.78.21:2181,192.168.78.22:2181/mesos"|sudo tee /etc/mesos/zk
```

#### 运行

```
# 禁止 mesos-master 服务
[vagrant@node3 ~]$ sudo systemctl stop mesos-master
[vagrant@node3 ~]$ sudo systemctl disable mesos-master

# 重启
[vagrant@node3 ~]$ sudo systemctl restart mesos-slave
```

### 验证

```
[vagrant@node3 ~]$ MASTER=$(mesos-resolve `cat /etc/mesos/zk`)
[vagrant@node3 ~]$ mesos-execute --master=$MASTER --name="cluster-test" --command="sleep 5"
```

# vim: ft=ruby:

VAGRANTFILE_API_VERSION = "2"
HADOOP_VERSION = "2.7.0"
# PRIVATE_IP = "192.168.78.2?"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  (1..5).each do |i|
    nodename = "node#{i}"

    config.vm.define nodename do |node|
      node.vm.box = "centos/7"
      node.vm.hostname = nodename

      node.vm.provider "virtualbox" do |v|
        # v.cpus = i == 1 ? 2 : 1
        # v.memory = i == 1 ? 1024 : 512
        # v.memory = i == 3 ? 2048 : 512
        v.cpus = i == 1 ? 2 : 2
        v.memory = i == 1 ? 1024 : 4096
      end

      node.vm.network "private_network", ip: "192.168.78.2#{i}"
      node.vm.synced_folder "./", "/app/mesos-demo"
    end

  end

end

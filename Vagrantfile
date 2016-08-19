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
        v.memory = i == 1 ? 1536 : 512
        # v.memory = i == 3 ? 2048 : 512
      end

      node.vm.network "private_network", ip: "192.168.78.2#{i}"
      node.vm.synced_folder "./", "/app/mesos-demo"
    end

  end

end

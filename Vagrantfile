# vim: ft=ruby:

Vagrant.configure(2) do |config|

  (1..5).each do |i|
    nodename = "node#{i}"

    config.vm.define nodename do |node|
      node.vm.box = "centos/7"
      node.vm.hostname = nodename

      node.vm.provider "virtualbox" do |v|
        v.memory = i == 1 ? 1536 : 512
      end

      node.vm.network "private_network", ip: "192.168.78.2#{i}"
    end

  end

end

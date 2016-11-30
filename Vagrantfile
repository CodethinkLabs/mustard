Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/zesty64"
  config.vm.network "private_network", type: "dhcp"
  config.vm.synced_folder ".", "/src/mustard"
  config.vm.synced_folder "../content", "/src/mustard-example", create: true
  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    # vb.gui = true
    # Customize the VM:
    vb.memory = "1024"
    vb.cpus = "1"
  end

  config.vm.provision "shell", inline: <<-SHELL
    cd /src/mustard && sh ./install_dependencies.sh
    cd .. && git clone https://gitlab.com/trustable/baserock-mustard.git mustard-example
    cd /src/mustard
    ./mustard-render -b -r -j /src/mustard/plantuml.jar -p /src/mustard-example
  SHELL
end

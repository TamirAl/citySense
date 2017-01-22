# Install ethtool 
sudo apt-get -y install libssl-dev libnl-genl-3-dev libnl-3-dev iw ethtool

# Install aircrack
wget http://download.aircrack-ng.org/aircrack-ng-1.2-rc4.tar.gz
tar -zxvf aircrack-ng-1.2-rc4.tar.gz
make -C aircrack-ng-1.2-rc4
sudo make install -C aircrack-ng-1.2-rc4
rm aircrack-ng-1.2-rc4.tar.gz
rm -rf aircrack-ng-1.2-rc4.tar.gz

sudo airodump-ng-oui-update

# Install iw to get your wifi card to monitor mode:
apt-get -y install iw


# Install zookeeperd 
sudo apt-get install zookeeperd 

# Install Kafka 
mkdir -p ~/Downloads
wget "http://mirror.cc.columbia.edu/pub/software/apache/kafka/0.10.1.1/kafka_2.11-0.10.1.1.tgz" -O ~/Downloads/kafka.tgz
mkdir -p ~/kafka && cd ~/kafka
tar -xvzf ~/Downloads/kafka.tgz --strip 1

# Start zookeeper
# /usr/share/zookeeper/bin/zkServer.sh start-foreground 

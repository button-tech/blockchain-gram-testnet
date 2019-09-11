#!/bin/bash
export DEBCONF_FRONTEND=noninteractive
apt-get -y purge console-setup
apt-get update
apt-get -o Dpkg::Options::="--force-confold" -o Dpkg::Options::="--force-confdef" install -yq libghc-zlib-dev gperf build-essential make wget libreadline-dev git ccache libmicrohttpd-dev libssl-dev cmake libgflags-dev --allow-downgrades --allow-remove-essential --allow-change-held-packages
apt-get -o Dpkg::Options::="--force-confold" -o Dpkg::Options::="--force-confdef" dist-upgrade -yq
cd /root
git clone --recurse-submodules -j8 https://github.com/ton-blockchain/ton
mkdir /root/ton-build
cd /root/ton-build
cmake /root/ton
cmake --build . --target validator-engine
mkdir /var/ton-work
mkdir /var/ton-work/db
mkdir /var/ton-work/etc
mkdir /var/log/ton-node
chmod 775 /var/log/ton-node
chmod 775 -R /var/ton-work
cd /var/ton-work/etc
wget https://test.ton.org/ton-global.config.json
myip=$(wget -qO- http://ipecho.net/plain | xargs echo)
/root/ton-build/validator-engine/validator-engine -C /var/ton-work/etc/ton-global.config.json --db /var/ton-work/db/ --ip ${myip}:1338 -l  /var/log/ton-node/log
cat << EOF > /etc/systemd/system/ton-node.service
[Unit]
Description=TON Node
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
User=root
ExecStart=/root/ton-build/validator-engine/validator-engine -C /var/ton-work/etc/ton-global.config.json --db /var/ton-work/db/ --ip ${myip}:1338 -l /var/log/ton-node/log
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable ton-node
service ton-node start

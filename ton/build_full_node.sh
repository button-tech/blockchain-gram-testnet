#!/bin/bash

apt-get update
apt-get install tmux fish libssl-dev zlib1g-dev cmake g++ less gperf -y
cd /root
wget https://test.ton.org/ton-blockchain-full.tar.xz
tar -xvf ton-blockchain-full.tar.xz
mkdir /root/ton-build
cd /root/ton-build
cmake /root/ton-node
make
mkdir /var/ton-work
mkdir /var/ton-work/db
mkdir /var/ton-work/etc
mkdir /var/log/ton-node
chmod 775 /var/log/ton-node
chmod 775 -R /var/ton-work
cd /var/ton-work/etc
wget https://test.ton.org/ton-global.config.json
myip=$(wget -qO- http://ipecho.net/plain | xargs echo)
cat << EOF > /etc/systemd/system/ton-node.service
[Unit]
Description=TON Node
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
User=root
ExecStart=/root/ton-build/validator-engine/validator-engine -C /var/ton-work/etc/ton-global.config.json --db /var/ton-work/db/ --ip ${myip}:3000 -l /var/log/ton-node/log
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
# service ton-node start

# for generate keypair
# /root/ton-build/utils/generate-random-id -m keys -n liteserver

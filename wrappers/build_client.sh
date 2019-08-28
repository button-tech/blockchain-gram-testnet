#!/bin/bash

# for debian dep
apt-get update && apt-get upgrade
apt-get install tmux fish libssl-dev zlib1g-dev cmake g++ less

# download tar and unpack
wget https://test.ton.org/ton-test-liteclient-full.tar.xz
tar -xvf ton-test-liteclient-full.tar.xz 

# build
mkdir liteclient-build
cd liteclient-build
cmake ../lite-client
cmake --build . --target lite-client
cmake --build . --target fift

# download config file for client
wget https://test.ton.org/ton-lite-client-test1.config.json
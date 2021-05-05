#!/bin/sh

sudo apt update && sudo apt upgrade -y

# install node
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
sudo ~/.nvm/nvm.sh install --lts
sudo ~/.nvm/nvm.sh use --lts

npm install -g bundle-phobia-cli

# install python
sudo apt install python3 python3-venv python3-pip -y

# Setup venv
python3 -m venv env
. env/bin/activate
pip3 install -r requirements.txt

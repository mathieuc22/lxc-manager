#!/bin/bash

export DEBIAN_FRONTEND=noninteractive
export TERM=xterm

apt-get update
apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    kitty-terminfo

# Installer Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | bash - &&\
apt-get install -y nodejs

# Installer et configurer git
apt-get update
apt-get install -y git
git config --global user.name "Mathieu Collet"
git config --global user.email "mathieu.collet@gmail.com"

echo "Environnement Node.js et npm configuré avec succès"

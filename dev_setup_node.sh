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

echo "Environnement Node.js et npm configuré avec succès"

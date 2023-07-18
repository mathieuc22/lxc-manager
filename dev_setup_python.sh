#!/bin/bash

export DEBIAN_FRONTEND=noninteractive
export TERM=xterm

apt-get update
apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libffi-dev \
    libssl-dev \
    python3-dev \
    python3-venv \
    zlib1g-dev \
    kitty-terminfo

# Crée un nouvel environnement virtuel Python
python3 -m venv /opt/venv

# Active l'environnement virtuel
source /opt/venv/bin/activate

# Met à jour pip, setuptools et wheel
pip install --upgrade pip setuptools wheel

# Installer et configurer git
apt-get update
apt-get install -y git
git config --global user.name "Mathieu Collet"
git config --global user.email "mathieu.collet@gmail.com"

echo "Environnement Python configuré avec succès"

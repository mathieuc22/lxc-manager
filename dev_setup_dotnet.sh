#!/bin/bash

export DEBIAN_FRONTEND=noninteractive
export TERM=xterm

# Mettre à jour les paquets et installer les dépendances
apt-get update
apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \
    kitty-terminfo

# Ajouter le référentiel Microsoft
wget https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb

# Installer .NET SDK
apt-get update
apt-get install -y dotnet-sdk-7.0

# Installer le runtime
apt-get update
apt-get install -y aspnetcore-runtime-7.0

echo "Environnement C# et .NET configuré avec succès"

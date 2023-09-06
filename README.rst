============================
Proxmox LXC Manager
============================

Ce projet est un gestionnaire de conteneurs LXC pour Proxmox. Il offre une interface CLI simple pour créer, démarrer et supprimer des conteneurs LXC pré-configurés pour différents environnements de développement.

Fonctionnalités
===============

* Création automatisée de conteneurs LXC pré-configurés pour Node.js, Python et .NET.
* Démarrage et arrêt de conteneurs LXC.
* Suppression de conteneurs LXC.
* Gestion de journalisation avec différents niveaux.

Installation
============

1. Clonez le dépôt :

   .. code-block:: bash

       git clone https://github.com/mathieuc22/proxmox-lxc-manager.git
       cd proxmox-lxc-manager

2. Installez les dépendances avec Poetry:

   .. code-block:: bash

       poetry install

3. Copiez le fichier `.env.example` en `.env` et modifiez les variables d'environnement en conséquence.

4. Copiez le fichier `config.example.yaml` en `config.yaml` et ajustez les paramètres selon vos besoins.

Utilisation
===========

Pour créer un conteneur LXC :

.. code-block:: bash

    poetry run python -m lxc_manager create

Pour créer un conteneur LXC pour Node.js :

.. code-block:: bash

    poetry run python -m lxc_manager create node

Pour créer un conteneur LXC pour Python :

.. code-block:: bash

    poetry run python -m lxc_manager create python

Pour créer un conteneur LXC pour .NET :

.. code-block:: bash

    poetry run python -m lxc_manager create dotnet

Pour démarrer un conteneur LXC existant :

.. code-block:: bash

    poetry run python -m lxc_manager start --vm-id <VM_ID>

Pour supprimer un conteneur LXC existant :

.. code-block:: bash

    poetry run python -m lxc_manager delete --vm-id <VM_ID>

Options Globales
================

* `-l`, `--log-level`: Définit le niveau de journalisation (DEBUG, INFO, WARNING, ERROR, CRITICAL). Par défaut : INFO.

Licence
=======

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.

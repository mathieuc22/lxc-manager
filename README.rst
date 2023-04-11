============================
Proxmox LXC Manager
============================

Ce projet est un gestionnaire de conteneurs LXC pour Proxmox. Il permet de créer, démarrer, arrêter et supprimer des conteneurs LXC de manière automatisée.

Fonctionnalités
===============

* Création de conteneurs LXC avec configuration réseau et accès SSH
* Démarrage de conteneurs LXC
* Suppression de conteneurs LXC
* Utilisation des ID de conteneur personnalisés à partir de 300

Installation
============

1. Clonez le dépôt :

   .. code-block:: bash

       git clone https://github.com/mathieuc22/proxmox-lxc-manager.git
       cd proxmox-lxc-manager

2. Installez les dépendances :

   .. code-block:: bash

       poetry install

3. Copiez le fichier `.env.example` en `.env` et modifiez les variables d'environnement en conséquence.

4. Copiez le fichier `config.example.yaml` en `config.yaml` et modifiez les paramètres en conséquence.

Utilisation
===========

Pour créer un conteneur LXC :

.. code-block:: bash

    poetry run python lxc_manager.py create

Pour démarrer un conteneur LXC existant :

.. code-block:: bash

    poetry run python lxc_manager.py start --vm-id <VM_ID>

Pour supprimer un conteneur LXC existant :

.. code-block:: bash

    poetry run python lxc_manager.py delete --vm-id <VM_ID>

Licence
=======

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.

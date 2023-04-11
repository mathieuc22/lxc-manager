import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Gestionnaire de conteneurs LXC pour Proxmox"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sous-commande 'create'
    create_parser = subparsers.add_parser("create", help="Créer des conteneurs")
    create_parser.add_argument(
        "-n",
        "--num-containers",
        type=int,
        default=None,
        help="Le nombre de containers à créer.",
    )

    # Sous-commande 'start'
    start_parser = subparsers.add_parser("start", help="Démarrer un conteneur")
    start_parser.add_argument(
        "--vm-id", type=int, required=True, help="ID du conteneur à démarrer"
    )

    # Sous-commande 'delete'
    delete_parser = subparsers.add_parser("delete", help="Supprimer un conteneur")
    delete_parser.add_argument(
        "--vm-id", type=int, required=True, help="ID du conteneur à supprimer"
    )

    parser.add_argument(
        "-l",
        "--log-level",
        type=str,
        default="INFO",
        help="Niveau de journalisation (DEBUG, INFO, WARNING, ERROR, CRITICAL). Par défaut : INFO.",
    )

    args = parser.parse_args()

    return args

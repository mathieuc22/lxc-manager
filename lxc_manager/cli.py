import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Gestionnaire de conteneurs LXC pour Proxmox"
    )
    parser.add_argument(
        "-n",
        "--num-containers",
        type=int,
        default=None,
        help="Le nombre de containers à créer.",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        type=str,
        default="INFO",
        help="Niveau de journalisation (DEBUG, INFO, WARNING, ERROR, CRITICAL). Par défaut : INFO.",
    )
    parser.add_argument("--delete", type=int, help="ID du conteneur à supprimer")
    args = parser.parse_args()
    return args

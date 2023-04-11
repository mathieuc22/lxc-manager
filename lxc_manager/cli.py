import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Crée des containers LXC à partir d'un fichier de configuration YAML."
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
    args = parser.parse_args()
    return args

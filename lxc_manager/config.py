import os
import yaml
from dotenv import load_dotenv


def load_config():
    general_config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    load_dotenv()

    with open(general_config_path, "r") as general_file:
        general_config = yaml.safe_load(general_file)

    secrets_config = {
        "username": os.getenv("PROXMOX_USERNAME"),
        "password": os.getenv("PROXMOX_PASSWORD"),
        "root_password": os.getenv("PROXMOX_ROOT_PASSWORD"),
        "proxmox_host": os.getenv("PROXMOX_HOST"),
        "ssh_key": os.getenv("PROXMOX_PUBLIC_KEY"),
    }

    config = {**general_config, **secrets_config}

    return config

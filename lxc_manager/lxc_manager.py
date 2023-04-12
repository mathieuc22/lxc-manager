import logging
import os
import time
from proxmoxer import ProxmoxAPI

from .cli import parse_args
from .config import load_config
from .container import create_lxc_container, delete_container, start_container
from .log_config import setup_logging
from .name_generator import generate_container_name
from .utils import execute_script_in_container_ssh

logger = logging.getLogger(__name__)


def main():
    # Parse les arguments de la ligne de commande
    args = parse_args()

    # Initialise la journalisation avec le niveau spécifié en argument
    setup_logging(args.log_level)

    # Charge la configuration YAML
    config = load_config()

    # Connexion à l'API Proxmox
    proxmox = ProxmoxAPI(
        config["proxmox_host"],
        user=config["username"],
        backend="ssh_paramiko",
    )

    node_name = config["node_name"]

    if args.command == "delete":
        vm_id = args.vm_id
        delete_container(proxmox, node_name, vm_id)
    elif args.command == "start":
        vm_id = args.vm_id
        start_container(proxmox, node_name, vm_id)
    elif args.command == "create":
        container_name_prefix = config["container_name_prefix"]
        num_containers = args.num_containers or config["num_containers"]

        # Crée les containers
        for i in range(num_containers):
            container_name = generate_container_name(container_name_prefix)
            config["container_name"] = container_name

            vm_id = create_lxc_container(proxmox, node_name, config)

            start_container(proxmox, node_name, vm_id)

            # Attends quelques secondes pour permettre au conteneur de démarrer correctement
            time.sleep(10)

            # Choisir le script en fonction du type d'environnement de développement
            if args.env_type == "node":
                script_name = "dev_setup_node.sh"
            elif args.env_type == "python":
                script_name = "dev_setup_python.sh"
            elif args.env_type == "dotnet":
                script_name = "dev_setup_dotnet.sh"

            script_path = os.path.join(os.path.dirname(__file__), "..", script_name)
            execute_script_in_container_ssh(container_name, script_path)

            logger.info(
                f"Container {container_name} (ID: {vm_id}) a été créé et configuré."
            )

            logger.info(
                f"Vous pouvez maintenant vous connecter au conteneur en SSH avec la commande : ssh root@{container_name}"
            )


if __name__ == "__main__":
    main()

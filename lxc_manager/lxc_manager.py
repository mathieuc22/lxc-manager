from .cli import parse_args
from .config import load_config
from .container import (
    create_lxc_container,
    start_container,
)
from .log_config import setup_logging
import logging
from proxmoxer import ProxmoxAPI

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
        user=f"{config['username']}@pam",
        password=config["password"],
        verify_ssl=False,
    )

    node_name = config["node_name"]
    container_name_prefix = config["container_name_prefix"]
    num_containers = args.num_containers or config["num_containers"]

    # Crée les containers
    for i in range(num_containers):
        container_name = f"{container_name_prefix}-{i+1}"
        config["container_name"] = container_name

        vm_id = create_lxc_container(proxmox, node_name, config)

        logger.info(
            f"Container {container_name} (ID: {vm_id}) a été créé et configuré."
        )

        start_container(proxmox, node_name, vm_id)


if __name__ == "__main__":
    main()

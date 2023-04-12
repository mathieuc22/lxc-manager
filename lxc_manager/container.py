import logging

logger = logging.getLogger(__name__)


def get_next_available_id(proxmox, node_name, min_id=300):
    containers = proxmox.nodes(node_name).lxc.get()
    used_ids = [container["vmid"] for container in containers]
    used_ids = sorted(map(int, used_ids))

    for i in range(min_id, 100000):
        if i not in used_ids:
            return i

    raise ValueError("Aucun ID disponible trouvé.")


def create_lxc_container(proxmox, node_name, config):
    # Configuration de l'accès SSH
    with open(config["ssh_key"], "r") as key_file:
        public_key = key_file.read().strip()

    # Création du container LXC
    container_name = config["container_name"]
    template = config["template"]
    storage = config["storage"]
    root_password = config["root_password"]
    memory = config["memory"]
    swap = config["swap"]
    net0 = config["net0"]
    features = config["features"]

    next_vmid = get_next_available_id(proxmox, node_name)

    newcontainer = {
        "vmid": next_vmid,
        "ostemplate": template,
        "hostname": container_name,
        "storage": storage,
        "memory": memory,
        "swap": swap,
        "cores": 1,
        "password": root_password,
        "net0": net0,
        "features": features,
        "ssh-public-keys": public_key,
    }
    node = proxmox.nodes(node_name)
    result = node.lxc.create(**newcontainer)
    logger.info(f"Container {container_name} (ID: {next_vmid}) a été créé.")

    return next_vmid


def start_container(proxmox, node_name, vm_id):
    result = proxmox.nodes(node_name).lxc(vm_id).status.start.post()
    logger.info(f"Conteneur (ID: {vm_id}) démarré.")


def delete_container(proxmox, node_name, vm_id):
    container_status = proxmox.nodes(node_name).lxc(vm_id).status.current.get()

    if container_status["status"] != "stopped":
        taskid = proxmox.nodes(node_name).lxc(vm_id).status.stop.post()

        logger.info(f"Conteneur (ID: {vm_id}) arrêté.")

    result = proxmox.nodes(node_name).lxc(vm_id).delete()
    logger.info(f"Conteneur (ID: {vm_id}) supprimé.")

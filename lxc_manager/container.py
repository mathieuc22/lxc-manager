import logging
import time

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
        "ssh-public-keys": public_key,
    }
    node = proxmox.nodes(node_name)
    taskid = node.lxc.create(**newcontainer)

    while True:
        task_status = proxmox.nodes(node_name).tasks(taskid).status.get()
        if task_status["status"] == "stopped":
            if task_status["exitstatus"] == "OK":
                logger.info(f"Container {container_name} (ID: {next_vmid}) a été créé.")
            else:
                logger.error(
                    f"Échec de la création du conteneur {container_name} (ID: {next_vmid}): {task_status['exitstatus']}"
                )
            break
        time.sleep(
            2
        )  # Attendre 2 secondes avant de vérifier à nouveau l'état de la tâche

    return next_vmid


def start_container(proxmox, node_name, vm_id):
    taskid = proxmox.nodes(node_name).lxc(vm_id).status.start.post()

    while True:
        task_status = proxmox.nodes(node_name).tasks(taskid).status.get()
        if task_status["status"] == "st opped":
            if task_status["exitstatus"] == "OK":
                logger.info(f"Conteneur (ID: {vm_id}) démarré.")
            else:
                logger.error(
                    f"Échec du démarrage du conteneur (ID: {vm_id}): {task_status['exitstatus']}"
                )
            break
        time.sleep(
            2
        )  # Attendre 2 secondes avant de vérifier à nouveau l'état de la tâche


def delete_container(proxmox, node_name, vm_id):
    container_status = proxmox.nodes(node_name).lxc(vm_id).status.current.get()

    if container_status["status"] != "stopped":
        taskid = proxmox.nodes(node_name).lxc(vm_id).status.stop.post()

        while True:
            task_status = proxmox.nodes(node_name).tasks(taskid).status.get()
            if task_status["status"] == "stopped":
                if task_status["exitstatus"] == "OK":
                    logger.info(f"Conteneur (ID: {vm_id}) arrêté.")
                else:
                    logger.error(
                        f"Échec de l'arrêt du conteneur (ID: {vm_id}): {task_status['exitstatus']}"
                    )
                    return
                break
            time.sleep(
                2
            )  # Attendre 2 secondes avant de vérifier à nouveau l'état de la tâche

    taskid = proxmox.nodes(node_name).lxc(vm_id).delete()

    while True:
        task_status = proxmox.nodes(node_name).tasks(taskid).status.get()
        if task_status["status"] == "stopped":
            if task_status["exitstatus"] == "OK":
                logger.info(f"Conteneur (ID: {vm_id}) supprimé.")
            else:
                logger.error(
                    f"Échec de la suppression du conteneur (ID: {vm_id}): {task_status['exitstatus']}"
                )
            break
        time.sleep(
            2
        )  # Attendre 2 secondes avant de vérifier à nouveau l'état de la tâche

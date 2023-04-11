import logging
import time

logger = logging.getLogger(__name__)


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

    next_vmid = proxmox.cluster.nextid.get()

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

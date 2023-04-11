import os
import logging
from proxmoxer import ProxmoxAPI

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

    next_vmid = proxmox.cluster.nextid()

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

    result = node.tasks(taskid).wait()
    logger.info(f"Container {container_name} (ID: {next_vmid}) a été créé.")

    return next_vmid


def start_container(proxmox, node_name, vm_id):
    proxmox.nodes(node_name).lxc(vm_id).status.start()
    logger.info(f"Container {vm_id} a été démarré.")

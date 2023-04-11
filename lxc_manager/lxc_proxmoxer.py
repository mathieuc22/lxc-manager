import os
from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv

load_dotenv()

PROXMOX_HOST = os.getenv("PROXMOX_HOST")
USERNAME = os.getenv("PROXMOX_USERNAME")
PASSWORD = os.getenv("PROXMOX_PASSWORD")
NODE_NAME = "pve2"

# Configuration du container
vm_id = 300
container_name = "dev-container"
template = "local:vztmpl/debian-11-standard_11.3-0_amd64.tar.gz"
storage = "local-lvm"
root_password = os.getenv("PROXMOX_ROOT_PASSWORD")
public_key_path = os.getenv("PROXMOX_PUBLIC_KEY")

# Connexion à l'API Proxmox
proxmox = ProxmoxAPI(
    PROXMOX_HOST, user=f"{USERNAME}@pam", password=PASSWORD, verify_ssl=False
)

# Configuration de l'accès SSH
with open(public_key_path, "r") as key_file:
    public_key = key_file.read().strip()

# Création du container LXC
newcontainer = {
    "vmid": vm_id,
    "ostemplate": template,
    "hostname": container_name,
    "storage": storage,
    "memory": 512,
    "swap": 512,
    "cores": 1,
    "password": root_password,
    "net0": "name=eth0,bridge=vmbr0,ip=dhcp",
    "ssh-public-keys": public_key,
}
node = proxmox.nodes(NODE_NAME)
taskid = node.lxc.create(**newcontainer)

# Attente de la fin de la création du container
result = proxmox.nodes(NODE_NAME).tasks(taskid).wait()

# Démarrage du container LXC
proxmox.nodes(NODE_NAME).lxc(vm_id).status.start()

print(
    f"Container {container_name} (ID: {vm_id}) a été créé et démarré, avec le réseau et le mot de passe root configurés."
)

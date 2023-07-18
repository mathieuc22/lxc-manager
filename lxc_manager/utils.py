import logging

import paramiko

logger = logging.getLogger(__name__)


def execute_script_in_container_ssh(container_ip, script_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(container_ip, username="root")
        logger.info(f"Connexion SSH établie avec le conteneur {container_ip}")

        with open(script_path, "r") as script_file:
            script = script_file.read()

        stdin, stdout, stderr = ssh.exec_command(f"bash -s")
        stdin.write(script)
        stdin.channel.shutdown_write()

        output = stdout.read().decode("utf-8")
        errors = stderr.read().decode("utf-8")

        if errors:
            logger.error(f"Erreurs lors de l'exécution du script :\n{errors}")
        else:
            logger.info(f"Script exécuté avec succès :\n{output}")

    except Exception as e:
        logger.error(f"Erreur lors de l'exécution du script dans le conteneur : {e}")

    finally:
        ssh.close()
        logger.info(f"Connexion SSH fermée avec le conteneur {container_ip}")

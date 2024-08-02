import argparse
import time
import uuid

import hyperstack


def create_pytorch_vm(
    name, flavor_name, environment, key_name, image_name="Ubuntu Server 22.04 LTS R535 CUDA 12.2", username=None, password=None, docker_image=None
):
    """
    password is the password created for the user within the Docker container. It's randomly generated and printed out in the std out if not entered.
    """
    hyperstack.set_environment(environment)
    if password is None:
        USER_PASSWORD = uuid.uuid4()
    else:
        USER_PASSWORD = password

    if username is None:
        USER_NAME = "dockeruser"
    else:
        USER_NAME = username

    if docker_image is None:
        DOCKER_IMAGE = uuid.uuid4()
    else:
        DOCKER_IMAGE = docker_image
    response = hyperstack.create_vm(
        name=name,
        image_name=image_name,
        flavor_name=flavor_name,
        assign_floating_ip=True,
        key_name=key_name,
        user_data=f"#!/bin/bash\n\n# Set up docker\n\n## Add Docker's official GPG key:\nsudo apt-get update\nsudo apt-get install -y ca-certificates curl gnupg\nsudo install -m 0755 -d /etc/apt/keyrings\ncurl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --yes --dearmor -o /etc/apt/keyrings/docker.gpg\nsudo chmod a+r /etc/apt/keyrings/docker.gpg\n\n## Add the repository to Apt sources:\necho \\\n\"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \\\n$(. /etc/os-release && echo $VERSION_CODENAME) stable\" | \\\nsudo tee /etc/apt/sources.list.d/docker.list > /dev/null\nsudo apt-get update\n\n## Install docker\nsudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin\n\n## Add docker group to ubuntu user\nsudo usermod -aG docker ubuntu\nsudo usermod -aG docker $USER\n\nsudo apt-get install nvidia-container-toolkit -y\n\n## Configure docker\n\nsudo nvidia-ctk runtime configure --runtime=docker\n\nsudo systemctl restart docker\n\n# New verification step\necho 'Verifying NVIDIA runtime...'\nmax_attempts=6\nattempt=0\nwhile ! docker info | grep -i nvidia > /dev/null; do\n    attempt=$((attempt+1))\n    if [ $attempt -eq $max_attempts ]; then\n        echo 'NVIDIA runtime not detected after $max_attempts attempts. Please check your installation.'\n        exit 1\n    fi\n    echo 'NVIDIA runtime not detected. Waiting... (Attempt $attempt of $max_attempts)'\n    sleep 10\ndone\necho 'NVIDIA runtime detected successfully.'\nnewgrp docker\ndocker run -d -t --gpus all -v /usr/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu -v /usr/bin/nvidia-smi:/usr/bin/nvidia-smi -p 8888:8888 -e USER_NAME={USER_NAME} -e USER_PASSWORD={USER_PASSWORD} --name pytorch {DOCKER_IMAGE}",
    )

    vm_id = response['instances'][0]['id']
    print(f"Booting {vm_id}")
    hyperstack.wait_for_vm_active(vm_id, max_attempts=4, initial_delay=30, delay=10, backoff_factor=1.5)
    hyperstack.set_sg_rules(vm_id=vm_id, port_range_min=22, port_range_max=22)
    hyperstack.set_sg_rules(vm_id=vm_id, protocol="icmp")
    print(f"Machine {vm_id} Ready")
    time.sleep(5)
    floating_ip = hyperstack.get_floating_ip(vm_id)
    print(f"Public IP: {floating_ip}")
    print(f"In container credentials:\nusername: dockeruser\nPassword: {USER_PASSWORD}")
    return vm_id, floating_ip

def create_ollama_vm(name, flavor_name, environment, key_name, image_name="Ubuntu Server 22.04 LTS R535 CUDA 12.2"):
    hyperstack.set_environment(environment)

    response = hyperstack.create_vm(
        name=name,
        image_name=image_name,
        flavor_name=flavor_name,
        assign_floating_ip=True,
        key_name=key_name,
        user_data="#!/bin/bash\n\n# Set up docker\n\n## Add Docker's official GPG key:\nsudo apt-get update\nsudo apt-get install -y ca-certificates curl gnupg\nsudo install -m 0755 -d /etc/apt/keyrings\ncurl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --yes --dearmor -o /etc/apt/keyrings/docker.gpg\nsudo chmod a+r /etc/apt/keyrings/docker.gpg\n\n## Add the repository to Apt sources:\necho \\\n\"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \\\n$(. /etc/os-release && echo $VERSION_CODENAME) stable\" | \\\nsudo tee /etc/apt/sources.list.d/docker.list > /dev/null\nsudo apt-get update\n\n## Install docker\nsudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin\n\n## Add docker group to ubuntu user\nsudo usermod -aG docker ubuntu\nsudo usermod -aG docker $USER\n\nsudo apt-get install nvidia-container-toolkit -y\n\n## Configure docker\n\nsudo nvidia-ctk runtime configure --runtime=docker\n\nsudo systemctl restart docker\n\nnewgrp docker\ndocker run -d --gpus all -v /usr/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu -v /usr/bin/nvidia-smi:/usr/bin/nvidia-smi -v ollama:/root/.ollama -p 11434:11434 -e OLLAMA_HOST=0.0.0.0 --name ollama ollama/ollama",
    )

    vm_id = response['instances'][0]['id']

    print(f'Virtual Machine {vm_id} booting up')
    hyperstack.wait_for_vm_active(vm_id, max_attempts=4, initial_delay=30, delay=10, backoff_factor=1.5)
    hyperstack.set_sg_rules(vm_id=vm_id, port_range_min=22, port_range_max=22)
    hyperstack.set_sg_rules(vm_id=vm_id, port_range_min=11434, port_range_max=11434)
    hyperstack.set_sg_rules(vm_id=vm_id, protocol="icmp")

    print(f"Machine {vm_id} Ready")
    time.sleep(5)
    floating_ip = hyperstack.get_floating_ip(vm_id)
    print(f"Public IP: {floating_ip}")
    print('DONE')
    return vm_id, floating_ip


def deploy(
    deployment_type, name, environment, flavor_name, key_name, image_name="Ubuntu Server 22.04 LTS R535 CUDA 12.2"
):
    if deployment_type == "pytorch":
        return create_pytorch_vm(name, flavor_name, environment, key_name, image_name)
    elif deployment_type == "ollama":
        return create_ollama_vm(name, flavor_name, environment, key_name, image_name)
    else:
        raise ValueError("Invalid deployment type. Choose 'pytorch' or 'ollama'.")

def main():
    parser = argparse.ArgumentParser(description="Deploy PyTorch or Ollama on Hyperstack")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # PyTorch subcommand
    pytorch_parser = subparsers.add_parser("pytorch", help="Deploy PyTorch")
    pytorch_parser.add_argument("--name", required=True, help="Name of the virtual machine")
    pytorch_parser.add_argument("--environment", required=True, help="Environment to deploy in")
    pytorch_parser.add_argument("--flavor_name", required=True, help="Flavor name for the VM")
    pytorch_parser.add_argument("--key_name", required=True, help="Name of the key to use")
    pytorch_parser.add_argument("--image_name", default="Ubuntu Server 22.04 LTS R535 CUDA 12.2", help="Name of the image to use")
    pytorch_parser.add_argument("--username", default=None, help="Password of the docker user")
    pytorch_parser.add_argument("--password", default=None, help="Password of the docker user")
    pytorch_parser.add_argument("--docker_image", default=None, help="Docker image to use, if not default")

    # Ollama subcommand
    ollama_parser = subparsers.add_parser("ollama", help="Deploy Ollama")
    ollama_parser.add_argument("--name", required=True, help="Name of the virtual machine")
    ollama_parser.add_argument("--environment", required=True, help="Environment to deploy in")
    ollama_parser.add_argument("--flavor_name", required=True, help="Flavor name for the VM")
    ollama_parser.add_argument("--key_name", required=True, help="Name of the key to use")
    ollama_parser.add_argument("--image_name", default="Ubuntu Server 22.04 LTS R535 CUDA 12.2", help="Name of the image to use")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    vm_id, floating_ip = deploy(
        deployment_type=args.command,
        name=args.name,
        flavor_name=args.flavor_name,
        key_name=args.key_name,
        image_name=args.image_name,
        environment=args.environment,
    )

if __name__ == "__main__":
    main()
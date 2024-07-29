import argparse
import time

import hyperstack


def wait_for_vm_active(vm_id, max_attempts=4, initial_delay=20, delay=10, backoff_factor=1.5):
    current_delay = initial_delay
    time.sleep(current_delay)
    for attempt in range(max_attempts):
        vm_details = hyperstack.retrieve_vm_details(vm_id)
        status = vm_details['instance']['status']

        if status == 'ACTIVE':
            return True
        elif status == 'ERROR':
            raise Exception(f"VM {vm_id} entered ERROR state")

        print(
            f"Attempt {attempt + 1}/{max_attempts}: VM {vm_id} status is {status}. Waiting for {current_delay} seconds."
        )
        time.sleep(current_delay)

        # Increase the delay for the next iteration
        current_delay = delay + (delay * backoff_factor * attempt)

    raise TimeoutError(f"VM {vm_id} did not become active within the specified time")


def create_pytorch_vm(name, flavor_name, environment, key_name, image_name="Ubuntu Server 22.04 LTS R535 CUDA 12.2"):
    hyperstack.set_environment(environment)

    response = hyperstack.create_vm(
        name=name,
        image_name=image_name,
        flavor_name=flavor_name,
        assign_floating_ip=True,
        key_name=key_name,
        user_data="#!/bin/bash\n\n# Set up docker\n\n## Add Docker's official GPG key:\nsudo apt-get update\nsudo apt-get install -y ca-certificates curl gnupg\nsudo install -m 0755 -d /etc/apt/keyrings\ncurl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --yes --dearmor -o /etc/apt/keyrings/docker.gpg\nsudo chmod a+r /etc/apt/keyrings/docker.gpg\n\n## Add the repository to Apt sources:\necho \\\n\"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \\\n$(. /etc/os-release && echo $VERSION_CODENAME) stable\" | \\\nsudo tee /etc/apt/sources.list.d/docker.list > /dev/null\nsudo apt-get update\n\n## Install docker\nsudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin\n\n## Add docker group to ubuntu user\nsudo usermod -aG docker ubuntu\nsudo usermod -aG docker $USER\n\nsudo apt-get install nvidia-container-toolkit -y\n\n## Configure docker\n\nsudo nvidia-ctk runtime configure --runtime=docker\n\nsudo systemctl restart docker\n\nnewgrp docker\ndocker run -d -t --gpus all -v /usr/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu -v /usr/bin/nvidia-smi:/usr/bin/nvidia-smi -p 8888:8888 --name pytorch balancedscorpion/python3-pytorch-ubuntu",
    )

    vm_id = response['instances'][0]['id']
    print(f"Booting {vm_id}")
    wait_for_vm_active(vm_id, max_attempts=4, initial_delay=30, delay=10, backoff_factor=1.5)
    hyperstack.set_sg_rules(vm_id=vm_id, port_range_min=22, port_range_max=22)
    hyperstack.set_sg_rules(vm_id=vm_id, protocol="icmp")
    print(f"Machine {vm_id} Ready")


def main():
    parser = argparse.ArgumentParser(description="Deploy PyTorch on Hyperstack")
    parser.add_argument("--name", required=True, help="Name of the virtual machine")
    parser.add_argument("--environment", help="Environment to deploy in")
    parser.add_argument("--flavor_name", required=True, help="Flavor name for the VM")
    parser.add_argument("--key_name", required=True, help="Name of the key to use")
    parser.add_argument(
        "--image_name", default="Ubuntu Server 22.04 LTS R535 CUDA 12.2", help="Name of the image to use"
    )

    args = parser.parse_args()

    create_pytorch_vm(
        name=args.name,
        flavor_name=args.flavor_name,
        key_name=args.key_name,
        image_name=args.image_name,
        environment=args.environment,
    )


if __name__ == "__main__":
    main()

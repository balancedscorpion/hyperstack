from hyperstack import Hyperstack
import json


def deploy_ollama(flavor_name="n2-RTX-A5000x1"):
    hyperstack = Hyperstack()

    hyperstack.set_environment("development")

    response = hyperstack.create_vm(
            name="ollama-server",
            image_name="Ubuntu Server 22.04 LTS R535 CUDA 12.2",
            flavor_name=flavor_name,
            assign_floating_ip=True,
            user_data="#!/bin/bash\n\n# Set up docker\n\n## Add Docker's official GPG key:\nsudo apt-get update\nsudo apt-get install -y ca-certificates curl gnupg\nsudo install -m 0755 -d /etc/apt/keyrings\ncurl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --yes --dearmor -o /etc/apt/keyrings/docker.gpg\nsudo chmod a+r /etc/apt/keyrings/docker.gpg\n\n## Add the repository to Apt sources:\necho \\\n\"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \\\n$(. /etc/os-release && echo $VERSION_CODENAME) stable\" | \\\nsudo tee /etc/apt/sources.list.d/docker.list > /dev/null\nsudo apt-get update\n\n## Install docker\nsudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin\n\n## Add docker group to ubuntu user\nsudo usermod -aG docker ubuntu\nsudo usermod -aG docker $USER\n\nsudo apt-get install nvidia-container-toolkit -y\n\n## Configure docker\n\nsudo nvidia-ctk runtime configure --runtime=docker\n\nsudo systemctl restart docker\n\nnewgrp docker\ndocker run -d --gpus all -v /usr/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu -v /usr/bin/nvidia-smi:/usr/bin/nvidia-smi -v ollama:/root/.ollama -p 11434:11434 -e OLLAMA_HOST=0.0.0.0 --name ollama ollama/ollama"
        )

    content = json.loads(response.content)
    vm_id = content['instances'][0]['id']

    print('Virtual Machine ', vm_id,' booting up')
    hyperstack._execute_with_backoff(hyperstack.set_sg_rules,max_attempts=4, initial_delay=30, delay=10, backoff_factor=1.5, vm_id=vm_id, port_range_min=11434, port_range_max=11434)
    hyperstack._execute_with_backoff(hyperstack.set_sg_rules,max_attempts=4, initial_delay=0, delay=10, backoff_factor=1.5, vm_id=vm_id, port_range_min=22, port_range_max=22)
    hyperstack._execute_with_backoff(hyperstack.set_sg_rules,max_attempts=4, initial_delay=0, delay=10, backoff_factor=1.5, vm_id=vm_id, protocol="icmp")
    print(hyperstack.get_floating_ip(vm_id))
    print('DONE')

deploy_ollama()
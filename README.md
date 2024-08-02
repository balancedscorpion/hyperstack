# Hyperstack Python Client
![Tests](https://img.shields.io/github/actions/workflow/status/balancedscorpion/hyperstack/tests.yml?label=tests)
![Coverage](https://img.shields.io/codecov/c/github/balancedscorpion/hyperstack)
![PyPI](https://img.shields.io/pypi/v/hyperstack)
![Python Versions](https://img.shields.io/pypi/pyversions/hyperstack)
![License](https://img.shields.io/github/License/balancedscorpion/hyperstack)
![PyPI Downloads](https://img.shields.io/pypi/dm/hyperstack)

This is a Python client for interacting with the Hyperstack API

### Installation

```bash
pip install hyperstack
```

### Usage

First ensure you have your API key set in an environment variable.

To create an API key, visit you can review [Hyperstack's documentation](https://infrahub-doc.nexgencloud.com/docs/api-reference/getting-started-api/authentication/#api-keys).

Then add your API key to the environment variables.

```bash
export HYPERSTACK_API_KEY=<your API Key>
```

```python
import hyperstack
```

#### Create an environment if you don't have one

```python
hyperstack.create_environment('your-environment-name')
```

#### Set your environment

```python
hyperstack.set_environment('your-environment-name')
```

#### Create a VM
```python
hyperstack.create_vm(
        name='first-vm',
        image_name="Ubuntu Server 22.04 LTS R535 CUDA 12.2",
        flavor_name='n2-RTX-A5000x1',
        key_name="your-key",
        user_data="",
        create_bootable_volume=False,
        assign_floating_ip=False,
        count=1)
```


### One-click Deployments

Before you make any deployments, ensure you have set up your environment and [ssh-key](https://infrahub-doc.nexgencloud.com/docs/network/ssh/#create-an-ssh-key) as per the Hyperstack Documentation. Please note that the one-click deployments can take 5-10 minutes to be ready after the script has completed. The script completes when the machine is ready, but the machine still needs to download the docker image with ollama or python with notebooks within it. Further details can be found below within [One-click deployment further details](#one-click-deployment-further-details) section.


#### Deploy Ollama Server

First set-up your ssh key and environment. Then navigate to the hyperstack library and run:

```bash
hyperstack ollama --name ollama-server --flavor_name n2-RTX-A5000x1 --key_name your-key --environment your-environment
```


#### Deploy Pytorch server

The same command as above, but change ollama to pytorch

```bash
hyperstack pytorch --name ollama-server --flavor_name n2-RTX-A5000x1 --key_name your-key --environment your-environment
```


#### Deploy from Python

```python3
from hyperstack.deploy import deploy
deploy(deployment_type="pytorch", name="pytorch-vm", environment="your-environment", flavor_name="n2-RTX-A5000x1", key_name="your-key")
```



```python3
from hyperstack.deploy import deploy
deploy(deployment_type="ollama", name="ollama-vm", environment="your-environment", flavor_name="n2-RTX-A5000x1", key_name="your-key")
```


### One-click deployment further details

Here's a sample command to run the deployment.

```bash
hyperstack pytorch --name ollama-server --flavor_name n2-RTX-A5000x1 --key_name your-key --environment your-environment
```

After you run a command (for example the Pytorch server), you will receive the requested configuration and useful details will print out.

```bash
Environment set to: your-environment
Booting 12345
Attempt 1/4: VM 12345 status is BUILD. Waiting for 30 seconds.
Machine 12345 Ready
Public IP: xxx.xxx.xxx.xxx
In container credentials:
username: dockeruser
Password: xxxxxxxx
````

This includes your virtual machine id, public ip for to ssh into the machine, and your dockeruser credentials. This will default to a uuid, unless explicitly provided.
The machine is ready and will now download docker, the docker image with pytorch, juptyer notebooks inside and the configuration. This will take another 5-10 minutes, but for now, you will be able to ssh into the machine:

```bash
ssh -i ~/.ssh/ed25519 ubuntu@xxx.xxx.xxx.xxx
```

If you'd like to follow the installation:

Once ssh in the machine, you can try to open the docker container. Please note: it can sometimes take 5-10 minutes for docker to install and the docker image to be downloaded after the machine is ready. Please be patient with this. If you'd like to debug this you can do the following once ssh into the machine.

Apply the docker group to your current shell session:
```bash
newgrp docker
```

Check that docker and the image has indeed downloaded. This may take 5-10 minutes.
```bash
docker ps -a
```

Once it has downloaded you should see output like the below:
```
CONTAINER ID   IMAGE                                     COMMAND                  CREATED         STATUS         PORTS                                       NAMES
xxxxxxxxxxxx   balancedscorpion/python3-pytorch-ubuntu   "/entrypoint.sh /bin…"   2 minutes ago   Up 2 minutes   0.0.0.0:8888->8888/tcp, :::8888->8888/tcp   pytorch
```

Now you can access the docker container. You can access this. For example, using VScode you can download ssh-connect and dev-containers to access this directly.

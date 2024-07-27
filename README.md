# Hyperstack Python Client

This is a Python client for interacting with the Hyperstack API

### Installation

```bash
pip install hyperstack
```

### Usage

First ensure you have your API key set in an environment variable:

```bash
HYPERSTACK_API_KEY=<your API Key>
```

```python
from hyperstack import Hyperstack

client = Hyperstack()
```

#### Create an environment if you don't have one

```python
client.create_environment('development')  
```

#### Set your environment

```python
client.set_environment('development')  
```

#### Create a VM
```python
client.create_vm(
        name='first vm', 
        image_name="Ubuntu Server 22.04 LTS R535 CUDA 12.2", 
        flavor_name='n2-RTX-A5000x1', 
        key_name="development-key", 
        user_data="", 
        create_bootable_volume=False, 
        assign_floating_ip=False, 
        count=1)
```
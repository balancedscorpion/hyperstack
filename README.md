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

First ensure you have your API key set in an environment variable:

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
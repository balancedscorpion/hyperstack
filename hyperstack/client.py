import requests
import os
import json
import time

class Hyperstack:
    
    def __init__(self):
        self.api_key = os.environ["HYPERSTACK_API_KEY"]
        if not self.api_key:
            raise EnvironmentError("HYPERSTACK_API_KEY environment variable not set. Please set it to continue.")
        self.base_url = "https://infrahub-api.nexgencloud.com/v1/"
        self.headers = {
            "Content-Type": "application/json",
            "api_key": self.api_key
        }
        self.valid_regions = ["NORWAY-1", "CANADA-1"]
        self.environment = None
    
    def create_environment(self, name, region):
        """
        Creates a new environment with the given name and region.

        :param name: The name of the environment.
        :param region: The region where the environment will be created.
        :return: The response from the API call.
        """
        if region not in self.valid_regions:
            raise ValueError(f"Invalid region specified. Valid regions are: {', '.join(self.valid_regions)}")
        
        url = f"{self.base_url}core/environments"
        payload = {
            "name": name,
            "region": region
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 201:
            print("Environment created successfully.")
        else:
            print(f"Failed to create environment: {response.status_code} - {response.text}")
        
        return response
    
    def set_environment(self, environment):
        """
        Sets the current environment.

        :param environment: The name of the environment to set.
        """
        self.environment = environment
        print(f"Environment set to: {self.environment}")


    def create_vm(self, name, image_name, flavor_name, key_name="development-key", user_data="", create_bootable_volume=False, assign_floating_ip=False, count=1):
        """
        Creates a new virtual machine with the given parameters.

        :param name: The name of the virtual machine.
        :param image_name: The image to use for the virtual machine.
        :param flavor_name: The flavor (size) of the virtual machine.
        :param key_name: The key pair name to associate with the virtual machine.
        :param user_data: The user data to provide when launching the instance.
        :param create_bootable_volume: Whether to create a bootable volume.
        :param assign_floating_ip: Whether to assign a floating IP.
        :param count: The number of virtual machines to create.
        :return: The response from the API call.
        """
        self._check_environment_set()
        
        url = f"{self.base_url}core/virtual-machines"
        payload = {
            "name": name,
            "environment_name": self.environment,
            "image_name": image_name,
            "create_bootable_volume": create_bootable_volume,
            "flavor_name": flavor_name,
            "key_name": key_name,
            "user_data": user_data,
            "assign_floating_ip": assign_floating_ip,
            "count": count
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 201:
            print("VM created successfully.")
        else:
            print(f"Failed to create VM: {response.status_code} - {response.text}")
        
        return response
    
    def _check_environment_set(self):
        """
        Checks if the environment is set.

        :return: None if the environment is set.
        :raises EnvironmentError: If the environment is not set.
        """
        if self.environment is None:
            raise EnvironmentError("Environment is not set. Please set the environment using set_environment().")
        else:
            print(f"Current environment: {self.environment}")

    def set_sg_rules(self, vm_id, remote_ip_prefix="0.0.0.0/0", direction="ingress", ethertype="IPv4", protocol="tcp", port_range_min=None, port_range_max=None):
        """
        Sets security group rules for the specified virtual machine.

        :param vm_id: The ID of the virtual machine.
        :param remote_ip_prefix: The remote IP prefix (default is "0.0.0.0/0").
        :param direction: The direction of traffic (default is "ingress").
        :param ethertype: The Ethernet type (default is "IPv4").
        :param protocol: The protocol (default is "tcp").
        :param port_range_min: The minimum port range (optional).
        :param port_range_max: The maximum port range (optional).
        :return: The response from the API call.
        """
        self._check_environment_set()
        
        url = f"{self.base_url}core/virtual-machines/{vm_id}/sg-rules"
        payload = {
            "remote_ip_prefix": remote_ip_prefix,
            "direction": direction,
            "ethertype": ethertype,
            "protocol": protocol
        }
        
        if port_range_min is not None:
            payload["port_range_min"] = port_range_min
        if port_range_max is not None:
            payload["port_range_max"] = port_range_max
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:  # 200 indicates that the request was successful
            print("Security group rule set successfully.")
        else:
            print(f"Failed to set security group rule: {response.status_code} - {response.text}")
        
        return response
    
    def _execute_with_backoff(self, func, max_attempts=4, initial_delay=30, delay=10, backoff_factor=1.5, **kwargs):
        """
        Executes a function with a back-off strategy.

        :param func: The function to execute.
        :param args: Positional arguments to pass to the function.
        :param max_attempts: Maximum number of attempts.
        :param initial_delay: Initial delay between attempts.
        :param backoff_factor: Factor by which the delay increases after each attempt.
        :param kwargs: Keyword arguments to pass to the function.
        :return: The result of the function if it succeeds, or None if it fails after the maximum number of attempts.
        """
        attempts = 0
        time.sleep(initial_delay)
        attempts += 1
        while attempts < max_attempts:
            try:
                result = func(**kwargs)
                if result.status_code == 200:
                    return result
                else:
                    print(f"Attempt {attempts + 1} failed: {result.status_code} - {result.text}")
            except Exception as e:
                print(f"Attempt {attempts + 1} encountered an error: {e}")

            time.sleep(delay)
            delay *= backoff_factor
        
        print("All attempts failed.")
        return None
    
    def _execute_with_backoff(self, func, max_attempts=4, initial_delay=30, delay=10, backoff_factor=1.5, **kwargs):
        """
        Executes a function with a back-off strategy.

        :param func: The function to execute.
        :param args: Positional arguments to pass to the function.
        :param max_attempts: Maximum number of attempts.
        :param initial_delay: Initial delay between attempts.
        :param backoff_factor: Factor by which the delay increases after each attempt.
        :param kwargs: Keyword arguments to pass to the function.
        :return: The result of the function if it succeeds, or None if it fails after the maximum number of attempts.
        """
        attempts = 0
        time.sleep(initial_delay)
        attempts += 1
        while attempts < max_attempts:
            try:
                result = func(**kwargs)
                if result.status_code == 200:
                    return result
                else:
                    print(f"Attempt {attempts + 1} failed: {result.status_code} - {result.text}")
            except Exception as e:
                print(f"Attempt {attempts + 1} encountered an error: {e}")

            time.sleep(delay)
            delay *= backoff_factor
        
        print("All attempts failed.")
        return None
    
    def create_volume(self, name, volume_type, size=50, image_id=None, description=None, callback_url=None):
        """
        Creates a new volume with the given parameters.

        :param name: The name of the volume (required).
        :param volume_type: The type of the volume (required).
        :param size: The size of the volume in GB (default is 50).
        :param image_id: The ID of the image to use for the volume (optional).
        :param description: A description for the volume (optional).
        :param callback_url: A callback URL (optional).
        :return: The response from the API call.
        """
        self._check_environment_set()
        
        url = f"{self.base_url}core/volumes"
        payload = {
            "name": name,
            "environment_name": self.environment,
            "volume_type": volume_type,
            "size": size
        }
        
        # Add optional parameters to the payload if they are provided
        if image_id is not None:
            payload["image_id"] = image_id
        if description is not None:
            payload["description"] = description
        if callback_url is not None:
            payload["callback_url"] = callback_url
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 201:
            print("Volume created successfully.")
        else:
            print(f"Failed to create volume: {response.status_code} - {response.text}")
        
        return response
    
    def list_volumes(self):
        """
        Lists all volumes in the current environment.

        :return: The response from the API call, containing the list of volumes.
        """
        self._check_environment_set()
        
        url = f"{self.base_url}core/volumes"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            volumes = response.json()
            print(f"Successfully retrieved {len(volumes)} volumes.")
            for volume in volumes:
                print(f"Volume ID: {volume.get('id')}, Name: {volume.get('name')}, Size: {volume.get('size')}GB")
        else:
            print(f"Failed to retrieve volumes: {response.status_code} - {response.text}")
        
        return response
    
    def list_volume_types(self):
        """
        Lists all available volume types.

        :return: The response from the API call, containing the list of volume types.
        """
        url = f"{self.base_url}core/volume-types"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            volume_types = response.json()
            print(f"Successfully retrieved {len(volume_types)} volume types.")
            for volume_type in volume_types:
                print(f"Name: {volume_type.get('name')}, Description: {volume_type.get('description')}")
        else:
            print(f"Failed to retrieve volume types: {response.status_code} - {response.text}")
        
        return response

    def start_virtual_machine(self, vm_id):
        """
        Starts a virtual machine.

        :param vm_id: The ID of the virtual machine to start.
        :return: The response from the API call.
        """
        self._check_environment_set()
        
        url = f"{self.base_url}core/virtual-machines/{vm_id}/start"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            print(f"Successfully started virtual machine with ID: {vm_id}")
        else:
            print(f"Failed to start virtual machine: {response.status_code} - {response.text}")
        
        return response

    def stop_virtual_machine(self, vm_id):
        """
        Shuts down a virtual machine.

        :param vm_id: The ID of the virtual machine to stop.
        :return: The response from the API call.
        """
        self._check_environment_set()
        
        url = f"{self.base_url}core/virtual-machines/{vm_id}/stop"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            print(f"Successfully stopped virtual machine with ID: {vm_id}")
        else:
            print(f"Failed to stop virtual machine: {response.status_code} - {response.text}")
        
        return response

    def hard_reboot_virtual_machine(self, vm_id):
        """
        Reboots a virtual machine (hard reboot).

        :param vm_id: The ID of the virtual machine to reboot.
        :return: The response from the API call.
        """
        self._check_environment_set()
        
        url = f"{self.base_url}core/virtual-machines/{vm_id}/hard-reboot"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            print(f"Successfully initiated hard reboot for virtual machine with ID: {vm_id}")
        else:
            print(f"Failed to hard reboot virtual machine: {response.status_code} - {response.text}")
        
        return response
    
    def hibernate_virtual_machine(self, vm_id):
        """
        Initiates the hibernation of a virtual machine.

        :param vm_id: The ID of the virtual machine to hibernate.
        :return: The response from the API call.
        """
        self._check_environment_set()
        
        url = f"{self.base_url}core/virtual-machines/{vm_id}/hibernate"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            print(f"Successfully initiated hibernation for virtual machine with ID: {vm_id}")
        else:
            print(f"Failed to hibernate virtual machine: {response.status_code} - {response.text}")
        
        return response

    def restore_hibernated_virtual_machine(self, vm_id):
        """
        Resumes a virtual machine from hibernation.

        :param vm_id: The ID of the virtual machine to restore from hibernation.
        :return: The response from the API call.
        """
        self._check_environment_set()
        
        url = f"{self.base_url}core/virtual-machines/{vm_id}/hibernate-restore"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            print(f"Successfully restored virtual machine with ID: {vm_id} from hibernation")
        else:
            print(f"Failed to restore virtual machine from hibernation: {response.status_code} - {response.text}")
        
        return response

    def delete_virtual_machine(self, vm_id):
        """
        Permanently deletes a virtual machine.

        :param vm_id: The ID of the virtual machine to delete.
        :return: The response from the API call.
        """
        self._check_environment_set()
        
        url = f"{self.base_url}core/virtual-machines/{vm_id}"
        
        response = requests.delete(url, headers=self.headers)
        
        if response.status_code == 204:  # Assuming 204 No Content is returned on successful deletion
            print(f"Successfully deleted virtual machine with ID: {vm_id}")
        else:
            print(f"Failed to delete virtual machine: {response.status_code} - {response.text}")
        
        return response

    def attach_public_ip(self, vm_id):
        """
        Attaches a public IP address to a virtual machine.

        :param vm_id: The ID of the virtual machine to attach a public IP to.
        :return: The response from the API call.
        """
        self._check_environment_set()
        
        url = f"{self.base_url}core/virtual-machines/{vm_id}/attach-floatingip"
        
        response = requests.post(url, headers=self.headers)
        
        if response.status_code == 200:
            result = response.json()
            ip_address = result.get('floating_ip', 'Unknown')
            print(f"Successfully attached public IP {ip_address} to virtual machine with ID: {vm_id}")
        else:
            print(f"Failed to attach public IP to virtual machine: {response.status_code} - {response.text}")
        
        return response

    def detach_public_ip(self, vm_id):
        """
        Removes a public IP address from a virtual machine.

        :param vm_id: The ID of the virtual machine to detach the public IP from.
        :return: The response from the API call.
        """
        self._check_environment_set()
        
        url = f"{self.base_url}core/virtual-machines/{vm_id}/detach-floatingip"
        
        response = requests.post(url, headers=self.headers)
        
        if response.status_code == 200:
            print(f"Successfully detached public IP from virtual machine with ID: {vm_id}")
        else:
            print(f"Failed to detach public IP from virtual machine: {response.status_code} - {response.text}")
        
        return response

    def list_virtual_machines(self):
        """
        Lists all virtual machines in the current environment.

        :return: The response from the API call, containing the list of virtual machines.
        """
        self._check_environment_set()
        
        url = f"{self.base_url}core/virtual-machines"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            vms = response.json()
            print(f"Successfully retrieved {len(vms)} virtual machines.")
            for vm in vms:
                print(f"VM ID: {vm.get('id')}, Name: {vm.get('name')}, Status: {vm.get('status')}")
        else:
            print(f"Failed to retrieve virtual machines: {response.status_code} - {response.text}")
        
        return response
    
    def retrieve_vm_details(self, vm_id):
        """
        Lists all virtual machines in the current environment.

        :return: The response from the API call, containing the list of virtual machines.
        """
        self._check_environment_set()
        
        url = f"{self.base_url}core/virtual-machines/{vm_id}"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            response = response.json()
        else:
            print(f"Failed to retrieve virtual machines: {response.status_code} - {response.text}")
        
        return response
    
    def get_floating_ip(self, vm_id):
        """
        Lists all virtual machines in the current environment.

        :return: The response from the API call, containing the list of virtual machines.
        """
        self._check_environment_set()
        response = self.retrieve_vm_details(vm_id)
        floating_ip = response['instance']['floating_ip']
        return floating_ip

    def create_profile(self, name, environment_name, image_name, flavor_name, key_name, count,
                    assign_floating_ip=False, create_bootable_volume=False, user_data="",
                    callback_url="", description=None):
        """
        Creates a new profile with the given parameters.

        :param name: The name of the profile being created (max 50 characters).
        :param environment_name: Name of the environment for the virtual machine.
        :param image_name: Name of the operating system image.
        :param flavor_name: Name of the flavor for hardware configuration.
        :param key_name: Name of the SSH keypair.
        :param count: Number of virtual machines to be deployed.
        :param assign_floating_ip: Whether to assign a public IP address (default False).
        :param create_bootable_volume: Whether to create a bootable volume (default False).
        :param user_data: Initialization configuration data (default "").
        :param callback_url: URL for callback events (default "").
        :param description: An optional description for the profile (max 150 characters).
        :return: The response from the API call.
        """
        if len(name) > 50:
            raise ValueError("Profile name must not exceed 50 characters.")
        
        if description and len(description) > 150:
            raise ValueError("Profile description must not exceed 150 characters.")

        url = f"{self.base_url}core/profiles"
        
        data = {
            "environment_name": environment_name,
            "image_name": image_name,
            "flavor_name": flavor_name,
            "key_name": key_name,
            "count": count,
            "assign_floating_ip": str(assign_floating_ip).lower(),
            "create_bootable_volume": str(create_bootable_volume).lower(),
            "user_data": user_data,
            "callback_url": callback_url
        }

        payload = {
            "name": name,
            "data": data
        }
        
        if description:
            payload["description"] = description

        # Validate count is an integer
        if not isinstance(count, int):
            raise ValueError("'count' must be an integer.")

        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 201:
            print("Profile created successfully.")
        else:
            print(f"Failed to create profile: {response.status_code} - {response.text}")
        
        return response

    def list_profiles(self):
        """
        Lists all profiles.

        :return: The response from the API call.
        """
        url = f"{self.base_url}core/profiles"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            print("Profiles listed successfully.")
        else:
            print(f"Failed to list profiles: {response.status_code} - {response.text}")
        
        return response

    def retrieve_profile(self, id):
        """
        Retrieves details of a specific profile.

        :param id: The unique identifier of the profile.
        :return: The response from the API call.
        """
        url = f"{self.base_url}core/profiles/{id}"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            print(f"Profile {id} retrieved successfully.")
        else:
            print(f"Failed to retrieve profile {id}: {response.status_code} - {response.text}")
        
        return response

    def delete_profile(self, id):
        """
        Deletes a specific profile.

        :param id: The unique identifier of the profile to be deleted.
        :return: The response from the API call.
        """
        url = f"{self.base_url}core/profiles/{id}"
        
        response = requests.delete(url, headers=self.headers)
        
        if response.status_code == 204:  # 204 typically indicates successful deletion with no content returned
            print(f"Profile {id} deleted successfully.")
        else:
            print(f"Failed to delete profile {id}: {response.status_code} - {response.text}")
        
        return response


    def list_regions(self):
        """
        Lists all available regions.

        :return: The response from the API call.
        """
        url = f"{self.base_url}core/regions"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            print("Regions listed successfully.")
        else:
            print(f"Failed to list regions: {response.status_code} - {response.text}")
        
        return response

    def list_flavors(self, region=None):
        """
        Lists all available flavors, optionally filtered by region.

        :param region: Optional. The region to filter flavors (e.g., "NORWAY-1" or "CANADA-1").
        :return: The response from the API call.
        """
        url = f"{self.base_url}core/flavors"
        params = {}
        if region:
            if region not in self.valid_regions:
                raise ValueError(f"Invalid region specified. Valid regions are: {', '.join(self.valid_regions)}")
            params['region'] = region
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            print("Flavors listed successfully.")
        else:
            print(f"Failed to list flavors: {response.status_code} - {response.text}")
        
        return response

    def list_images(self, region=None):
        """
        Lists all available images, optionally filtered by region.

        :param region: Optional. The region to filter images (e.g., "NORWAY-1" or "CANADA-1").
        :return: The response from the API call.
        """
        url = f"{self.base_url}core/images"
        params = {}
        if region:
            if region not in self.valid_regions:
                raise ValueError(f"Invalid region specified. Valid regions are: {', '.join(self.valid_regions)}")
            params['region'] = region
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            print("Images listed successfully.")
        else:
            print(f"Failed to list images: {response.status_code} - {response.text}")
        
        return response

    def retrieve_gpu_stock(self):
        """
        Retrieves the current GPU stock information.

        :return: The response from the API call.
        """
        url = f"{self.base_url}core/stocks"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            print("GPU stock retrieved successfully.")
        else:
            print(f"Failed to retrieve GPU stock: {response.status_code} - {response.text}")
        
        return response


"""Test this out"""


"""
hyperstack.set_environment("development-CA")
response = hyperstack.create_vm(
        name="ollama-server2",
        create_bootable_volume=True,
        image_name="Ubuntu Server 22.04 LTS R535 CUDA 12.2",
        key_name="development-key-ca",
        flavor_name="n3-H100x4",
        assign_floating_ip=True,
        user_data="#!/bin/bash\n\n# Set up docker\n\n## Add Docker's official GPG key:\nsudo apt-get update\nsudo apt-get install -y ca-certificates curl gnupg\nsudo install -m 0755 -d /etc/apt/keyrings\ncurl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --yes --dearmor -o /etc/apt/keyrings/docker.gpg\nsudo chmod a+r /etc/apt/keyrings/docker.gpg\n\n## Add the repository to Apt sources:\necho \\\n\"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \\\n$(. /etc/os-release && echo $VERSION_CODENAME) stable\" | \\\nsudo tee /etc/apt/sources.list.d/docker.list > /dev/null\nsudo apt-get update\n\n## Install docker\nsudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin\n\n## Add docker group to ubuntu user\nsudo usermod -aG docker ubuntu\nsudo usermod -aG docker $USER\n\nsudo apt-get install nvidia-container-toolkit -y\n\n## Configure docker\n\nsudo nvidia-ctk runtime configure --runtime=docker\n\nsudo systemctl restart docker\n\nnewgrp docker\ndocker run -d --gpus all -v /usr/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu -v /usr/bin/nvidia-smi:/usr/bin/nvidia-smi -v ollama:/root/.ollama -p 11434:11434 -e OLLAMA_HOST=0.0.0.0 --name ollama ollama/ollama"
    )
"""


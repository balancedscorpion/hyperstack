import json
import os

import requests

from .api import environments, flavors, images, network, profiles, regions, stock, virtual_machines, volumes


class Hyperstack:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("HYPERSTACK_API_KEY")
        if not self.api_key:
            raise EnvironmentError("HYPERSTACK_API_KEY environment variable not set. Please set it to continue.")
        self.base_url = "https://infrahub-api.nexgencloud.com/v1/"
        self.headers = {"Content-Type": "application/json", "api_key": self.api_key}
        self.valid_regions = ["NORWAY-1", "CANADA-1"]
        self.environment = None

    def _check_environment_set(self):
        if self.environment is None:
            raise EnvironmentError("Environment is not set. Please set the environment using set_environment().")

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response

    def get(self, endpoint, **kwargs):
        """Send a GET request."""
        return json.loads(self._request("GET", endpoint, **kwargs).content)

    def post(self, endpoint, data=None, **kwargs):
        """Send a POST request."""
        return json.loads(self._request("POST", endpoint, json=data, **kwargs).content)

    def put(self, endpoint, data=None, **kwargs):
        """Send a PUT request."""
        return json.loads(self._request("PUT", endpoint, json=data, **kwargs).content)

    def delete(self, endpoint, **kwargs):
        """Send a DELETE request."""
        return json.loads(self._request("DELETE", endpoint, **kwargs).content)

    # Forward methods from profiles module
    create_profile = profiles.create_profile
    list_profiles = profiles.list_profiles
    retrieve_profile = profiles.retrieve_profile
    delete_profile = profiles.delete_profile

    # Forward methods from regions module
    list_regions = regions.list_regions
    get_region_enum = regions.get_region_enum

    # Forward methods from environments module
    create_environment = environments.create_environment
    list_environments = environments.list_environments
    get_environment = environments.get_environment
    set_environment = environments.set_environment
    delete_environment = environments.delete_environment
    update_environment = environments.update_environment

    # Forward methods from flavors module
    list_flavors = flavors.list_flavors
    get_flavor_enum = flavors.get_flavor_enum

    # Forward methods from images module
    list_images = images.list_images
    get_image_enum = images.get_image_enum

    # Forward methods from network module
    attach_public_ip = network.attach_public_ip
    detach_public_ip = network.detach_public_ip
    set_sg_rules = network.set_sg_rules
    delete_sg_rules = network.delete_sg_rules
    retrieve_vnc_path = network.retrieve_vnc_path
    retrieve_vnc_url = network.retrieve_vnc_url

    # Forward methods from stock module
    retrieve_gpu_stock = stock.retrieve_gpu_stock

    # Forward methods from virtual_machines module
    create_vm = virtual_machines.create_vm
    list_virtual_machines = virtual_machines.list_virtual_machines
    retrieve_vm_details = virtual_machines.retrieve_vm_details
    start_virtual_machine = virtual_machines.start_virtual_machine
    stop_virtual_machine = virtual_machines.stop_virtual_machine
    hard_reboot_virtual_machine = virtual_machines.hard_reboot_virtual_machine
    hibernate_virtual_machine = virtual_machines.hibernate_virtual_machine
    restore_hibernated_virtual_machine = virtual_machines.restore_hibernated_virtual_machine
    delete_virtual_machine = virtual_machines.delete_virtual_machine
    resize_virtual_machine = virtual_machines.resize_virtual_machine
    update_virtual_machine_labels = virtual_machines.update_virtual_machine_labels
    get_floating_ip = virtual_machines.get_floating_ip
    wait_for_vm_active = virtual_machines.wait_for_vm_active

    # Forward methods from volumes module
    create_volume = volumes.create_volume
    list_volumes = volumes.list_volumes
    list_volume_types = volumes.list_volume_types
    get_volume = volumes.get_volume
    delete_volume = volumes.delete_volume

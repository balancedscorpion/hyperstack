def create_vm(self, name, image_name, flavor_name, key_name="development-key", user_data="", create_bootable_volume=False, assign_floating_ip=False, count=1):
    self._check_environment_set()
    
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
    
    return self._request("POST", "core/virtual-machines", json=payload)

def list_virtual_machines(self):
    self._check_environment_set()
    return self._request("GET", "core/virtual-machines")

def retrieve_vm_details(self, vm_id):
    self._check_environment_set()
    return self._request("GET", f"core/virtual-machines/{vm_id}")

def start_virtual_machine(self, vm_id):
    self._check_environment_set()
    return self._request("GET", f"core/virtual-machines/{vm_id}/start")

def stop_virtual_machine(self, vm_id):
    self._check_environment_set()
    return self._request("GET", f"core/virtual-machines/{vm_id}/stop")

def hard_reboot_virtual_machine(self, vm_id):
    self._check_environment_set()
    return self._request("GET", f"core/virtual-machines/{vm_id}/hard-reboot")

def hibernate_virtual_machine(self, vm_id):
    self._check_environment_set()
    return self._request("GET", f"core/virtual-machines/{vm_id}/hibernate")

def restore_hibernated_virtual_machine(self, vm_id):
    self._check_environment_set()
    return self._request("GET", f"core/virtual-machines/{vm_id}/hibernate-restore")

def delete_virtual_machine(self, vm_id):
    self._check_environment_set()
    return self._request("DELETE", f"core/virtual-machines/{vm_id}")

def resize_virtual_machine(self, vm_id, flavor):
    self._check_environment_set()
    payload = {'flavor_name': flavor}
    return self._request("POST", f"core/virtual-machines/{vm_id}/resize", json=payload)

def update_virtual_machine_labels(self, vm_id, labels: list):
    self._check_environment_set()
    payload = {'labels': labels}
    return self._request("PUT", f"core/virtual-machines/{vm_id}/label", json=payload)

def get_floating_ip(self, vm_id):
    response = self.retrieve_vm_details(vm_id)
    return response.json()['instance']['floating_ip']
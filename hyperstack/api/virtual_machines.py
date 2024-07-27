from .. import hyperstack

def create_vm(name, image_name, flavor_name, key_name="development-key", user_data="", create_bootable_volume=False, assign_floating_ip=False, count=1):
    hyperstack._check_environment_set()
    
    payload = {
        "name": name,
        "environment_name": hyperstack.environment,
        "image_name": image_name,
        "create_bootable_volume": create_bootable_volume,
        "flavor_name": flavor_name,
        "key_name": key_name,
        "user_data": user_data,
        "assign_floating_ip": assign_floating_ip,
        "count": count
    }
    
    return hyperstack._request("POST", "core/virtual-machines", json=payload)

def list_virtual_machines():
    hyperstack._check_environment_set()
    return hyperstack._request("GET", "core/virtual-machines")

def retrieve_vm_details(vm_id):
    hyperstack._check_environment_set()
    return hyperstack._request("GET", f"core/virtual-machines/{vm_id}")

def start_virtual_machine(vm_id):
    hyperstack._check_environment_set()
    return hyperstack._request("GET", f"core/virtual-machines/{vm_id}/start")

def stop_virtual_machine(vm_id):
    hyperstack._check_environment_set()
    return hyperstack._request("GET", f"core/virtual-machines/{vm_id}/stop")

def hard_reboot_virtual_machine(vm_id):
    hyperstack._check_environment_set()
    return hyperstack._request("GET", f"core/virtual-machines/{vm_id}/hard-reboot")

def hibernate_virtual_machine(vm_id):
    hyperstack._check_environment_set()
    return hyperstack._request("GET", f"core/virtual-machines/{vm_id}/hibernate")

def restore_hibernated_virtual_machine(vm_id):
    hyperstack._check_environment_set()
    return hyperstack._request("GET", f"core/virtual-machines/{vm_id}/hibernate-restore")

def delete_virtual_machine(vm_id):
    hyperstack._check_environment_set()
    return hyperstack._request("DELETE", f"core/virtual-machines/{vm_id}")

def resize_virtual_machine(vm_id, flavor):
    hyperstack._check_environment_set()
    payload = {}
    payload['flavor_name']= flavor
    return hyperstack._request("POST", f"core/virtual-machines/{vm_id}/resize")

def update_virtual_machine_labels(vm_id, labels: list):
    hyperstack._check_environment_set()
    payload = {}
    payload['labels']= labels
    return hyperstack._request("PUT", f"core/virtual-machines/{vm_id}/label")

def get_floating_ip(vm_id):
    response = retrieve_vm_details(vm_id)
    return response.json()['instance']['floating_ip']








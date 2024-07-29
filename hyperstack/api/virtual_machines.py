import time


def create_vm(
    self,
    name,
    image_name,
    flavor_name,
    key_name="development-key",
    user_data="",
    create_bootable_volume=False,
    assign_floating_ip=False,
    count=1,
):
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
        "count": count,
    }

    return self.post("core/virtual-machines", data=payload)


def list_virtual_machines(self):
    self._check_environment_set()
    return self.get("core/virtual-machines")


def retrieve_vm_details(self, vm_id):
    self._check_environment_set()
    return self.get(f"core/virtual-machines/{vm_id}")


def start_virtual_machine(self, vm_id):
    self._check_environment_set()
    return self.get(f"core/virtual-machines/{vm_id}/start")


def stop_virtual_machine(self, vm_id):
    self._check_environment_set()
    return self.get(f"core/virtual-machines/{vm_id}/stop")


def hard_reboot_virtual_machine(self, vm_id):
    self._check_environment_set()
    return self.get(f"core/virtual-machines/{vm_id}/hard-reboot")


def hibernate_virtual_machine(self, vm_id):
    self._check_environment_set()
    return self.get(f"core/virtual-machines/{vm_id}/hibernate")


def restore_hibernated_virtual_machine(self, vm_id):
    self._check_environment_set()
    return self.get(f"core/virtual-machines/{vm_id}/hibernate-restore")


def delete_virtual_machine(self, vm_id):
    self._check_environment_set()
    return self.delete(f"core/virtual-machines/{vm_id}")


def resize_virtual_machine(self, vm_id, flavor):
    self._check_environment_set()
    payload = {'flavor_name': flavor}
    return self.post(f"core/virtual-machines/{vm_id}/resize", data=payload)


def update_virtual_machine_labels(self, vm_id, labels: list):
    self._check_environment_set()
    payload = {'labels': labels}
    return self.put(f"core/virtual-machines/{vm_id}/label", data=payload)


def get_floating_ip(self, vm_id):
    response = self.retrieve_vm_details(vm_id)
    return response['instance']['floating_ip']


def wait_for_vm_active(self, vm_id, max_attempts=4, initial_delay=20, delay=10, backoff_factor=1.5):
    current_delay = initial_delay
    time.sleep(current_delay)
    for attempt in range(max_attempts):
        vm_details = self.retrieve_vm_details(vm_id)
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

def attach_public_ip(self, vm_id):
    self._check_environment_set()
    return self.post(f"core/virtual-machines/{vm_id}/attach-floatingip")


def detach_public_ip(self, vm_id):
    self._check_environment_set()
    return self.post(f"core/virtual-machines/{vm_id}/detach-floatingip")


def set_sg_rules(
    self,
    vm_id,
    remote_ip_prefix="0.0.0.0/0",
    direction="ingress",
    ethertype="IPv4",
    protocol="tcp",
    port_range_min=None,
    port_range_max=None,
):
    self._check_environment_set()

    payload = {
        "remote_ip_prefix": remote_ip_prefix,
        "direction": direction,
        "ethertype": ethertype,
        "protocol": protocol,
    }

    if port_range_min is not None:
        payload["port_range_min"] = port_range_min
    if port_range_max is not None:
        payload["port_range_max"] = port_range_max

    return self.post(f"core/virtual-machines/{vm_id}/sg-rules", data=payload)


def delete_sg_rules(self, vm_id, sg_rule_id):
    self._check_environment_set()
    return self.delete(f"core/virtual-machines/{vm_id}/sg-rules/{sg_rule_id}")


def retrieve_vnc_path(self, vm_id):
    self._check_environment_set()
    return self.get(f"core/virtual-machines/{vm_id}/request-console")


def retrieve_vnc_url(self, vm_id, job_id):
    """
    Retrieves the VNC URL for a specific virtual machine.

    :param vm_id: The ID of the virtual machine for which to retrieve the VNC console.
    :param job_id: The ID of the job corresponding to the VNC console.
    :return: The response from the API call.
    """
    self._check_environment_set()
    return self.post(f"core/virtual-machines/{vm_id}/console/{job_id}")

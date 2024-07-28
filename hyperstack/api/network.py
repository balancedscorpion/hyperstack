import time

def attach_public_ip(self, vm_id):
    self._check_environment_set()
    return self._request("POST", f"core/virtual-machines/{vm_id}/attach-floatingip")

def detach_public_ip(self, vm_id):
    self._check_environment_set()
    return self._request("POST", f"core/virtual-machines/{vm_id}/detach-floatingip")

def set_sg_rules(self, vm_id, remote_ip_prefix="0.0.0.0/0", direction="ingress", ethertype="IPv4", protocol="tcp", port_range_min=None, port_range_max=None):
    self._check_environment_set()
    
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
    
    return self._request("POST", f"core/virtual-machines/{vm_id}/sg-rules", json=payload)

def delete_sg_rules(self, vm_id, sg_rule_id):
    self._check_environment_set()
    return self._request("DELETE", f"core/virtual-machines/{vm_id}/sg-rules/{sg_rule_id}")

def retrieve_vnc_path(self, vm_id):
    self._check_environment_set()
    return self._request("GET", f"core/virtual-machines/{vm_id}/request-console")

def retrieve_vnc_url(self, vm_id, job_id):
    """
    Retrieves the VNC URL for a specific virtual machine.

    :param vm_id: The ID of the virtual machine for which to retrieve the VNC console.
    :param job_id: The ID of the job corresponding to the VNC console.
    :return: The response from the API call.
    """
    self._check_environment_set()
    return self._request("POST", f"core/virtual-machines/{vm_id}/console/{job_id}")

def _execute_with_backoff(self, func, max_attempts=4, initial_delay=30, delay=10, backoff_factor=1.5, **kwargs):
    """
    Executes a function with a back-off strategy.

    :param func: The function to execute.
    :param max_attempts: Maximum number of attempts.
    :param initial_delay: Initial delay between attempts.
    :param delay: Delay between subsequent attempts.
    :param backoff_factor: Factor by which the delay increases after each attempt.
    :param kwargs: Keyword arguments to pass to the function.
    :return: The result of the function if it succeeds, or None if it fails after the maximum number of attempts.
    """
    attempts = 0
    time.sleep(initial_delay)
    
    while attempts < max_attempts:
        try:
            result = func(**kwargs)
            if result.status_code == 200:
                return result
            else:
                pass
        except Exception as e:
            print(f"Attempt {attempts + 1} encountered an error: {e}")

        time.sleep(delay)
        delay *= backoff_factor
        attempts += 1
    
    print("All attempts failed.")
    return None
def create_profile(
    self,
    name,
    environment_name,
    image_name,
    flavor_name,
    key_name,
    count,
    assign_floating_ip=False,
    create_bootable_volume=False,
    user_data="",
    callback_url="",
    description=None,
):
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

    if not isinstance(count, int):
        raise ValueError("'count' must be an integer.")

    data = {
        "environment_name": environment_name,
        "image_name": image_name,
        "flavor_name": flavor_name,
        "key_name": key_name,
        "count": count,
        "assign_floating_ip": str(assign_floating_ip).lower(),
        "create_bootable_volume": str(create_bootable_volume).lower(),
        "user_data": user_data,
        "callback_url": callback_url,
    }

    payload = {"name": name, "data": data}

    if description:
        payload["description"] = description

    return self.post("core/profiles", json=payload)


def list_profiles(self):
    """
    Lists all profiles.

    :return: The response from the API call.
    """
    return self.get("core/profiles")


def retrieve_profile(self, profile_id):
    """
    Retrieves details of a specific profile.

    :param profile_id: The unique identifier of the profile.
    :return: The response from the API call.
    """
    return self.get(f"core/profiles/{profile_id}")


def delete_profile(self, profile_id):
    """
    Deletes a specific profile.

    :param profile_id: The unique identifier of the profile to be deleted.
    :return: The response from the API call.
    """
    return self.delete(f"core/profiles/{profile_id}")

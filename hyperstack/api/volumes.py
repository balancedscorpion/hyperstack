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

    payload = {"name": name, "environment_name": self.environment, "volume_type": volume_type, "size": size}

    if image_id is not None:
        payload["image_id"] = image_id
    if description is not None:
        payload["description"] = description
    if callback_url is not None:
        payload["callback_url"] = callback_url

    return self.post("core/volumes", data=payload)


def list_volumes(self):
    """
    Lists all volumes in the current environment.

    :return: The response from the API call, containing the list of volumes.
    """
    self._check_environment_set()
    return self.get("core/volumes")


def list_volume_types(self):
    """
    Lists all available volume types.

    :return: The response from the API call, containing the list of volume types.
    """
    return self.get("core/volume-types")


def get_volume(self, volume_id):
    """
    Retrieves details of a specific volume.

    :param volume_id: The ID of the volume to retrieve.
    :return: The response from the API call, containing the volume details.
    """
    self._check_environment_set()
    return self.get(f"core/volumes/{volume_id}")


def delete_volume(self, volume_id):
    """
    Deletes a specific volume.

    :param volume_id: The ID of the volume to delete.
    :return: The response from the API call.
    """
    self._check_environment_set()
    return self.delete(f"core/volumes/{volume_id}")

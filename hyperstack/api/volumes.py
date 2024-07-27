from .. import hyperstack

def create_volume(name, volume_type, size=50, image_id=None, description=None, callback_url=None):
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
    hyperstack._check_environment_set()
    
    payload = {
        "name": name,
        "environment_name": hyperstack.environment,
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
    
    return hyperstack._request("POST", "core/volumes", json=payload)

def list_volumes():
    """
    Lists all volumes in the current environment.

    :return: The response from the API call, containing the list of volumes.
    """
    hyperstack._check_environment_set()
    return hyperstack._request("GET", "core/volumes")

def list_volume_types():
    """
    Lists all available volume types.

    :return: The response from the API call, containing the list of volume types.
    """
    return hyperstack._request("GET", "core/volume-types")

def get_volume(volume_id):
    """
    Retrieves details of a specific volume.

    :param volume_id: The ID of the volume to retrieve.
    :return: The response from the API call, containing the volume details.
    """
    hyperstack._check_environment_set()
    return hyperstack._request("GET", f"core/volumes/{volume_id}")

def delete_volume(volume_id):
    """
    Deletes a specific volume.

    :param volume_id: The ID of the volume to delete.
    :return: The response from the API call.
    """
    hyperstack._check_environment_set()
    return hyperstack._request("DELETE", f"core/volumes/{volume_id}")
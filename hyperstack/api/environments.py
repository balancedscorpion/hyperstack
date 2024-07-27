from .. import hyperstack
from .regions import Region, get_region_enum

def create_environment(name, region_str):
    """
    Creates a new environment with the given name and region.

    :param name: The name of the environment.
    :param region_str: The region where the environment will be created (string).
    :return: The response from the API call.
    """
    try:
        region = get_region_enum(region_str)
    except ValueError as e:
        raise ValueError(f"Invalid region specified: {region_str}. {str(e)}")
    
    payload={
        "name": name,
        "region": region.value
    }

    return hyperstack._request("POST","core/environments",json=payload)

def list_environments():
    """
    Lists all environments.

    :return: The response from the API call.
    """
    return hyperstack._request("GET", "core/environments")

def get_environment(environment_id):
    """
    Retrieves details of a specific environment.

    :param environment_id: The ID of the environment to retrieve.
    :return: The response from the API call.
    """
    return hyperstack._request("GET", f"core/environments/{environment_id}")

def set_environment(environment_id):
    """
    Retrieves details of a specific environment.

    :param environment_id: The ID of the environment to retrieve.
    :return: The response from the API call.
    """
    return hyperstack._request("GET", f"core/environments/{environment_id}")

def delete_environment(environment_id):
    """
    Deletes a specific environment.

    :param environment_id: The ID of the environment to delete.
    :return: The response from the API call.
    """
    return hyperstack._request("DELETE", f"core/environments/{environment_id}")

def update_environment(environment_id, name):
    """
    Updates an existing environment.

    :param environment_id: The ID of the environment to update.
    :param name: (Optional) The new name for the environment.
    """
    payload = {}
    payload["name"] = name

    return hyperstack._request("PUT", f"core/environments/{environment_id}", json=payload)


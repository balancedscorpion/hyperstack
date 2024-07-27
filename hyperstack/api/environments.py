from ..client import hyperstack

def create_environment(name, region):
    """
    Creates a new environment with the given name and region.

    :param name: The name of the environment.
    :param region: The region where the environment will be created.
    :return: The response from the API call.
    """
    if region not in hyperstack.valid_regions:
        raise ValueError(f"Invalid region specified. Valid regions are: {', '.join(hyperstack.valid_regions)}")
    
    payload = {
        "name": name,
        "region": region
    }
    
    return hyperstack._request("POST", "core/environments", json=payload)

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
    if name is not None:
        payload["name"] = name

    return hyperstack._request("PUT", f"core/environments/{environment_id}", json=payload)


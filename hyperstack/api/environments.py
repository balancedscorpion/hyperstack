from .regions import get_region_enum


def create_environment(self, name, region_str):
    """
    Creates a new environment with the given name and region.

    :param name: The name of the environment.
    :param region_str: The region where the environment will be created (string).
    :return: The response from the API call.
    """
    try:
        region = get_region_enum(region_str)
    except ValueError as e:
        raise ValueError(f"Invalid region specified: {region_str}. {str(e)}") from e

    payload = {"name": name, "region": region.value}
    return self.post("POST", "core/environments", data=payload)


def list_environments(self):
    """
    Lists all environments.

    :return: The response from the API call.
    """
    return self.get("core/environments")


def get_environment(self, environment_id):
    """
    Retrieves details of a specific environment.

    :param environment_id: The ID of the environment to retrieve.
    :return: The response from the API call.
    """
    return self.get(f"core/environments/{environment_id}")


def set_environment(self, environment_name):
    """
    Sets the current environment.

    :param environment_id: The ID of the environment to set.
    :return: The response from the API call.
    """
    self.environment = environment_name
    print(f"Environment set to: {environment_name}")


def delete_environment(self, environment_id):
    """
    Deletes a specific environment.

    :param environment_id: The ID of the environment to delete.
    :return: The response from the API call.
    """
    return self.delete(f"core/environments/{environment_id}")


def update_environment(self, environment_id, name):
    """
    Updates an existing environment.

    :param environment_id: The ID of the environment to update.
    :param name: The new name for the environment.
    :return: The response from the API call.
    """
    payload = {"name": name}
    return self.put(f"core/environments/{environment_id}", data=payload)

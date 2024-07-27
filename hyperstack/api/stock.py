from .. import hyperstack

def retrieve_gpu_stock():
    """
    Retrieves the current GPU stock information.

    :return: The response from the API call.
    """
    return hyperstack._request("GET", "core/stocks")
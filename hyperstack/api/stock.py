def retrieve_gpu_stock(self):
    """
    Retrieves the current GPU stock information.

    :return: The response from the API call.
    """
    return self.get("core/stocks")

from .regions import Region


def list_images(self, region=None):
    """
    Lists all available regions or filters by a specific region.

    :param region: Optional. The region to filter (enum: Region.NORWAY_1 or Region.CANADA_1).
    :return: The response from the API call.
    """
    params = {}
    if region:
        if not isinstance(region, Region):
            raise ValueError(
                f"Invalid region specified. Use Region enum: {', '.join([r.value for r in Region])}"
            ) from None
        params['region'] = region.value
    return self.get("core/images", params=params)


def get_image_enum(region_string):
    """
    Convert a string representation of a region to the Region enum.

    :param region_string: String representation of the region (e.g., "NORWAY-1" or "CANADA-1")
    :return: Corresponding Region enum value
    """
    try:
        return Region(region_string)
    except ValueError as e:
        raise ValueError(f"Invalid region string. Valid regions are: {', '.join([r.value for r in Region])}") from e

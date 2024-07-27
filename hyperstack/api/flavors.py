from ..client import hyperstack
from enum import Enum
from .regions import Region

def list_flavors(region=None):
    """
    Lists all available regions or filters by a specific region.

    :param region: Optional. The region to filter (enum: Region.NORWAY_1 or Region.CANADA_1).
    :return: The response from the API call.

    Query string parameters:
    region (enum): Optional. Include a region name in the query string of the request
                   to return only the information for the specified region.
                   If no region is included, information for all regions will be retrieved.
    Possible enum values: NORWAY-1 or CANADA-1.
    """
    params = {}
    if region:
        if not isinstance(region, Region):
            raise ValueError(f"Invalid region specified. Use Region enum: {', '.join([r.value for r in Region])}")
        params['region'] = region.value
    
    return hyperstack._request("GET", "core/flavors", params=params)

def get_flavor_enum(region_string):
    """
    Convert a string representation of a region to the Region enum.

    :param region_string: String representation of the region (e.g., "NORWAY-1" or "CANADA-1")
    :return: Corresponding Region enum value
    """
    try:
        return Region(region_string)
    except ValueError:
        raise ValueError(f"Invalid region string. Valid regions are: {', '.join([r.value for r in Region])}")

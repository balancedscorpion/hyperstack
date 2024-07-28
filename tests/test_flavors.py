from unittest.mock import patch

import pytest

from hyperstack.api.flavors import get_flavor_enum, list_flavors
from hyperstack.api.regions import Region


@pytest.fixture
def mock_hyperstack():
    with patch('hyperstack.Hyperstack') as MockHyperstack:
        mock_instance = MockHyperstack.return_value
        mock_instance.get.return_value = {"status": "success", "data": {"flavors": []}}
        yield mock_instance


def test_list_flavors_no_region(mock_hyperstack):
    result = list_flavors(mock_hyperstack)
    mock_hyperstack.get.assert_called_once_with("core/flavors", params={})
    assert result == {"status": "success", "data": {"flavors": []}}


def test_list_flavors_with_valid_region(mock_hyperstack):
    result = list_flavors(mock_hyperstack, Region.NORWAY_1)
    mock_hyperstack.get.assert_called_once_with("core/flavors", params={"region": "NORWAY-1"})
    assert result == {"status": "success", "data": {"flavors": []}}


def test_list_flavors_with_invalid_region(mock_hyperstack):
    with pytest.raises(ValueError, match="Invalid region specified. Use Region enum: NORWAY-1, CANADA-1"):
        list_flavors(mock_hyperstack, "INVALID-REGION")


def test_get_flavor_enum_valid():
    assert get_flavor_enum("NORWAY-1") == Region.NORWAY_1
    assert get_flavor_enum("CANADA-1") == Region.CANADA_1


def test_get_flavor_enum_invalid():
    with pytest.raises(ValueError, match="Invalid region string. Valid regions are: NORWAY-1, CANADA-1"):
        get_flavor_enum("INVALID-REGION")


def test_list_flavors_region_enum_creation(mock_hyperstack):
    result = list_flavors(mock_hyperstack, Region.NORWAY_1)
    mock_hyperstack.get.assert_called_once_with("core/flavors", params={"region": "NORWAY-1"})
    assert result == {"status": "success", "data": {"flavors": []}}

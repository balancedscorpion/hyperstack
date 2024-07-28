from unittest.mock import MagicMock, patch

import pytest

from hyperstack.api.regions import Region, get_region_enum, list_regions


@pytest.fixture
def mock_hyperstack():
    with patch('hyperstack.Hyperstack') as MockHyperstack:
        mock_instance = MockHyperstack.return_value
        mock_instance.get.return_value = {"status": "success", "data": {}}
        yield mock_instance


def test_list_regions_no_filter(mock_hyperstack):
    result = list_regions(mock_hyperstack)
    mock_hyperstack.get.assert_called_once_with("core/regions", params={})
    assert result == {"status": "success", "data": {}}


def test_list_regions_with_filter(mock_hyperstack):
    result = list_regions(mock_hyperstack, Region.NORWAY_1)
    mock_hyperstack.get.assert_called_once_with("core/regions", params={"region": "NORWAY-1"})
    assert result == {"status": "success", "data": {}}


def test_list_regions_invalid_region():
    with pytest.raises(ValueError, match="Invalid region specified. Use Region enum: NORWAY-1, CANADA-1"):
        list_regions(MagicMock(), "INVALID-REGION")


def test_get_region_enum_valid():
    assert get_region_enum("NORWAY-1") == Region.NORWAY_1
    assert get_region_enum("CANADA-1") == Region.CANADA_1


def test_get_region_enum_invalid():
    with pytest.raises(ValueError, match="Invalid region string. Valid regions are: NORWAY-1, CANADA-1"):
        get_region_enum("INVALID-REGION")

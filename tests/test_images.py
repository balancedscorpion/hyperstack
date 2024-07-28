import pytest
from unittest.mock import patch, MagicMock
from hyperstack import Hyperstack
from hyperstack.api.regions import Region
from hyperstack.api.images import list_images, get_image_enum

@pytest.fixture
def mock_hyperstack():
    with patch('hyperstack.Hyperstack') as MockHyperstack:
        mock_instance = MockHyperstack.return_value
        mock_instance.get.return_value = {"status": "success", "data": {"images": []}}
        yield mock_instance

def test_list_images_no_region(mock_hyperstack):
    result = list_images(mock_hyperstack)
    mock_hyperstack.get.assert_called_once_with("core/images", params={})
    assert result == {"status": "success", "data": {"images": []}}

def test_list_images_with_valid_region(mock_hyperstack):
    result = list_images(mock_hyperstack, Region.NORWAY_1)
    mock_hyperstack.get.assert_called_once_with("core/images", params={"region": "NORWAY-1"})
    assert result == {"status": "success", "data": {"images": []}}

def test_list_images_with_invalid_region(mock_hyperstack):
    with pytest.raises(ValueError, match="Invalid region specified. Use Region enum: NORWAY-1, CANADA-1"):
        list_images(mock_hyperstack, "INVALID-REGION")

def test_get_image_enum_valid():
    assert get_image_enum("NORWAY-1") == Region.NORWAY_1
    assert get_image_enum("CANADA-1") == Region.CANADA_1

def test_get_image_enum_invalid():
    with pytest.raises(ValueError, match="Invalid region string. Valid regions are: NORWAY-1, CANADA-1"):
        get_image_enum("INVALID-REGION")

def test_list_images_region_enum_creation(mock_hyperstack):
    result = list_images(mock_hyperstack, Region.NORWAY_1)
    mock_hyperstack.get.assert_called_once_with("core/images", params={"region": "NORWAY-1"})
    assert result == {"status": "success", "data": {"images": []}}
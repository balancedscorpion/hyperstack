from unittest.mock import MagicMock, patch

import pytest

from hyperstack.api.volumes import create_volume, delete_volume, get_volume, list_volume_types, list_volumes


@pytest.fixture
def mock_hyperstack():
    with patch('hyperstack.Hyperstack') as MockHyperstack:
        mock_instance = MockHyperstack.return_value
        mock_instance.post.return_value = {"status": "success", "data": {"id": "volume-123"}}
        mock_instance.get.return_value = {"status": "success", "data": {}}
        mock_instance.delete.return_value = {"status": "success", "data": {}}
        mock_instance.environment = "test-env"
        mock_instance._check_environment_set = MagicMock()
        yield mock_instance


def test_create_volume(mock_hyperstack):
    result = create_volume(mock_hyperstack, name="test-volume", volume_type="ssd", size=100)
    expected_payload = {"name": "test-volume", "environment_name": "test-env", "volume_type": "ssd", "size": 100}
    mock_hyperstack.post.assert_called_once_with("core/volumes", data=expected_payload)
    assert result == {"status": "success", "data": {"id": "volume-123"}}


def test_create_volume_with_optional_params(mock_hyperstack):
    result = create_volume(
        mock_hyperstack,
        name="test-volume",
        volume_type="ssd",
        size=100,
        image_id="image-123",
        description="Test volume",
        callback_url="https://example.com/callback",
    )
    expected_payload = {
        "name": "test-volume",
        "environment_name": "test-env",
        "volume_type": "ssd",
        "size": 100,
        "image_id": "image-123",
        "description": "Test volume",
        "callback_url": "https://example.com/callback",
    }
    mock_hyperstack.post.assert_called_once_with("core/volumes", data=expected_payload)
    assert result == {"status": "success", "data": {"id": "volume-123"}}


def test_list_volumes(mock_hyperstack):
    result = list_volumes(mock_hyperstack)
    mock_hyperstack.get.assert_called_once_with("core/volumes")
    assert result == {"status": "success", "data": {}}


def test_list_volume_types(mock_hyperstack):
    result = list_volume_types(mock_hyperstack)
    mock_hyperstack.get.assert_called_once_with("core/volume-types")
    assert result == {"status": "success", "data": {}}


def test_get_volume(mock_hyperstack):
    result = get_volume(mock_hyperstack, "volume-123")
    mock_hyperstack.get.assert_called_once_with("core/volumes/volume-123")
    assert result == {"status": "success", "data": {}}


def test_delete_volume(mock_hyperstack):
    result = delete_volume(mock_hyperstack, "volume-123")
    mock_hyperstack.delete.assert_called_once_with("core/volumes/volume-123")
    assert result == {"status": "success", "data": {}}


def test_environment_not_set(mock_hyperstack):
    mock_hyperstack.environment = None
    mock_hyperstack._check_environment_set.side_effect = EnvironmentError("Environment is not set")
    with pytest.raises(EnvironmentError, match="Environment is not set"):
        create_volume(mock_hyperstack, name="test-volume", volume_type="ssd")

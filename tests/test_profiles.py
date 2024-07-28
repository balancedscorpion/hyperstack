from unittest.mock import patch

import pytest

from hyperstack.api.profiles import create_profile, delete_profile, list_profiles, retrieve_profile


@pytest.fixture
def mock_hyperstack():
    with patch('hyperstack.Hyperstack') as MockHyperstack:
        mock_instance = MockHyperstack.return_value
        mock_instance.post.return_value = {"status": "success", "data": {"id": "profile-123"}}
        mock_instance.get.return_value = {"status": "success", "data": {}}
        mock_instance.delete.return_value = {"status": "success", "data": {}}
        yield mock_instance


def test_create_profile_success(mock_hyperstack):
    result = create_profile(
        mock_hyperstack,
        name="test-profile",
        environment_name="test-env",
        image_name="ubuntu-20.04",
        flavor_name="standard-1",
        key_name="test-key",
        count=1,
    )

    expected_payload = {
        "name": "test-profile",
        "data": {
            "environment_name": "test-env",
            "image_name": "ubuntu-20.04",
            "flavor_name": "standard-1",
            "key_name": "test-key",
            "count": 1,
            "assign_floating_ip": "false",
            "create_bootable_volume": "false",
            "user_data": "",
            "callback_url": "",
        },
    }

    mock_hyperstack.post.assert_called_once_with("core/profiles", json=expected_payload)
    assert result == {"status": "success", "data": {"id": "profile-123"}}


def test_create_profile_with_description(mock_hyperstack):
    result = create_profile(
        mock_hyperstack,
        name="test-profile",
        environment_name="test-env",
        image_name="ubuntu-20.04",
        flavor_name="standard-1",
        key_name="test-key",
        count=1,
        description="Test profile description",
    )

    expected_payload = {
        "name": "test-profile",
        "description": "Test profile description",
        "data": {
            "environment_name": "test-env",
            "image_name": "ubuntu-20.04",
            "flavor_name": "standard-1",
            "key_name": "test-key",
            "count": 1,
            "assign_floating_ip": "false",
            "create_bootable_volume": "false",
            "user_data": "",
            "callback_url": "",
        },
    }

    mock_hyperstack.post.assert_called_once_with("core/profiles", json=expected_payload)
    assert result == {"status": "success", "data": {"id": "profile-123"}}


def test_create_profile_name_too_long(mock_hyperstack):
    with pytest.raises(ValueError, match="Profile name must not exceed 50 characters."):
        create_profile(
            mock_hyperstack,
            name="a" * 51,
            environment_name="test-env",
            image_name="ubuntu-20.04",
            flavor_name="standard-1",
            key_name="test-key",
            count=1,
        )


def test_create_profile_description_too_long(mock_hyperstack):
    with pytest.raises(ValueError, match="Profile description must not exceed 150 characters."):
        create_profile(
            mock_hyperstack,
            name="test-profile",
            environment_name="test-env",
            image_name="ubuntu-20.04",
            flavor_name="standard-1",
            key_name="test-key",
            count=1,
            description="a" * 151,
        )


def test_create_profile_invalid_count(mock_hyperstack):
    with pytest.raises(ValueError, match="'count' must be an integer."):
        create_profile(
            mock_hyperstack,
            name="test-profile",
            environment_name="test-env",
            image_name="ubuntu-20.04",
            flavor_name="standard-1",
            key_name="test-key",
            count="1",  # String instead of integer
        )


def test_list_profiles(mock_hyperstack):
    result = list_profiles(mock_hyperstack)
    mock_hyperstack.get.assert_called_once_with("core/profiles")
    assert result == {"status": "success", "data": {}}


def test_retrieve_profile(mock_hyperstack):
    result = retrieve_profile(mock_hyperstack, "profile-123")
    mock_hyperstack.get.assert_called_once_with("core/profiles/profile-123")
    assert result == {"status": "success", "data": {}}


def test_delete_profile(mock_hyperstack):
    result = delete_profile(mock_hyperstack, "profile-123")
    mock_hyperstack.delete.assert_called_once_with("core/profiles/profile-123")
    assert result == {"status": "success", "data": {}}

import pytest
from unittest.mock import patch, MagicMock
from hyperstack import Hyperstack
from hyperstack.api.regions import Region
from hyperstack.api.environments import (
    create_environment, list_environments, get_environment,
    set_environment, delete_environment, update_environment
)

@pytest.fixture
def mock_hyperstack():
    with patch('hyperstack.Hyperstack') as MockHyperstack:
        mock_instance = MockHyperstack.return_value
        mock_instance.post.return_value = {"status": "success", "data": {"id": "env-123"}}
        mock_instance.get.return_value = {"status": "success", "data": {}}
        mock_instance.delete.return_value = {"status": "success", "data": {}}
        mock_instance.put.return_value = {"status": "success", "data": {}}
        yield mock_instance

def test_create_environment(mock_hyperstack):
    result = create_environment(mock_hyperstack, "test-env", "NORWAY-1")
    mock_hyperstack.post.assert_called_once_with(
        "POST", "core/environments", 
        data={"name": "test-env", "region": "NORWAY-1"}
    )
    assert result == {"status": "success", "data": {"id": "env-123"}}

def test_create_environment_invalid_region(mock_hyperstack):
    with pytest.raises(ValueError, match="Invalid region specified: INVALID-REGION"):
        create_environment(mock_hyperstack, "test-env", "INVALID-REGION")

def test_list_environments(mock_hyperstack):
    result = list_environments(mock_hyperstack)
    mock_hyperstack.get.assert_called_once_with("core/environments")
    assert result == {"status": "success", "data": {}}

def test_get_environment(mock_hyperstack):
    result = get_environment(mock_hyperstack, "env-123")
    mock_hyperstack.get.assert_called_once_with("core/environments/env-123")
    assert result == {"status": "success", "data": {}}

def test_set_environment(mock_hyperstack, capsys):
    set_environment(mock_hyperstack, "test-env")
    assert mock_hyperstack.environment == "test-env"
    captured = capsys.readouterr()
    assert captured.out == "Environment set to: test-env\n"

def test_delete_environment(mock_hyperstack):
    result = delete_environment(mock_hyperstack, "env-123")
    mock_hyperstack.delete.assert_called_once_with("core/environments/env-123")
    assert result == {"status": "success", "data": {}}

def test_update_environment(mock_hyperstack):
    result = update_environment(mock_hyperstack, "env-123", "new-name")
    mock_hyperstack.put.assert_called_once_with(
        "core/environments/env-123", 
        data={"name": "new-name"}
    )
    assert result == {"status": "success", "data": {}}

@patch('hyperstack.api.environments.get_region_enum')
def test_create_environment_with_region_enum(mock_get_region_enum, mock_hyperstack):
    mock_get_region_enum.return_value = Region.NORWAY_1
    result = create_environment(mock_hyperstack, "test-env", "NORWAY-1")
    mock_get_region_enum.assert_called_once_with("NORWAY-1")
    mock_hyperstack.post.assert_called_once_with(
        "POST", "core/environments", 
        data={"name": "test-env", "region": "NORWAY-1"}
    )
    assert result == {"status": "success", "data": {"id": "env-123"}}
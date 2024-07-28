import pytest
from unittest.mock import patch, MagicMock, call
import time
from hyperstack import Hyperstack
from hyperstack.api.network import (
    attach_public_ip, detach_public_ip, set_sg_rules, delete_sg_rules,
    retrieve_vnc_path, retrieve_vnc_url, _execute_with_backoff
)

@pytest.fixture
def mock_hyperstack():
    with patch('hyperstack.Hyperstack') as MockHyperstack:
        mock_instance = MockHyperstack.return_value
        mock_instance.post.return_value = {"status": "success", "data": {}}
        mock_instance.get.return_value = {"status": "success", "data": {}}
        mock_instance.delete.return_value = {"status": "success", "data": {}}
        mock_instance.environment = "test_env"
        mock_instance._check_environment_set = MagicMock()
        yield mock_instance

def test_attach_public_ip(mock_hyperstack):
    result = attach_public_ip(mock_hyperstack, "vm-123")
    mock_hyperstack.post.assert_called_once_with("core/virtual-machines/vm-123/attach-floatingip")
    assert result == {"status": "success", "data": {}}

def test_detach_public_ip(mock_hyperstack):
    result = detach_public_ip(mock_hyperstack, "vm-123")
    mock_hyperstack.post.assert_called_once_with("core/virtual-machines/vm-123/detach-floatingip")
    assert result == {"status": "success", "data": {}}

def test_set_sg_rules(mock_hyperstack):
    result = set_sg_rules(mock_hyperstack, "vm-123", port_range_min=80, port_range_max=80)
    expected_payload = {
        "remote_ip_prefix": "0.0.0.0/0",
        "direction": "ingress",
        "ethertype": "IPv4",
        "protocol": "tcp",
        "port_range_min": 80,
        "port_range_max": 80
    }
    mock_hyperstack.post.assert_called_once_with("core/virtual-machines/vm-123/sg-rules", data=expected_payload)
    assert result == {"status": "success", "data": {}}

def test_delete_sg_rules(mock_hyperstack):
    result = delete_sg_rules(mock_hyperstack, "vm-123", "rule-456")
    mock_hyperstack.delete.assert_called_once_with("core/virtual-machines/vm-123/sg-rules/rule-456")
    assert result == {"status": "success", "data": {}}

def test_retrieve_vnc_path(mock_hyperstack):
    result = retrieve_vnc_path(mock_hyperstack, "vm-123")
    mock_hyperstack.get.assert_called_once_with("core/virtual-machines/vm-123/request-console")
    assert result == {"status": "success", "data": {}}

def test_retrieve_vnc_url(mock_hyperstack):
    result = retrieve_vnc_url(mock_hyperstack, "vm-123", "job-789")
    mock_hyperstack.post.assert_called_once_with("core/virtual-machines/vm-123/console/job-789")
    assert result == {"status": "success", "data": {}}

@patch('time.sleep')
def test_execute_with_backoff_success(mock_sleep, mock_hyperstack):
    mock_func = MagicMock()
    mock_func.return_value.status_code = 200
    
    result = _execute_with_backoff(mock_hyperstack, mock_func, initial_delay=0, delay=0)
    
    assert mock_func.call_count == 1
    assert result.status_code == 200
    mock_sleep.assert_called_once_with(0)  # Initial delay

@patch('time.sleep')
def test_execute_with_backoff_failure(mock_sleep, mock_hyperstack):
    mock_func = MagicMock()
    mock_func.return_value.status_code = 500
    
    result = _execute_with_backoff(mock_hyperstack, mock_func, max_attempts=3, initial_delay=0, delay=0)
    
    assert mock_func.call_count == 3
    assert result is None
    assert mock_sleep.call_count == 4  # Initial delay + 3 retries

def test_environment_not_set(mock_hyperstack):
    mock_hyperstack._check_environment_set.side_effect = EnvironmentError("Environment is not set")
    with pytest.raises(EnvironmentError, match="Environment is not set"):
        attach_public_ip(mock_hyperstack, "vm-123")
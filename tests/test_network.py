from unittest.mock import MagicMock, patch

import pytest

from hyperstack.api.network import (
    attach_public_ip,
    delete_sg_rules,
    detach_public_ip,
    retrieve_vnc_path,
    retrieve_vnc_url,
    set_sg_rules,
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
        "port_range_max": 80,
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

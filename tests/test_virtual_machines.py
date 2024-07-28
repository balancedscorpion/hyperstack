from unittest.mock import MagicMock, patch

import pytest

from hyperstack.api.virtual_machines import (
    create_vm,
    delete_virtual_machine,
    get_floating_ip,
    hard_reboot_virtual_machine,
    hibernate_virtual_machine,
    list_virtual_machines,
    resize_virtual_machine,
    restore_hibernated_virtual_machine,
    retrieve_vm_details,
    start_virtual_machine,
    stop_virtual_machine,
    update_virtual_machine_labels,
)


@pytest.fixture
def mock_hyperstack():
    with patch('hyperstack.Hyperstack') as MockHyperstack:
        mock_instance = MockHyperstack.return_value
        mock_instance.post.return_value = {"status": "success", "data": {"id": "vm-123"}}
        mock_instance.get.return_value = {"status": "success", "data": {}}
        mock_instance.delete.return_value = {"status": "success", "data": {}}
        mock_instance.put.return_value = {"status": "success", "data": {}}
        mock_instance.environment = "test-env"
        mock_instance._check_environment_set = MagicMock()
        yield mock_instance


def test_create_vm_success(mock_hyperstack):
    result = create_vm(mock_hyperstack, name="test-vm", image_name="ubuntu-20.04", flavor_name="standard-1")
    expected_payload = {
        "name": "test-vm",
        "environment_name": "test-env",
        "image_name": "ubuntu-20.04",
        "create_bootable_volume": False,
        "flavor_name": "standard-1",
        "key_name": "development-key",
        "user_data": "",
        "assign_floating_ip": False,
        "count": 1,
    }
    mock_hyperstack.post.assert_called_once_with("core/virtual-machines", data=expected_payload)
    assert result == {"status": "success", "data": {"id": "vm-123"}}


def test_create_vm_with_optional_params(mock_hyperstack):
    result = create_vm(
        mock_hyperstack,
        name="test-vm",
        image_name="ubuntu-20.04",
        flavor_name="standard-1",
        key_name="custom-key",
        user_data="custom-data",
        create_bootable_volume=True,
        assign_floating_ip=True,
        count=2,
    )
    expected_payload = {
        "name": "test-vm",
        "environment_name": "test-env",
        "image_name": "ubuntu-20.04",
        "create_bootable_volume": True,
        "flavor_name": "standard-1",
        "key_name": "custom-key",
        "user_data": "custom-data",
        "assign_floating_ip": True,
        "count": 2,
    }
    mock_hyperstack.post.assert_called_once_with("core/virtual-machines", data=expected_payload)
    assert result == {"status": "success", "data": {"id": "vm-123"}}


def test_list_virtual_machines(mock_hyperstack):
    result = list_virtual_machines(mock_hyperstack)
    mock_hyperstack.get.assert_called_once_with("core/virtual-machines")
    assert result == {"status": "success", "data": {}}


def test_retrieve_vm_details(mock_hyperstack):
    result = retrieve_vm_details(mock_hyperstack, "vm-123")
    mock_hyperstack.get.assert_called_once_with("core/virtual-machines/vm-123")
    assert result == {"status": "success", "data": {}}


@pytest.mark.parametrize(
    "action, endpoint",
    [
        (start_virtual_machine, "start"),
        (stop_virtual_machine, "stop"),
        (hard_reboot_virtual_machine, "hard-reboot"),
        (hibernate_virtual_machine, "hibernate"),
        (restore_hibernated_virtual_machine, "hibernate-restore"),
    ],
)
def test_vm_actions(mock_hyperstack, action, endpoint):
    result = action(mock_hyperstack, "vm-123")
    mock_hyperstack.get.assert_called_once_with(f"core/virtual-machines/vm-123/{endpoint}")
    assert result == {"status": "success", "data": {}}


def test_delete_virtual_machine(mock_hyperstack):
    result = delete_virtual_machine(mock_hyperstack, "vm-123")
    mock_hyperstack.delete.assert_called_once_with("core/virtual-machines/vm-123")
    assert result == {"status": "success", "data": {}}


def test_resize_virtual_machine(mock_hyperstack):
    result = resize_virtual_machine(mock_hyperstack, "vm-123", "larger-flavor")
    expected_payload = {'flavor_name': 'larger-flavor'}
    mock_hyperstack.post.assert_called_once_with("core/virtual-machines/vm-123/resize", data=expected_payload)
    assert result == {"status": "success", "data": {"id": "vm-123"}}


def test_update_virtual_machine_labels(mock_hyperstack):
    labels = ["label1", "label2"]
    result = update_virtual_machine_labels(mock_hyperstack, "vm-123", labels)
    expected_payload = {'labels': labels}
    mock_hyperstack.put.assert_called_once_with("core/virtual-machines/vm-123/label", data=expected_payload)
    assert result == {"status": "success", "data": {}}


def test_get_floating_ip(mock_hyperstack):
    mock_response = {"instance": {"floating_ip": "123.45.67.89"}}
    mock_hyperstack.retrieve_vm_details.return_value = mock_response

    result = get_floating_ip(mock_hyperstack, "vm-123")

    assert result == "123.45.67.89"
    mock_hyperstack.retrieve_vm_details.assert_called_once_with("vm-123")


def test_environment_not_set(mock_hyperstack):
    mock_hyperstack.environment = None
    mock_hyperstack._check_environment_set.side_effect = EnvironmentError("Environment is not set")
    with pytest.raises(EnvironmentError, match="Environment is not set"):
        create_vm(mock_hyperstack, name="test-vm", image_name="ubuntu-20.04", flavor_name="standard-1")


@pytest.mark.parametrize(
    "function, args",
    [
        (create_vm, {"name": "test-vm", "image_name": "ubuntu-20.04", "flavor_name": "standard-1"}),
        (list_virtual_machines, {}),
        (retrieve_vm_details, {"vm_id": "vm-123"}),
        (start_virtual_machine, {"vm_id": "vm-123"}),
        (stop_virtual_machine, {"vm_id": "vm-123"}),
        (hard_reboot_virtual_machine, {"vm_id": "vm-123"}),
        (hibernate_virtual_machine, {"vm_id": "vm-123"}),
        (restore_hibernated_virtual_machine, {"vm_id": "vm-123"}),
        (delete_virtual_machine, {"vm_id": "vm-123"}),
        (resize_virtual_machine, {"vm_id": "vm-123", "flavor": "new-flavor"}),
        (update_virtual_machine_labels, {"vm_id": "vm-123", "labels": ["label1"]}),
        (get_floating_ip, {"vm_id": "vm-123"}),
    ],
)
def test_api_error_handling(mock_hyperstack, function, args):
    mock_hyperstack.post.side_effect = Exception("API Error")
    mock_hyperstack.get.side_effect = Exception("API Error")
    mock_hyperstack.delete.side_effect = Exception("API Error")
    mock_hyperstack.put.side_effect = Exception("API Error")
    mock_hyperstack.retrieve_vm_details.side_effect = Exception("API Error")

    with pytest.raises(Exception, match="API Error"):
        function(mock_hyperstack, **args)

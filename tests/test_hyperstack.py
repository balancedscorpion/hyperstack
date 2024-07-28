import pytest
from hyperstack.api.regions import Region
from unittest.mock import Mock
import time

# test_hyperstack.py
def test_create_environment_success(hyperstack_client, mock_hyperstack):
    # Print statements for detailed debugging
    print("Debug: Starting test_create_environment_success")

    # Create a unique environment name to avoid conflicts
    unique_env_name = "test-env-" + str(int(time.time()))

    # Mock response setup
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": "env-123", "name": unique_env_name}
    mock_response.raise_for_status = Mock()

    # Set up the mock _request method to return the mock response
    mock_hyperstack._request.return_value = mock_response

    # Call the method using the client
    response = hyperstack_client.create_environment(unique_env_name, "NORWAY-1")

    # Debugging outputs
    print(f"Debug: Response received: {response}")
    print(f"Debug: Mock _request called with: {mock_hyperstack._request.call_args}")

    # Assertions
    assert response.status_code == 201
    assert response.json()["name"] == unique_env_name
    mock_hyperstack._request.assert_called_once_with(
        "POST", 
        "core/environments", 
        json={"name": unique_env_name, "region": "NORWAY-1"}
    )

    print("Debug: test_create_environment_success completed successfully")

def test_create_environment_invalid_region(hyperstack_client):
    with pytest.raises(ValueError, match="Invalid region specified: INVALID-REGION"):
        hyperstack_client.create_environment("test-env", "INVALID-REGION")

def test_set_environment(hyperstack_client, mock_hyperstack):
    hyperstack_client.set_environment("test-env")
    assert mock_hyperstack.environment == "test-env"

def test_create_vm_success(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 201
    mock_hyperstack._request.return_value.json.return_value = {"id": "vm-123", "name": "test-vm"}

    response = hyperstack_client.create_vm("test-vm", "ubuntu-20.04", "t2.micro")

    assert response.status_code == 201
    assert response.json()["name"] == "test-vm"
    mock_hyperstack._request.assert_called_once_with(
        "POST",
        "core/virtual-machines",
        json={
            "name": "test-vm",
            "environment_name": "development",
            "image_name": "ubuntu-20.04",
            "create_bootable_volume": False,
            "flavor_name": "t2.micro",
            "key_name": "development-key",
            "user_data": "",
            "assign_floating_ip": False,
            "count": 1
        }
    )

def test_create_vm_no_environment(hyperstack_client, mock_hyperstack):
    mock_hyperstack.environment = None
    with pytest.raises(EnvironmentError, match="Environment is not set"):
        hyperstack_client.create_vm("test-vm", "ubuntu-20.04", "t2.micro")

@pytest.mark.parametrize("method_name, url_suffix", [
    ("start_virtual_machine", "start"),
    ("stop_virtual_machine", "stop"),
    ("hard_reboot_virtual_machine", "hard-reboot"),
    ("hibernate_virtual_machine", "hibernate"),
    ("restore_hibernated_virtual_machine", "hibernate-restore")
])
def test_vm_actions(hyperstack_client, mock_hyperstack, method_name, url_suffix):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = {"status": "success"}

    method = getattr(hyperstack_client, method_name)
    response = method("vm-123")

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_hyperstack._request.assert_called_once_with(
        "GET",
        f"core/virtual-machines/vm-123/{url_suffix}"
    )

def test_delete_virtual_machine(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 204

    response = hyperstack_client.delete_virtual_machine("vm-123")

    assert response.status_code == 204
    mock_hyperstack._request.assert_called_once_with(
        "DELETE",
        "core/virtual-machines/vm-123"
    )

@pytest.mark.parametrize("method_name, url_suffix", [
    ("attach_public_ip", "attach-floatingip"),
    ("detach_public_ip", "detach-floatingip")
])
def test_public_ip_actions(hyperstack_client, mock_hyperstack, method_name, url_suffix):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = {"status": "success"}

    method = getattr(hyperstack_client, method_name)
    response = method("vm-123")

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_hyperstack._request.assert_called_once_with(
        "POST",
        f"core/virtual-machines/vm-123/{url_suffix}"
    )

def test_list_virtual_machines(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = [{"id": "vm-123", "name": "test-vm"}]

    response = hyperstack_client.list_virtual_machines()

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "test-vm"
    mock_hyperstack._request.assert_called_once_with(
        "GET",
        "core/virtual-machines"
    )

def test_retrieve_vm_details(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = {"id": "vm-123", "name": "test-vm"}

    response = hyperstack_client.retrieve_vm_details("vm-123")

    assert response.json()["id"] == "vm-123"
    mock_hyperstack._request.assert_called_once_with(
        "GET",
        "core/virtual-machines/vm-123"
    )

def test_get_floating_ip(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = {"instance": {"floating_ip": "1.2.3.4"}}

    floating_ip = hyperstack_client.get_floating_ip("vm-123")

    assert floating_ip == "1.2.3.4"
    mock_hyperstack._request.assert_called_once_with(
        "GET",
        "core/virtual-machines/vm-123"
    )

def test_set_sg_rules(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = {"status": "success"}

    response = hyperstack_client.set_sg_rules("vm-123", port_range_min=80, port_range_max=80)

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_hyperstack._request.assert_called_once_with(
        "POST",
        "core/virtual-machines/vm-123/sg-rules",
        json={
            "remote_ip_prefix": "0.0.0.0/0",
            "direction": "ingress",
            "ethertype": "IPv4",
            "protocol": "tcp",
            "port_range_min": 80,
            "port_range_max": 80
        }
    )

def test_create_volume(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 201
    mock_hyperstack._request.return_value.json.return_value = {"id": "vol-123", "name": "test-volume"}

    response = hyperstack_client.create_volume("test-volume", "SSD", size=100)

    assert response.status_code == 201
    assert response.json()["name"] == "test-volume"
    mock_hyperstack._request.assert_called_once_with(
        "POST",
        "core/volumes",
        json={
            "name": "test-volume",
            "environment_name": "development",
            "volume_type": "SSD",
            "size": 100
        }
    )

def test_list_volumes(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = [{"id": "vol-123", "name": "test-volume"}]

    response = hyperstack_client.list_volumes()

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "test-volume"
    mock_hyperstack._request.assert_called_once_with(
        "GET",
        "core/volumes"
    )

def test_list_volume_types(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = [{"name": "SSD", "description": "Solid State Drive"}]

    response = hyperstack_client.list_volume_types()

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "SSD"
    mock_hyperstack._request.assert_called_once_with(
        "GET",
        "core/volume-types"
    )

def test_create_profile(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 201
    mock_hyperstack._request.return_value.json.return_value = {"id": "profile-123", "name": "test-profile"}

    response = hyperstack_client.create_profile(
        "test-profile", "development", "ubuntu-20.04", "t2.micro", "test-key", 1
    )

    assert response.status_code == 201
    assert response.json()["name"] == "test-profile"
    mock_hyperstack._request.assert_called_once_with(
        "POST",
        "core/profiles",
        json={
            "name": "test-profile",
            "data": {
                "environment_name": "development",
                "image_name": "ubuntu-20.04",
                "flavor_name": "t2.micro",
                "key_name": "test-key",
                "count": 1,
                "assign_floating_ip": "false",
                "create_bootable_volume": "false",
                "user_data": "",
                "callback_url": ""
            }
        }
    )

def test_list_profiles(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = [{"id": "profile-123", "name": "test-profile"}]

    response = hyperstack_client.list_profiles()

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "test-profile"
    mock_hyperstack._request.assert_called_once_with(
        "GET",
        "core/profiles"
    )

def test_retrieve_profile(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = {"id": "profile-123", "name": "test-profile"}

    response = hyperstack_client.retrieve_profile("profile-123")

    assert response.status_code == 200
    assert response.json()["name"] == "test-profile"
    mock_hyperstack._request.assert_called_once_with(
        "GET",
        "core/profiles/profile-123"
    )

def test_delete_profile(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 204

    response = hyperstack_client.delete_profile("profile-123")

    assert response.status_code == 204
    mock_hyperstack._request.assert_called_once_with(
        "DELETE",
        "core/profiles/profile-123"
    )

def test_list_regions(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = [{"name": "NORWAY-1"}, {"name": "CANADA-1"}]

    response = hyperstack_client.list_regions()

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "NORWAY-1"
    mock_hyperstack._request.assert_called_once_with(
        "GET",
        "core/regions",
        params={}
    )

@pytest.mark.parametrize("region", [None, Region.NORWAY_1])
def test_list_flavors(hyperstack_client, mock_hyperstack, region):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = [{"name": "t2.micro"}, {"name": "t2.small"}]

    response = hyperstack_client.list_flavors(region)

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "t2.micro"
    
    expected_params = {"region": region.value} if region else {}
    mock_hyperstack._request.assert_called_once_with(
        "GET",
        "core/flavors",
        params=expected_params
    )

def test_list_flavors_invalid_region(hyperstack_client):
    with pytest.raises(ValueError, match="Invalid region specified"):
        hyperstack_client.list_flavors("INVALID-REGION")

@pytest.mark.parametrize("region", [None, Region.NORWAY_1])
def test_list_images(hyperstack_client, mock_hyperstack, region):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = [{"name": "ubuntu-20.04"}, {"name": "centos-8"}]

    response = hyperstack_client.list_images(region)

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "ubuntu-20.04"
    
    expected_params = {"region": region.value} if region else {}
    mock_hyperstack._request.assert_called_once_with(
        "GET",
        "core/images",
        params=expected_params
    )

def test_list_images_invalid_region(hyperstack_client):
    with pytest.raises(ValueError, match="Invalid region specified"):
        hyperstack_client.list_images("INVALID-REGION")

def test_retrieve_gpu_stock(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = {
        "stocks": [
            {
                "region": "NORWAY-1",
                "models": [{"available": "100+", "model": "A100"}]
            }
        ]
    }

    response = hyperstack_client.retrieve_gpu_stock()

    assert response.status_code == 200
    assert "stocks" in response.json()
    assert response.json()["stocks"][0]["region"] == "NORWAY-1"
    mock_hyperstack._request.assert_called_once_with(
        "GET",
        "core/stocks"
    )

def test_create_profile_name_too_long(hyperstack_client):
    with pytest.raises(ValueError, match="Profile name must not exceed 50 characters"):
        hyperstack_client.create_profile("a" * 51, "development", "ubuntu-20.04", "t2.micro", "test-key", 1)

def test_create_profile_description_too_long(hyperstack_client):
    with pytest.raises(ValueError, match="Profile description must not exceed 150 characters"):
        hyperstack_client.create_profile("test-profile", "development", "ubuntu-20.04", "t2.micro", "test-key", 1, description="a" * 151)

def test_create_profile_invalid_count(hyperstack_client):
    with pytest.raises(ValueError, match="'count' must be an integer"):
        hyperstack_client.create_profile("test-profile", "development", "ubuntu-20.04", "t2.micro", "test-key", "1")

def test_set_sg_rules_all_parameters(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = {"status": "success"}

    response = hyperstack_client.set_sg_rules(
        "vm-123",
        remote_ip_prefix="192.168.1.0/24",
        direction="egress",
        ethertype="IPv6",
        protocol="udp",
        port_range_min=1000,
        port_range_max=2000
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_hyperstack._request.assert_called_once_with(
        "POST",
        "core/virtual-machines/vm-123/sg-rules",
        json={
            "remote_ip_prefix": "192.168.1.0/24",
            "direction": "egress",
            "ethertype": "IPv6",
            "protocol": "udp",
            "port_range_min": 1000,
            "port_range_max": 2000
        }
    )

def test_create_volume_with_optional_parameters(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 201
    mock_hyperstack._request.return_value.json.return_value = {"id": "vol-123", "name": "test-volume"}

    response = hyperstack_client.create_volume(
        "test-volume",
        "SSD",
        size=100,
        image_id="img-123",
        description="Test volume description",
        callback_url="https://example.com/callback"
    )

    assert response.status_code == 201
    assert response.json()["name"] == "test-volume"
    mock_hyperstack._request.assert_called_once_with(
        "POST",
        "core/volumes",
        json={
            "name": "test-volume",
            "environment_name": "development",
            "volume_type": "SSD",
            "size": 100,
            "image_id": "img-123",
            "description": "Test volume description",
            "callback_url": "https://example.com/callback"
        }
    )

def test_list_regions_with_specific_region(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = [{"name": "NORWAY-1"}]

    response = hyperstack_client.list_regions(Region.NORWAY_1)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "NORWAY-1"
    mock_hyperstack._request.assert_called_once_with(
        "GET",
        "core/regions",
        params={"region": "NORWAY-1"}
    )

def test_get_region_enum_valid():
    assert Region.get_region_enum("NORWAY-1") == Region.NORWAY_1

def test_get_region_enum_invalid():
    with pytest.raises(ValueError, match="Invalid region string"):
        Region.get_region_enum("INVALID-REGION")

def test_create_vm_environment_not_set(hyperstack_client, mock_hyperstack):
    mock_hyperstack.environment = None
    with pytest.raises(EnvironmentError, match="Environment is not set"):
        hyperstack_client.create_vm("test-vm", "ubuntu-20.04", "t2.micro")

def test_invalid_api_key(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.side_effect = Exception("Invalid API key")
    with pytest.raises(Exception, match="Invalid API key"):
        hyperstack_client.list_virtual_machines()

def test_network_error(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.side_effect = Exception("Network error")
    with pytest.raises(Exception, match="Network error"):
        hyperstack_client.list_virtual_machines()

def test_unexpected_server_error(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 500
    mock_hyperstack._request.return_value.json.return_value = {"error": "Unexpected server error"}
    with pytest.raises(Exception):
        hyperstack_client.list_virtual_machines()

@pytest.mark.parametrize("http_method", ["GET", "POST", "PUT", "DELETE"])
def test_successful_api_call(hyperstack_client, mock_hyperstack, http_method):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = {"status": "success"}

    response = hyperstack_client._hyperstack._request(http_method, "test/endpoint")

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_hyperstack._request.assert_called_once_with(http_method, "test/endpoint")

def test_api_rate_limiting(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.side_effect = [
        Exception("Rate limit exceeded"),
        Mock(status_code=200, json=lambda: {"status": "success"})
    ]
    
    response = hyperstack_client.list_virtual_machines()
    
    assert response.json()["status"] == "success"
    assert mock_hyperstack._request.call_count == 2

def test_list_virtual_machines_pagination(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.side_effect = [
        Mock(status_code=200, json=lambda: {"data": [{"id": "vm-1"}], "next_page": "page2"}),
        Mock(status_code=200, json=lambda: {"data": [{"id": "vm-2"}], "next_page": None})
    ]

    response = hyperstack_client.list_virtual_machines()

    assert len(response) == 2
    assert mock_hyperstack._request.call_count == 2

def test_create_vm_with_boolean_parameters(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 201
    mock_hyperstack._request.return_value.json.return_value = {"id": "vm-123", "name": "test-vm"}

    response = hyperstack_client.create_vm("test-vm", "ubuntu-20.04", "t2.micro", assign_floating_ip=True, create_bootable_volume=True)

    assert response.status_code == 201
    mock_hyperstack._request.assert_called_once_with(
        "POST",
        "core/virtual-machines",
        json={
            "name": "test-vm",
            "environment_name": "development",
            "image_name": "ubuntu-20.04",
            "create_bootable_volume": True,
            "flavor_name": "t2.micro",
            "key_name": "development-key",
            "user_data": "",
            "assign_floating_ip": True,
            "count": 1
        }
    )

def test_create_environment_with_region_enum(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 201
    mock_hyperstack._request.return_value.json.return_value = {"id": "env-123", "name": "test-env"}

    response = hyperstack_client.create_environment("test-env", Region.NORWAY_1)

    assert response.status_code == 201
    mock_hyperstack._request.assert_called_once_with(
        "POST",
        "core/environments",
        json={"name": "test-env", "region": "NORWAY-1"}
    )

def test_update_environment(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = {"id": "env-123", "name": "updated-env"}

    response = hyperstack_client.update_environment("env-123", name="updated-env")

    assert response.status_code == 200
    assert response.json()["name"] == "updated-env"
    mock_hyperstack._request.assert_called_once_with(
        "PUT",
        "core/environments/env-123",
        json={"name": "updated-env"}
    )

def test_resize_virtual_machine(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = {"status": "success"}

    response = hyperstack_client.resize_virtual_machine("vm-123", "t2.large")

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_hyperstack._request.assert_called_once_with(
        "POST",
        "core/virtual-machines/vm-123/resize",
        json={"flavor_name": "t2.large"}
    )

def test_update_virtual_machine_labels(hyperstack_client, mock_hyperstack):
    mock_hyperstack._request.return_value.status_code = 200
    mock_hyperstack._request.return_value.json.return_value = {"status": "success"}

    response = hyperstack_client.update_virtual_machine_labels("vm-123", ["label1", "label2"])

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_hyperstack._request.assert_called_once_with(
        "PUT",
        "core/virtual-machines/vm-123/label",
        json={"labels": ["label1", "label2"]}
    )

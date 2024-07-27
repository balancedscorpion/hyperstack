import pytest
from hyperstack import hyperstack
from hyperstack.api import environments, virtual_machines, volumes, network, profiles, regions, flavors, images, stock
from unittest.mock import patch
from hyperstack.api.regions import Region, get_region_enum

@pytest.fixture
def mock_hyperstack_request():
    with patch('hyperstack.client.Hyperstack._request') as mock_request:
        yield mock_request

def test_create_environment_success(mock_hyperstack_request):
    mock_hyperstack_request.return_value.status_code = 201
    mock_hyperstack_request.return_value.json.return_value = {"id": "env-123", "name": "test-env"}

    response = environments.create_environment("test-env", "NORWAY-1")

    assert response.status_code == 201
    assert response.json()["name"] == "test-env"
    mock_hyperstack_request.assert_called_once_with(
        "POST",
        "core/environments",
        json={"name": "test-env", "region": "NORWAY-1"}
    )

def test_create_environment_invalid_region():
    with pytest.raises(ValueError, match="Invalid region specified: INVALID-REGION"):
        environments.create_environment("test-env", "INVALID-REGION")

def test_set_environment():
    hyperstack.set_environment("test-env")
    assert hyperstack.environment == "test-env"

def test_create_vm_success(mock_hyperstack_request):
    hyperstack.set_environment("test-env")
    mock_hyperstack_request.return_value.status_code = 201
    mock_hyperstack_request.return_value.json.return_value = {"id": "vm-123", "name": "test-vm"}

    response = virtual_machines.create_vm("test-vm", "ubuntu-20.04", "t2.micro")

    assert response.status_code == 201
    assert response.json()["name"] == "test-vm"
    mock_hyperstack_request.assert_called_once_with(
        "POST",
        "core/virtual-machines",
        json={
            "name": "test-vm",
            "environment_name": "test-env",
            "image_name": "ubuntu-20.04",
            "create_bootable_volume": False,
            "flavor_name": "t2.micro",
            "key_name": "development-key",
            "user_data": "",
            "assign_floating_ip": False,
            "count": 1
        }
    )

def test_create_vm_no_environment():
    hyperstack.environment = None
    with pytest.raises(EnvironmentError, match="Environment is not set"):
        virtual_machines.create_vm("test-vm", "ubuntu-20.04", "t2.micro")

@pytest.mark.parametrize("method_name, url_suffix", [
    ("start_virtual_machine", "start"),
    ("stop_virtual_machine", "stop"),
    ("hard_reboot_virtual_machine", "hard-reboot"),
    ("hibernate_virtual_machine", "hibernate"),
    ("restore_hibernated_virtual_machine", "hibernate-restore")
])
def test_vm_actions(mock_hyperstack_request, method_name, url_suffix):
    hyperstack.set_environment("test-env")
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = {"status": "success"}

    method = getattr(virtual_machines, method_name)
    response = method("vm-123")

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_hyperstack_request.assert_called_once_with(
        "GET",
        f"core/virtual-machines/vm-123/{url_suffix}"
    )

def test_delete_virtual_machine(mock_hyperstack_request):
    hyperstack.set_environment("test-env")
    mock_hyperstack_request.return_value.status_code = 204

    response = virtual_machines.delete_virtual_machine("vm-123")

    assert response.status_code == 204
    mock_hyperstack_request.assert_called_once_with(
        "DELETE",
        "core/virtual-machines/vm-123"
    )

@pytest.mark.parametrize("method_name, url_suffix", [
    ("attach_public_ip", "attach-floatingip"),
    ("detach_public_ip", "detach-floatingip")
])
def test_public_ip_actions(mock_hyperstack_request, method_name, url_suffix):
    hyperstack.set_environment("test-env")
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = {"status": "success"}

    method = getattr(network, method_name)
    response = method("vm-123")

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_hyperstack_request.assert_called_once_with(
        "POST",
        f"core/virtual-machines/vm-123/{url_suffix}"
    )
    
def test_list_virtual_machines(mock_hyperstack_request):
    hyperstack.set_environment("test-env")
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = [{"id": "vm-123", "name": "test-vm"}]

    response = virtual_machines.list_virtual_machines()

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "test-vm"
    mock_hyperstack_request.assert_called_once_with(
        "GET",
        "core/virtual-machines"
    )

def test_retrieve_vm_details(mock_hyperstack_request):
    hyperstack.set_environment("test-env")
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = {"id": "vm-123", "name": "test-vm"}

    response = virtual_machines.retrieve_vm_details("vm-123")

    assert response.json()["id"] == "vm-123"
    mock_hyperstack_request.assert_called_once_with(
        "GET",
        "core/virtual-machines/vm-123"
    )


def test_get_floating_ip(mock_hyperstack_request):
    hyperstack.set_environment("test-env")
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = {"instance": {"floating_ip": "1.2.3.4"}}

    floating_ip = virtual_machines.get_floating_ip("vm-123")

    assert floating_ip == "1.2.3.4"
    mock_hyperstack_request.assert_called_once_with(
        "GET",
        "core/virtual-machines/vm-123"
    )

def test_set_sg_rules(mock_hyperstack_request):
    hyperstack.set_environment("test-env")
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = {"status": "success"}

    response = network.set_sg_rules("vm-123", port_range_min=80, port_range_max=80)

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_hyperstack_request.assert_called_once_with(
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

def test_create_volume(mock_hyperstack_request):
    hyperstack.set_environment("test-env")
    mock_hyperstack_request.return_value.status_code = 201
    mock_hyperstack_request.return_value.json.return_value = {"id": "vol-123", "name": "test-volume"}

    response = volumes.create_volume("test-volume", "SSD", size=100)

    assert response.status_code == 201
    assert response.json()["name"] == "test-volume"
    mock_hyperstack_request.assert_called_once_with(
        "POST",
        "core/volumes",
        json={
            "name": "test-volume",
            "environment_name": "test-env",
            "volume_type": "SSD",
            "size": 100
        }
    )

def test_list_volumes(mock_hyperstack_request):
    hyperstack.set_environment("test-env")
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = [{"id": "vol-123", "name": "test-volume"}]

    response = volumes.list_volumes()

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "test-volume"
    mock_hyperstack_request.assert_called_once_with(
        "GET",
        "core/volumes"
    )

def test_list_volume_types(mock_hyperstack_request):
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = [{"name": "SSD", "description": "Solid State Drive"}]

    response = volumes.list_volume_types()

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "SSD"
    mock_hyperstack_request.assert_called_once_with(
        "GET",
        "core/volume-types"
    )

def test_create_profile(mock_hyperstack_request):
    mock_hyperstack_request.return_value.status_code = 201
    mock_hyperstack_request.return_value.json.return_value = {"id": "profile-123", "name": "test-profile"}

    response = profiles.create_profile(
        "test-profile", "test-env", "ubuntu-20.04", "t2.micro", "test-key", 1
    )

    assert response.status_code == 201
    assert response.json()["name"] == "test-profile"
    mock_hyperstack_request.assert_called_once_with(
        "POST",
        "core/profiles",
        json={
            "name": "test-profile",
            "data": {
                "environment_name": "test-env",
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

def test_list_profiles(mock_hyperstack_request):
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = [{"id": "profile-123", "name": "test-profile"}]

    response = profiles.list_profiles()

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "test-profile"
    mock_hyperstack_request.assert_called_once_with(
        "GET",
        "core/profiles"
    )

def test_retrieve_profile(mock_hyperstack_request):
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = {"id": "profile-123", "name": "test-profile"}

    response = profiles.retrieve_profile("profile-123")

    assert response.status_code == 200
    assert response.json()["name"] == "test-profile"
    mock_hyperstack_request.assert_called_once_with(
        "GET",
        "core/profiles/profile-123"
    )

def test_delete_profile(mock_hyperstack_request):
    mock_hyperstack_request.return_value.status_code = 204

    response = profiles.delete_profile("profile-123")

    assert response.status_code == 204
    mock_hyperstack_request.assert_called_once_with(
        "DELETE",
        "core/profiles/profile-123"
    )

def test_list_regions(mock_hyperstack_request):
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = [{"name": "NORWAY-1"}, {"name": "CANADA-1"}]

    response = regions.list_regions()

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "NORWAY-1"
    mock_hyperstack_request.assert_called_once_with(
        "GET",
        "core/regions",
        params={}
    )

@pytest.mark.parametrize("region", [None, Region.NORWAY_1])
def test_list_flavors(mock_hyperstack_request, region):
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = [{"name": "t2.micro"}, {"name": "t2.small"}]

    response = flavors.list_flavors(region)

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "t2.micro"
    
    expected_params = {"region": region.value} if region else {}
    mock_hyperstack_request.assert_called_once_with(
        "GET",
        "core/flavors",
        params=expected_params
    )

def test_list_flavors_invalid_region():
    with pytest.raises(ValueError, match="Invalid region specified"):
        flavors.list_flavors("INVALID-REGION")

@pytest.mark.parametrize("region", [None, Region.NORWAY_1])
def test_list_images(mock_hyperstack_request, region):
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = [{"name": "ubuntu-20.04"}, {"name": "centos-8"}]

    response = images.list_images(region)

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "ubuntu-20.04"
    
    expected_params = {"region": region.value} if region else {}
    mock_hyperstack_request.assert_called_once_with(
        "GET",
        "core/images",
        params=expected_params
    )

def test_list_images_invalid_region():
    with pytest.raises(ValueError, match="Invalid region specified"):
        images.list_images("INVALID-REGION")
def test_retrieve_gpu_stock(mock_hyperstack_request):
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = {"NORWAY-1": {"available": 10, "total": 20}}

    response = stock.retrieve_gpu_stock()

    assert response.status_code == 200
    assert "NORWAY-1" in response.json()
    assert response.json()["NORWAY-1"]["available"] == 10
    mock_hyperstack_request.assert_called_once_with(
        "GET",
        "core/stocks"
    )

# Additional tests to cover edge cases and error handling

def test_create_profile_name_too_long():
    with pytest.raises(ValueError, match="Profile name must not exceed 50 characters"):
        profiles.create_profile("a" * 51, "test-env", "ubuntu-20.04", "t2.micro", "test-key", 1)

def test_create_profile_description_too_long():
    with pytest.raises(ValueError, match="Profile description must not exceed 150 characters"):
        profiles.create_profile("test-profile", "test-env", "ubuntu-20.04", "t2.micro", "test-key", 1, description="a" * 151)

def test_create_profile_invalid_count():
    with pytest.raises(ValueError, match="'count' must be an integer"):
        profiles.create_profile("test-profile", "test-env", "ubuntu-20.04", "t2.micro", "test-key", "1")

def test_set_sg_rules_all_parameters(mock_hyperstack_request):
    hyperstack.set_environment("test-env")
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = {"status": "success"}

    response = network.set_sg_rules(
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
    mock_hyperstack_request.assert_called_once_with(
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

def test_create_volume_with_optional_parameters(mock_hyperstack_request):
    hyperstack.set_environment("test-env")
    mock_hyperstack_request.return_value.status_code = 201
    mock_hyperstack_request.return_value.json.return_value = {"id": "vol-123", "name": "test-volume"}

    response = volumes.create_volume(
        "test-volume",
        "SSD",
        size=100,
        image_id="img-123",
        description="Test volume description",
        callback_url="https://example.com/callback"
    )

    assert response.status_code == 201
    assert response.json()["name"] == "test-volume"
    mock_hyperstack_request.assert_called_once_with(
        "POST",
        "core/volumes",
        json={
            "name": "test-volume",
            "environment_name": "test-env",
            "volume_type": "SSD",
            "size": 100,
            "image_id": "img-123",
            "description": "Test volume description",
            "callback_url": "https://example.com/callback"
        }
    )

def test_list_regions_with_specific_region(mock_hyperstack_request):
    mock_hyperstack_request.return_value.status_code = 200
    mock_hyperstack_request.return_value.json.return_value = [{"name": "NORWAY-1"}]

    response = regions.list_regions(Region.NORWAY_1)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "NORWAY-1"
    mock_hyperstack_request.assert_called_once_with(
        "GET",
        "core/regions",
        params={"region": "NORWAY-1"}
    )

def test_get_region_enum_valid():
    assert regions.get_region_enum("NORWAY-1") == Region.NORWAY_1

def test_get_region_enum_invalid():
    with pytest.raises(ValueError, match="Invalid region string"):
        regions.get_region_enum("INVALID-REGION")

# Test for environment not set
def test_create_vm_environment_not_set():
    hyperstack.environment = None
    with pytest.raises(EnvironmentError, match="Environment is not set"):
        virtual_machines.create_vm("test-vm", "ubuntu-20.04", "t2.micro")

# Test for invalid API key
@patch('hyperstack.client.Hyperstack._request')
def test_invalid_api_key(mock_request):
    hyperstack.set_environment("test-env")  # Set environment before the test
    mock_request.side_effect = Exception("Invalid API key")
    with pytest.raises(Exception, match="Invalid API key"):
        virtual_machines.list_virtual_machines()

# Test for network error
@patch('hyperstack.client.Hyperstack._request')
def test_network_error(mock_request):
    hyperstack.set_environment("test-env")  # Set environment before the test
    mock_request.side_effect = Exception("Network error")
    with pytest.raises(Exception, match="Network error"):
        virtual_machines.list_virtual_machines()


# Test for unexpected server error
@patch('hyperstack.client.Hyperstack._request')
def test_unexpected_server_error(mock_request):
    hyperstack.set_environment("test-env")  # Set environment before the test
    mock_request.return_value.status_code = 500
    mock_request.return_value.json.return_value = {"error": "Unexpected server error"}
    response = virtual_machines.list_virtual_machines()
    assert response.status_code == 500
    assert response.json()["error"] == "Unexpected server error"
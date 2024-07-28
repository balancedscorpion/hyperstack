import pytest
from unittest.mock import patch, MagicMock
from hyperstack import Hyperstack

class MockHyperstack(Hyperstack):
    def __init__(self):
        self.api_key = "mock_api_key"
        self.base_url = "https://mock-api.example.com/v1/"
        self.headers = {
            "Content-Type": "application/json",
            "api_key": self.api_key
        }
        self.valid_regions = ["NORWAY-1", "CANADA-1"]
        self.environment = None

    def _request(self, method, endpoint, **kwargs):
        mock_response = MagicMock()
        mock_response.content = b'{"status": "success", "data": {}}'
        return mock_response

    def get(self, endpoint, **kwargs):
        return {"status": "success", "data": {}}

    def post(self, endpoint, data=None, **kwargs):
        return {"status": "success", "data": {}}

    def put(self, endpoint, data=None, **kwargs):
        return {"status": "success", "data": {}}

    def delete(self, endpoint, **kwargs):
        return {"status": "success", "data": {}}

# Mock all methods
for method_name in [
    'create_profile', 'list_profiles', 'retrieve_profile', 'delete_profile',
    'list_regions', 'get_region_enum',
    'create_environment', 'list_environments', 'get_environment', 'set_environment',
    'delete_environment', 'update_environment',
    'list_flavors', 'get_flavor_enum',
    'list_images', 'get_image_enum',
    'attach_public_ip', 'detach_public_ip', 'set_sg_rules', 'delete_sg_rules',
    'retrieve_vnc_path', 'retrieve_vnc_url',
    'retrieve_gpu_stock',
    'create_vm', 'list_virtual_machines', 'retrieve_vm_details', 'start_virtual_machine',
    'stop_virtual_machine', 'hard_reboot_virtual_machine', 'hibernate_virtual_machine',
    'restore_hibernated_virtual_machine', 'delete_virtual_machine', 'resize_virtual_machine',
    'update_virtual_machine_labels', 'get_floating_ip',
    'create_volume', 'list_volumes', 'list_volume_types', 'get_volume', 'delete_volume'
]:
    setattr(MockHyperstack, method_name, MagicMock(return_value={"status": "success", "data": {}}))

@pytest.fixture(autouse=True)
def mock_hyperstack():
    mock_instance = MockHyperstack()
    with patch('hyperstack.Hyperstack', return_value=mock_instance), \
         patch('hyperstack._hyperstack', mock_instance), \
         patch.multiple('hyperstack', 
                        create_profile=mock_instance.create_profile,
                        list_profiles=mock_instance.list_profiles,
                        # ... add all other methods here ...
                        delete_volume=mock_instance.delete_volume):
        yield mock_instance
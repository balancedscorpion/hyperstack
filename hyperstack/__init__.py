from .api.regions import Region
from .client import Hyperstack

# Singleton instance
_hyperstack = Hyperstack()

# Expose Region enum
Region = Region

# Expose methods at the module level
create_profile = _hyperstack.create_profile
list_profiles = _hyperstack.list_profiles
retrieve_profile = _hyperstack.retrieve_profile
delete_profile = _hyperstack.delete_profile

# Expose region methods
list_regions = _hyperstack.list_regions
get_region_enum = _hyperstack.get_region_enum

# Expose environment methods
create_environment = _hyperstack.create_environment
list_environments = _hyperstack.list_environments
get_environment = _hyperstack.get_environment
set_environment = _hyperstack.set_environment
delete_environment = _hyperstack.delete_environment
update_environment = _hyperstack.update_environment

# Expose flavor methods
list_flavors = _hyperstack.list_flavors
get_flavor_enum = _hyperstack.get_flavor_enum

# Expose image methods
list_images = _hyperstack.list_images
get_image_enum = _hyperstack.get_image_enum

# Expose network methods
attach_public_ip = _hyperstack.attach_public_ip
detach_public_ip = _hyperstack.detach_public_ip
set_sg_rules = _hyperstack.set_sg_rules
delete_sg_rules = _hyperstack.delete_sg_rules
retrieve_vnc_path = _hyperstack.retrieve_vnc_path
retrieve_vnc_url = _hyperstack.retrieve_vnc_url

# Expose stock methods
retrieve_gpu_stock = _hyperstack.retrieve_gpu_stock

# Expose virtual machine methods
create_vm = _hyperstack.create_vm
list_virtual_machines = _hyperstack.list_virtual_machines
retrieve_vm_details = _hyperstack.retrieve_vm_details
start_virtual_machine = _hyperstack.start_virtual_machine
stop_virtual_machine = _hyperstack.stop_virtual_machine
hard_reboot_virtual_machine = _hyperstack.hard_reboot_virtual_machine
hibernate_virtual_machine = _hyperstack.hibernate_virtual_machine
restore_hibernated_virtual_machine = _hyperstack.restore_hibernated_virtual_machine
delete_virtual_machine = _hyperstack.delete_virtual_machine
resize_virtual_machine = _hyperstack.resize_virtual_machine
update_virtual_machine_labels = _hyperstack.update_virtual_machine_labels
get_floating_ip = _hyperstack.get_floating_ip
wait_for_vm_active = _hyperstack.wait_for_vm_active

# Expose volume methods
create_volume = _hyperstack.create_volume
list_volumes = _hyperstack.list_volumes
list_volume_types = _hyperstack.list_volume_types
get_volume = _hyperstack.get_volume
delete_volume = _hyperstack.delete_volume

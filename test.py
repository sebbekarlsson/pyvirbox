from pyvirbox.utils import create_vm, clone_vm, remove_vm, list_vms, start_vm, stop_vm, execute_vm, list_sessions, list_os_types, vm_info


vmname = 'TESTBOX'

#print(create_vm(vmname, 'Debian_64', '/home/ianertson/isos/debian-8.3.0-amd64-netinst.iso', 1024, 8000))
#print(clone_vm('deb_1024_8000', vmname))
#print(start_vm(vmname))
#print(vm_info(vmname))
#print(execute_vm(vmname, '/sbin/ifconfig', 'root', 'debian'))
print(stop_vm(vmname))
#print(remove_vm(vmname))
#print(list_vms())

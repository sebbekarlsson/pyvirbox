import subprocess
import time


def list_os_types():
    output = subprocess.Popen(
            'VBoxManage list ostypes',
            shell=True, stdout=subprocess.PIPE
            ).stdout.read().decode('UTF-8')

    return output


def vm_info(name):
    output = subprocess.Popen(
            'VBoxManage showvminfo "{name}"'.format(name=name),
            shell=True, stdout=subprocess.PIPE
            ).stdout.read().decode('UTF-8')

    return output


def list_sessions(name):
    output = subprocess.Popen(
            'VBoxManage guestcontrol {name} list sessions'.\
                    format(
                        name=name
                        ),
            shell=True, stdout=subprocess.PIPE
            ).stdout.read().decode('UTF-8')

    return output


def list_vms():
    output = subprocess.Popen(
            'VBoxManage list vms',
            shell=True, stdout=subprocess.PIPE
            ).stdout.read().decode('UTF-8')

    return output


def clone_vm(name, new_name):
    output = subprocess.Popen(
            'VBoxManage clonevm "{name}" --name {new_name} --register'.\
            format(
                name=name,
                new_name=new_name
                ),
            shell=True, stdout=subprocess.PIPE
            ).stdout.read().decode('UTF-8')

    return output


def remove_vm(name):
    output = subprocess.Popen(
            'VBoxManage unregistervm "{name}" --delete'.\
            format(
                name=name
                ),
            shell=True, stdout=subprocess.PIPE
            ).stdout.read().decode('UTF-8')

    return output


def create_vm(name, os, iso, ram, size, net_device='enp3s0'):
    output = subprocess.Popen(
            '''
            VBoxManage createvm --name {name} --ostype "{os}" --register
            VBoxManage createhd --filename {name}.vdi --size {size}
            VBoxManage storagectl {name} --name "SATA Controller" --add sata --controller IntelAHCI
            VBoxManage storageattach {name} --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium {name}.vdi
            VBoxManage storagectl {name} --name "IDE Controller" --add ide
            VBoxManage storageattach {name} --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium {iso}
            VBoxManage modifyvm {name} --ioapic on
            VBoxManage modifyvm {name} --boot1 dvd --boot2 disk --boot3 none --boot4 none
            VBoxManage modifyvm {name} --memory {ram} --vram 128
            VBoxManage modifyvm {name} --nic1 bridged --bridgeadapter1 {net_device}
            #VBoxManage storageattach {name} --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium none
            '''.\
                    format(
                        name=name,
                        os=os,
                        iso=iso,
                        ram=ram,
                        size=size,
                        net_device=net_device
                        ),
            shell=True, stdout=subprocess.PIPE).stdout.read().decode('UTF-8')

    return output


def start_vm(name):
    output = subprocess.Popen(
            'VBoxManage startvm {name} --type headless'.\
                    format(
                        name=name
                        ),
            shell=True, stdout=subprocess.PIPE
            ).stdout.read().decode('UTF-8')

    return output


def stop_vm(name):
    output = subprocess.Popen(
            'VBoxManage controlvm {name} savestate'.\
                    format(
                        name=name
                        ),
            shell=True, stdout=subprocess.PIPE
            ).stdout.read().decode('UTF-8')

    return output


def execute_vm(name, command, username, password):
    process = subprocess.Popen(
            'VBoxManage guestcontrol {name} run --exe {command} --username {username} --password {password} --wait-stdout --wait-stderr'.\
                    format(
                        name=name,
                        command=command,
                        username=username,
                        password=password
                        ),
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
    process.wait()
    output = process.stdout.read().decode('UTF-8')
    error = process.stderr.read().decode('UTF-8')

    error_list = (
            'not ready',
            'not in started state',
            'Error starting guest session',
            'not running'
            )
    while any(err in error for err in error_list):
        time.sleep(3)
        output, error = execute_vm(name, command, username, password)

    return output, error

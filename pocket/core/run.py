import cgroups
import os
import unshare
from pocket.utils import console
from pocket.utils import fs


def run(container_id, commands, environment=None):
    """
    run commands in a container that has already been created
    :param container_id: container id
    :param commands: list of commands to execute
    :param environment: dictionary of key-value pairs
    """
    if environment is None:
        environment = {}

    if not os.path.exists(fs.get_path_to_container(container_id)):
        console.error("Container does not exist")
        return

    pid = os.fork()
    if pid == 0:
        # container process
        console.log('Pocket starting with process-id: %d' % os.getpid())

        cgroups.Cgroup(container_id).add(os.getpid())
        os.chroot(fs.get_path_to_container(container_id))
        os.chdir('/')

        unshare.unshare(unshare.CLONE_NEWUTS | unshare.CLONE_NEWNS | unshare.CLONE_NEWPID)

        pid2 = os.fork()
        if pid2 == 0:
            fs.mount("/proc", "/proc", "proc")
            os.system(f'/bin/hostname {container_id}')
            # execute the commands
            for command in commands:
                console.log(f'{container_id}: executing - {command}')
                os.execve(command.split(" ")[0], command.split(" "), environment)
        else:
            os.waitpid(pid2, 0)
    else:
        _, status = os.waitpid(pid, 0)
        fs.unmount(os.path.join(fs.get_path_to_container(container_id), "proc"))
        console.log(f'Pocket pid: {pid} exited with status {status}')

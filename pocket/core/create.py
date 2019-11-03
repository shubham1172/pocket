import cgroups
import os
import unshare
import uuid
from pocket.config.config import Config
from pocket.utils import console
from pocket.utils import fs


def create(config_path):
    """
    create a container from config
    :param config_path: path to config yaml
    """
    config = Config(config_path)
    base_image = config.args['image']
    container_id = str(uuid.uuid4())

    console.log('creating a new container (%s)' % container_id)

    # setup the cgroup
    cg = cgroups.Cgroup(container_id)
    if 'limit' in config.args.keys():
        if 'cpu' in config.args['limit'].keys():
            cg.set_cpu_limit(config.args['limit']['cpu'])
        if 'mem' in config.args['limit'].keys():
            cg.set_memory_limit(config.args['limit']['mem'])

    console.log('Spinning up a filesystem...')
    fs.setup_fs(base_image, container_id)

    for item in config.args.get('copy', []):
        console.log(f'{container_id}: copying {item["src"]} to {item["dest"]}')
        fs.copy_to_container(item['src'], item['dest'], container_id)


    pid = os.fork()
    if pid == 0:
        # container process
        console.log('Pocket starting with process-id: %d' % os.getpid())
        cg.add(os.getpid())

        os.chroot(fs.get_path_to_container(container_id))
        os.chdir('/')

        unshare.unshare(unshare.CLONE_NEWUTS | unshare.CLONE_NEWNS | unshare.CLONE_NEWPID)

        pid2 = os.fork()
        if pid2 == 0:
            fs.mount("/proc", "/proc", "proc")
            os.system(f'/bin/hostname {container_id}')
            # execute the commands
            for item in config.args.get('run', []):
                console.log(f'{container_id}: executing - {item}')
                os.execve(item.split(" ")[0], item.split(" "), config.args.get('env', {}))
        else:
            os.waitpid(pid2, 0)
    else:
        _, status = os.waitpid(pid, 0)
        fs.unmount(os.path.join(fs.get_path_to_container(container_id), "proc"))
        console.log(f'Pocket pid: {pid} exited with status {status}')

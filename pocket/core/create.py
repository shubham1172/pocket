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

    pid = os.fork()
    if pid == 0:
        # container process
        fs.setup_fs(base_image, container_id)
        unshare.unshare(unshare.CLONE_NEWUTS)
        os.system(f'hostname {container_id}')
        os.chroot(fs.get_path_to_container(container_id))
        os.chdir('/')
    else:
        _, status = os.waitpid(pid, 0)
        console.log(f'Pocket pid: {pid} exited with status {status}')
        fs.clean_fs(container_id)

import cgroups
import uuid
from pocket.config.config import Config
from pocket.core import run as pocket_run
from pocket.utils import console
from pocket.utils import defaults
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

    # file system tasks
    console.log('Spinning up a filesystem...')
    fs.setup_fs(base_image, container_id)

    for item in config.args.get('copy', []):
        console.log(f'{container_id}: copying {item["src"]} to {item["dest"]}')
        fs.copy_to_container(item['src'], item['dest'], container_id)

    # run commands if applicable
    commands = config.args.get('run', [])
    environment = dict(defaults.ENVIRONMENT, **config.args.get('env', {}))

    if len(commands) > 0:
        pocket_run.run(container_id, commands, environment)

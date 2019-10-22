from pocket.utils import fs
import datetime
import os
import time


def list_(quiet: bool):
    """
    list all containers
    :param quiet: print only id
    """
    containers_path = fs.get_path_to_containers()
    if not quiet:
        print("Container ID\tCreated At")
    for container_id in os.listdir(containers_path):
        stat = os.stat(os.path.join(containers_path, container_id))
        created_at = datetime.datetime.strptime(
            time.ctime(stat.st_ctime), "%a %b %d %H:%M:%S %Y").strftime("%d/%m/%Y %H:%M:%S")
        if quiet:
            print(f'{container_id}')
        else:
            print(f'{container_id}\t{created_at}')

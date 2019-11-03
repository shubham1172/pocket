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
        print("Container ID\tCreated At\tSize")
    for container_id in os.listdir(containers_path):
        container_path = fs.get_path_to_container(container_id)
        stat = os.stat(container_path)
        created_at = datetime.datetime.strptime(
            time.ctime(stat.st_ctime), "%a %b %d %H:%M:%S %Y").strftime("%d/%m/%Y %H:%M:%S")
        size = "%.2f MB" % (fs.get_size_kb(container_path) / 1024)
        if quiet:
            print(f'{container_id}')
        else:
            print(f'{container_id}\t{created_at}\t{size}')

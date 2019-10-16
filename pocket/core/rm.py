import cgroups
import os
from pocket.utils import fs


def rm(pid):
    """
    remove a pocket with pocket id
    :param pid: pocket id
    """
    cg = cgroups.Cgroup(pid)
    cg.delete()
    fs.clean_fs(pid)


def rm_all():
    """
    remove all pockets
    """
    containers_path = fs.get_path_to_containers()
    containers = os.listdir(containers_path)
    for pid in containers:
        rm(pid)
    return len(containers)

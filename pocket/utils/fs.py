import os
import shutil
import tarfile
from pocket.core.pull import Pull

BASE_PATH = os.path.join('/opt', 'pocket')


def get_path_to_images():
    return os.path.join(BASE_PATH, 'images')


def get_path_to_manifest(manifest_name):
    return os.path.join(get_path_to_images(), manifest_name)


def get_path_to_layers(manifest_name):
    return os.path.join(get_path_to_manifest(manifest_name), 'layers')


def get_path_to_manifest_file(manifest_name):
    return os.path.join(get_path_to_manifest(manifest_name), manifest_name+'.json')


def get_path_to_container(container_id):
    return os.path.join(BASE_PATH, 'containers', container_id)


def _extract(source, dest):
    for tar in os.listdir(source):
        with tarfile.open(os.path.join(source, tar), 'r') as layer_tarfile:
            layer_tarfile.extractall(dest)


def setup_fs(image, container_id):
    path_to_container = get_path_to_container(container_id)
    os.makedirs(path_to_container)
    if not os.path.isdir(get_path_to_manifest(image)):
        Pull(image).run()
    _extract(get_path_to_layers(image), path_to_container)
    # TODO: mount stuff
    pass


def clean_fs(container_id):
    path_to_container = get_path_to_container(container_id)
    shutil.rmtree(path_to_container)

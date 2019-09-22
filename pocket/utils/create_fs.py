import os
import tarfile
from pocket.utils import fs
from pocket.core.pull import Pull

def extract(source, destn):
    for tar in os.listdir(source):
        with tarfile.open(tar, 'r') as layer_tarfile:
            layer_tarfile.extractall(dest)

def setup_fs(image, container_id):
    path_to_container = fs.get_path_to_container(container_id)
    os.makedirs(path_to_container)
    if(!os.path.isdir(fs.get_path_to_manifest(image))):
        pull_image = Pull(image)
        pull_image.run()
    extract(fs.get_path_to_layers(image), path_to_container)

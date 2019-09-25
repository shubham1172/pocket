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


def _mount(src, dest=None, _type=None, options=None, flags=None):
    """
    Mount a file system
    :param src: source path
    :param dest: destination path (optional)
    :param _type: type of mount (optional)
    :param options: options for mount (optional)
    :param flags: flags for mount (optional)
    """
    options_string = "-o {}".format(options) if options else ""
    _type_string = "-t {}".format(_type) if _type else ""
    flags_string = flags if flags else ""
    dest_string = dest if dest else ""
    os.system('mount {} {} {} {} {}'.format(options_string, _type_string, flags_string, src, dest_string))


def _unmount(path):
    """
    Un-mount a file system
    :param path: path to un-mount
    """
    os.system(f'umount {path}')


def setup_fs(image, container_id):
    """
    Set up the file system
    - pull image if required
    - extract tars in the container directory
    - mount important directories
    :param image: name of the image:tag
    :param container_id:
    """
    path_to_container = get_path_to_container(container_id)
    os.makedirs(path_to_container)
    if not os.path.isdir(get_path_to_manifest(image)):
        Pull(image).run()
    _extract(get_path_to_layers(image), path_to_container)
    _mount('/proc', os.path.join(get_path_to_container(container_id), 'proc'), _type='proc')
    _mount('/sys', os.path.join(get_path_to_container(container_id), 'sys'), options='bind')
    _mount('/dev', os.path.join(get_path_to_container(container_id), 'dev'), options='bind')


def clean_fs(container_id):
    """
    Clean the file system
    - unmount mounted things
    - remove the container directory
    :param container_id:
    """
    path_to_container = get_path_to_container(container_id)
    _unmount(os.path.join(path_to_container, "proc"))
    _unmount(os.path.join(path_to_container, "sys"))
    _unmount(os.path.join(path_to_container, "dev"))
    shutil.rmtree(path_to_container)

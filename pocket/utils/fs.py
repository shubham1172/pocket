import os

BASE_PATH = os.path.join(os.environ['HOME'], '.pocket')


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

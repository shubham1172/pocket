import requests
import json
import os
from pocket.utils import console
from pocket.utils import fs

BASE_URL = 'https://registry-1.docker.io/v2'


class Pull:
    def __init__(self, image):
        self.image, self.tag = image.split(':')
        self.headers = {'Authorization': 'Bearer %s' % self.auth(self.image)}
        if not os.path.exists(fs.get_path_to_images()):
            os.makedirs(fs.get_path_to_images())

    def auth(self, image):
        token_request_url = 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/%s:pull' \
                            % image
        token_request_response = requests.get(token_request_url)
        token = token_request_response.json()['token']

        return token

    def get_manifest(self):
        console.log("Requesting manifest for %s..." % self.image)
        manifest_request_url = '%s/library/%s/manifests/%s' % (BASE_URL, self.image, self.tag)
        manifest_request_response = requests.get(manifest_request_url, headers=self.headers)
        manifest = manifest_request_response.json()
        console.ok("Manifest received!")

        return manifest

    def run(self):
        # get manifest
        manifest = self.get_manifest()

        # save manifest
        image_name = f'{self.image}:{self.tag}'

        if not os.path.exists(fs.get_path_to_manifest(image_name)):
            os.makedirs(fs.get_path_to_manifest(image_name))

        with open(fs.get_path_to_manifest_file(image_name), 'w') as manifest_file:
            manifest_file.write(json.dumps(manifest))

        # save layers
        if not os.path.exists(fs.get_path_to_layers(image_name)):
            os.makedirs(fs.get_path_to_layers(image_name))

        layers = [layer['blobSum'] for layer in manifest['fsLayers']]

        # get unique layers
        layers = set(layers)

        # fetching and extracting layers
        for layer in layers:
            console.log('Getting layer %s...' % layer)
            layer_request_url = '%s/library/%s/blobs/%s' % (BASE_URL, self.image, layer)
            tarfile_name = os.path.join(fs.get_path_to_layers(image_name), layer) + '.tar'
            layer_request_response = requests.get(layer_request_url, stream=True, headers=self.headers)
            with open(tarfile_name, 'wb') as layer_file:
                for chunk in layer_request_response.iter_content(1024):
                    layer_file.write(chunk)
        console.ok('All layers successfully received!')

        # set permissions
        os.system(f'chmod -R 755 {fs.get_path_to_manifest(image_name)}')

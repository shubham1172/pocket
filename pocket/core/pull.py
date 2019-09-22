import requests
import json
import os
import tarfile
from pocket.utils import console

BASE_URL = 'https://registry-1.docker.io/v2'
PATH_TO_IMAGES = os.path.join(os.environ['HOME'], '.pocket/images')

class Pull():

    def __init__ (self, arg, tag='latest'):
            self.image = arg
            self.tag = tag
            self.headers = {'Authorization': 'Bearer %s' % self.auth(self.image)}
            if not os.path.exists(PATH_TO_IMAGES):
                os.makedirs(PATH_TO_IMAGES)

    def auth(self, image):
        token_request_url = 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/%s:pull' % (image)
        token_request_response = requests.get(token_request_url)
        token = token_request_response.json()['token']

        return token

    def get_manifest(self):
        console.log("Requesting manifest for %s..." % (self.image))
        manifest_request_url = '%s/%s/%s/manifests/%s' % (BASE_URL, self.library, self.image, self.tag)
        manifest_request_response = requests.get(manifest_request_url, headers=self.headers)
        manifest = manifest_request_response.json()
        console.ok("Manifest received!")

        return manifest

    def run(self):
        # get manifest
        manifest = self.get_manifest()
        # save manifest
        manifest_name = manifest['name'].lstrip('library/')+':'+self.tag
        path_to_manifest = os.path.join(PATH_TO_IMAGES, manifest_name)
        if not os.path.exists(path_to_manifest):
            os.makedirs(path_to_manifest)
        with open(os.path.join(path_to_manifest, manifest_name+'.json'), 'w') as manifest_file:
            manifest_file.write(json.dumps(manifest))

        # save layers
        layers_path = os.path.join(path_to_manifest, 'layers')
        if not os.path.exists(layers_path):
            os.makedirs(layers_path)
        layers = [layer['blobSum'] for layer in manifest['fsLayers']]
        # get unique layers
        layers = set(layers)
        # fetching and extracting layers
        for layer in layers:
            console.log('Getting layer %s...' % layer)
            layer_request_url = '%s/%s/%s/blobs/%s' % (BASE_URL, self.library, self.image, layer)
            tarfile_name = os.path.join(layers_path, layer) + '.tar'
            layer_request_response = requests.get(layer_request_url, stream=True, headers=self.headers)
            with open(tarfile_name, 'wb') as layer_file:
                for chunk in layer_request_response.iter_content(1024):
                    layer_file.write(chunk)
        console.ok('All layers successfully received!')

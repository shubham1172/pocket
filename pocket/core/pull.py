import requests
import json
import os
import tarfile
from pocket.utils import console

BASE_URL = 'https://registry-1.docker.io/v2'
homedir = os.environ['HOME']
PATH_TO_IMAGES = os.path.join(homedir, '.pocket/images')

class Pull():

    def __init__ (self, arg, tag='latest'):
            self.image = arg
            self.tag = tag
            self.library = 'library'
            self.headers = {'Authorization': 'Bearer %s' % self.auth(self.image, self.library)}
            if not os.path.exists(PATH_TO_IMAGES):
                os.makedirs(PATH_TO_IMAGES)

    def auth(self, image, library):
        token_request_url = 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:%s/%s:pull' % (library, image)
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

    def run(self, arg):
        # get manifest
        manifest = self.get_manifest()
        # save manifest
        with open(os.path.join(PATH_TO_IMAGES, manifest['name'].replace('/','_')+'.json'), 'w') as manifest_file:
            manifest_file.write(json.dumps(manifest))

        # save layers
        layers_path = os.path.join(PATH_TO_IMAGES, manifest['name'].replace('/','_'), 'layers')
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
            with tarfile.open(tarfile_name, 'r') as layer_tarfile:
                layer_tarfile.extractall(layers_path)
        console.ok('All layers successfully received!')

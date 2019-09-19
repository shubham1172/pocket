import requests
import json
import os
import tarfile

BASE_URL = 'https://registry-1.docker.io/v2'
PATH_TO_IMAGES = '../../images'

class Pull():

    def __init__ (self, arg):
            self.image = arg
            self.tag = 'latest'
            self.library = 'library'
            self.headers = {'Authorization': 'Bearer %s' % self.auth(self.image, self.library)}

    def auth(self, image, library):
        token_request_url = 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:%s/%s:pull' % (library, image)
        token_request_response = requests.get(token_request_url)
        token = token_request_response.json()['token']

        return token

    def get_manifest(self):
        print("Requesting manifest for %s..." % (self.image))
        manifest_request_url = '%s/%s/%s/manifests/%s' % (BASE_URL, self.library, self.image, self.tag)
        manifest_request_response = requests.get(manifest_request_url, headers=self.headers)
        manifest = manifest_request_response.json()
        print("Manifest received!")

        return manifest

    def run(self, arg):
        # get manifest
        manifest = self.manifest()
        # save manifest
        manifest_file = open(os.path.join(PATH_TO_IMAGES, manifest['name'].replace('/','_')+'.json'), 'w')
        manifest_file.write(json.dumps(manifest))
        manifest_file.close()

        # save layers
        layers_path = os.path.join(PATH_TO_IMAGES, manifest['name'].replace('/','_'), 'layers')
        if not os.path.exists(layers_path):
            os.makedirs(layers_path)
        layers = [layer['blobSum'] for layer in manifest['fsLayers']]
        # get unique layers
        layers = set(layers)
        # fetching and extracting layers
        for layer in layers:
            print('Getting layer %s...' % layer)
            layer_request_url = '%s/%s/%s/blobs/%s' % (BASE_URL, self.library, self.image, layer)
            tarfile_name = os.path.join(layers_path, layer) + '.tar'
            layer_request_response = requests.get(layer_request_url, stream=True, headers=self.headers)
            layer_file = open(tarfile_name, 'wb')
            for chunk in layer_request_response.iter_content(1024):
                layer_file.write(chunk)
            layer_file.close()
            layer_tarfile = tarfile.open(tarfile_name, 'r')
            layer_tarfile.extractall(layers_path)
            layer_tarfile.close()
        print('All layers successfully received!')

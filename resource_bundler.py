
import gzip
import base64
import json
import os

class Bundler:
    def __init__(self, resources):
        self.resources = dict()
        for file in resources:
            self.add_resource(file)

    def add_resource(self, resource):
        key = os.path.splitext(os.path.basename(resource))[0]
        with open(resource, 'r') as f:
            data = f.read()
            self.resources[key] = data

    def _encode(self, data):
        data = gzip.compress(data.encode('utf-8'))
        data = base64.b64encode(data).decode("utf-8")
        return data

    def bundle(self):
        data = json.dumps(self.resources)
        return self._encode(data)

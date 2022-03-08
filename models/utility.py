
import base64
import gzip
import json

import sys
import importlib.abc, importlib.util

class ResourceLoader(importlib.abc.SourceLoader):
    def __init__(self, resource_string):
        self.resources = json.loads(self._unpack(resource_string))
        self._sysinit()

    def _unpack(self, data):
        return gzip.decompress(base64.b64decode(data)).decode('utf-8')

    def _sysinit(self):
        for mod_name in self.resources:
            spec = importlib.util.spec_from_loader(mod_name, self, origin=mod_name)
            module = importlib.util.module_from_spec(spec)
            sys.modules[mod_name] = module
            spec.loader.exec_module(module)

    def get_data(self, path):
        try:
            return self.resources[path]
        except KeyError:
            raise ImportError()

    def get_source(self, name):
        try:
            return self.resources[name].decode('utf-8')
        except KeyError:
            raise ImportError()

    def get_filename(self, name):
        return name

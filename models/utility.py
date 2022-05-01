
import base64
import gzip
import json

import sys
import importlib.abc, importlib.util

from inspect import getmembers, isclass

# This class is used to unpack libraries that have been encoded as resource
# strings at build time
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

def cdata_dict(cd):
    if isinstance(cd, ffi.CData):
        try:
            return ffi.string(cd)
        except TypeError:
            try:
                return [cdata_dict(x) for x in cd]
            except TypeError:
                return {k: cdata_dict(v) for k, v in getmembers(cd)}
    else:
        return cd

class ObjectRegistry:
    subsystems = dict() # Mapping subsystem name + function name -> object
    def bind(self, sub, name, object):
        if sub not in self.subsystems:
            self.subsystems[sub] = dict()
        self.subsystems[sub][name] = object

    def get(self, sub, name):
        return self.subsystems[sub][name]

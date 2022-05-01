
import base64
import gzip
import json

import sys
import importlib.abc, importlib.util

from inspect import getmembers, isclass

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

_dev_id_registry = {}
def register_probe(*device_ids):
    def wrapper(func):
        func._probe = True
        _dev_id_registry[func.__name__] = device_ids
        return func
    return wrapper

_subsystem_registry = {}
def subsystem_init(*args):
    def wrapper(func):
        func._subsystem = True
        _subsystem_registry[func.__name__] = args
        return func
    return wrapper

class DeviceClass:
    subclasses = []
    id_table = dict()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._propdict = {'device': True}
        cls.subclasses.append(cls)

    def get_subclasses(self):
        print("subclasses:")
        print("\t{}".format(self.subclasses))

    def build_id_table(self):
        print(self.subclasses, len(self.subclasses))
        for cls in self.subclasses:
            functions = [(name, func) for name, func in getmembers(cls)
                        if callable(func) and type(func) is not type]
            methods = [(_dev_id_registry[name], f) for (name, f) in functions if hasattr(f, '_probe')]
            self.id_table[cls] = methods
            print("device_id: ", self.id_table)

    def call_sim_probe(self, dev_id):
        print("probing for:", dev_id)
        for device in self.id_table:
            probes = self.id_table[device]
            for sim_probe in probes:
                if dev_id in sim_probe[0]:
                    print("found!", dev_id)
                    sim_probe[1](dev_id)
        return [] # Couldn't find a simulated device

class ObjectRegistry:
    subsystems = dict() # Mapping subsystem name + function name -> object
    def bind(self, sub, name, object):
        if sub not in self.subsystems:
            self.subsystems[sub] = dict()
        self.subsystems[sub][name] = object

    def get(self, sub, name):
        return self.subsystems[sub][name]

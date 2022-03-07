import cffi
import parse_code
import json

import importlib
from pathlib import Path
import os

class Config:
    def __init__(self, config_path):
        with open(config_path) as configfile:
            self.config = json.load(configfile)

    def get_headers_dir(self):
        if "headers_dir" in self.config:
            return self.config["headers_dir"]
        else:
            return "headers/"

    def get_models_dir(self):
        if "models_dir" in self.config:
            return self.config["models_dir"]
        else:
            return "models/"

    def get_driver_dir(self):
        if "driver_dir" in self.config:
            return self.config["driver_dir"]
        else:
            return "driver/"

    def get_internal_dir(self):
        if "internal_dir" in self.config:
            return self.config["internal_dir"]
        else:
            return "internal/"

    def get_model_utilities(self):
        if "model_utilities" in self.config:
            return self.config["model_utilities"]
        else:
            return []

def parse_config(filepath):
    config = None
    with open('config.json', 'r') as configfile:
        config = json.load(configfile)
    print(config['source_dir'])

def get_py_init(imports):
    lines = ["import sys;\n"]
    body = "sys.path.insert(0, \"{}\")\n"
    for file in imports:
        lines.append(body.format(file))
    return "".join(lines)

def main():
    ffibuilder = cffi.FFI()

    config = Config("config.json")

    source = []
    (macro_vals, _, structs, prototypes, _) = parse_code.parse(config.get_headers_dir())
    (_, _, _, internal_prototypes, internal_code) = parse_code.parse(config.get_internal_dir())
    print(internal_prototypes, internal_code)

    ffibuilder.embedding_api("\n".join(prototypes))

    source = []
    list(map(source.extend, [macro_vals, structs, internal_code]))
    source = "\n".join(source)
    ffibuilder.set_source("model", source)

    source = []
    list(map(source.extend, [macro_vals, structs, internal_prototypes]))
    source = "\n".join(source)
    ffibuilder.cdef(source)

    # Concat all the python models together
    source = []
    model_list = [x for x in Path(config.get_models_dir()).rglob('*.py')]
    for file in model_list:
        with open(file) as f:
            code = f.read()
            source.append(code + "\n")

    init = get_py_init(config.get_model_utilities())
    ffibuilder.embedding_init_code(init.join(source))

    target_name = "model.*"

    ffibuilder.compile(target=target_name, verbose=True)

if __name__=="__main__":
    main()

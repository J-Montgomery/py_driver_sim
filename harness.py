import cffi
import json
from pathlib import Path

import parse_code
from resource_bundler import Bundler


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

    def get_lib_name(self):
        if "lib_name" in self.config:
            return self.config["lib_name"]
        else:
            return "model"

    def get_devicetree(self):
        if "devicetree" in self.config:
            return self.config["devicetree"]
        else:
            return "test_setup.dts"

    def get_model_utilities(self):
        if "model_utilities" in self.config:
            return self.config["model_utilities"]
        else:
            return []

    def get_bundled_utilities(self):
        if "bundled_utilities" in self.config:
            return self.config["bundled_utilities"]
        else:
            return []


def parse_config(filepath):
    config = None
    with open("config.json", "r") as configfile:
        config = json.load(configfile)
    print(config["source_dir"])


def get_py_init(imports, misc_code):
    lines = ["import sys;\n"]
    body = 'sys.path.insert(0, \"{}\")\n'
    for file in imports:
        lines.append(body.format(file))
    for stmt in misc_code:
        lines.append('{}\n'.format(stmt))
    return "".join(lines)


def concat_sources(src_list):
    source = []
    list(map(source.extend, src_list))
    return "\n".join(source)


def main():
    ffibuilder = cffi.FFI()

    config = Config("config.json")


    # edt = edtlib.EDT(config.get_devicetree(), '')

    # # Get the DT nodes that declare a compatible string
    # device_nodes = edt.compat2nodes
    # for compat in device_nodes:
    #     if "pysim" in compat:
    #         print("Pysim: {}".format(compat))
    #     else:
    #         print("device: {}".format(compat))
    # print(edt.compat2nodes)

    (macro_vals, _, structs, prototypes, _) = parse_code.parse(config.get_headers_dir())
    (_, _, _, internal_prototypes, internal_code) = parse_code.parse(
        config.get_internal_dir()
    )

    ffibuilder.embedding_api(concat_sources([prototypes]))
    ffibuilder.set_source(
        config.get_lib_name(), concat_sources([macro_vals, structs, internal_code])
    )
    ffibuilder.cdef(concat_sources([macro_vals, structs, internal_prototypes]))

    # Concat all the python models together
    source = []

    # Ensure that utilities get loaded first
    model_list = [Path(x) for x in config.get_model_utilities()]
    model_list.extend([x for x in Path(config.get_models_dir()).rglob("*.py") if x not in model_list])

    for file in model_list:
        with open(file) as f:
            code = f.read()
            source.append(code + "\n")

    bundler = Bundler(config.get_bundled_utilities())

    init_misc = "RESOURCE_STRING = \'{0}\'".format(bundler.bundle())
    init = get_py_init([], [init_misc])
    ffibuilder.embedding_init_code(init.join(source))

    target_name = config.get_lib_name() + ".*"

    ffibuilder.compile(target=target_name, verbose=True)

if __name__ == "__main__":
    main()

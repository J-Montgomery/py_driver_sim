import cffi
ffibuilder = cffi.FFI()

module_list = ["model.py", "model2.py"]

with open('lib.h') as f:
    data = ''.join([line for line in f if not line.startswith('#')])
    ffibuilder.embedding_api(data)

ffibuilder.set_source("model", r'''
    #include "lib.h"
''')
source = []

for file in module_list:
    with open(file) as f:
        code = f.read()
        source.append(code + '\n')

code = ''.join(source)
ffibuilder.embedding_init_code(code)

version = "0.1"
target_name = "model-{version}.*".format(version=version)

ffibuilder.compile(target=target_name, verbose=True)
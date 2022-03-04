import cffi
ffibuilder = cffi.FFI()

with open('lib.h') as f:
    data = ''.join([line for line in f if not line.startswith('#')])
    ffibuilder.embedding_api(data)

ffibuilder.set_source("model", r'''
    #include "lib.h"
''')

with open("model.py") as f:
    code = ''.join([line for line in f])
    ffibuilder.embedding_init_code(code)

version = "0.1"
target_name = "model-{version}.*".format(version=version)

ffibuilder.compile(target=target_name, verbose=True)
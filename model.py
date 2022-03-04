from model import ffi

@ffi.def_extern()
def call_stub(x, y):
    print("stub({0}, {1})".format(x, y))
    return x + y
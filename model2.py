from model import ffi

@ffi.def_extern()
def call_stub2(x, y):
    print("stub2({0}, {1})".format(x, y))
    return x * y
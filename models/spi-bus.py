from libharness import ffi

class SpiBus(DeviceClass):
    @register_probe('pysim,spi-bus')
    def spi_bus_init(foo):
        print("Spi bus probe!")

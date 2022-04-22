from libharness import ffi

class GenericSpiDevice(DeviceClass):
    @register_probe('pysim,generic-device')
    def spi_dev_init(foo):
        print("generic spidev probe")

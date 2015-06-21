from zorg.driver import Driver


class I2CDriver(Driver):

    def __init__(self, options, connection):
        super(I2CDriver, self).__init__(options, connection)

        self.drivers = [
            "lcd"
        ]

        self.address = options.get("address", 0x27)

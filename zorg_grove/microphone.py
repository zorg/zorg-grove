from zorg.driver import Driver
import math


class Microphone(Driver):

    def __init__(self, options, connection):
        super(Microphone, self).__init__(options, connection)

        # The value of the input voltage
        self.reference_voltage = 5.0

        self.commands += [
            "read_decibels"
        ]

    def read_decibels(self):
        """
        Returns the value of the current sound level
        in decibels.
        """
        analog_value = self.connection.analog_read(self.pin)

        # Convert the analog value to volts
        volts = (analog_value * self.reference_voltage) / 1024

        decibels = 20 * math.log(volts / self.reference_voltage)
        return decibels

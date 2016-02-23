from unittest import TestCase
from zorg_grove import LCD
from zorg_grove import Microphone
from zorg_grove import RotaryAngleSensor
from zorg_grove import Servo
from zorg_grove import TemperatureSensor


class SmokeTestCase(TestCase):

    def setUp(self):
        self.connection = None
        self.options = {}


class LCDSmokeTests(SmokeTestCase):

    def test_command_method_exists(self):
        """
        Check that each command listed has a corresponding
        method on the driver class.
        """
        lcd = LCD(self.options, self.connection)

        for command in lcd.commands:
            self.assertIn(command, dir(lcd))


class MicrophoneTests(SmokeTestCase):

    def test_command_method_exists(self):
        mic = Microphone(self.options, self.connection)

        for command in mic.commands:
            self.assertIn(command, dir(mic))


class RotaryAngleSensorSmokeTests(SmokeTestCase):

    def test_command_method_exists(self):
        sensor = RotaryAngleSensor(self.options, self.connection)

        for command in sensor.commands:
            self.assertIn(command, dir(sensor))


class ServoSmokeTests(SmokeTestCase):

    def test_command_method_exists(self):
        servo = Servo(self.options, self.connection)

        for command in servo.commands:
            self.assertIn(command, dir(servo))


class TemperatureSmokeTests(SmokeTestCase):

    def test_command_method_exists(self):
        sensor = TemperatureSensor(self.options, self.connection)

        for command in sensor.commands:
            self.assertIn(command, dir(sensor))

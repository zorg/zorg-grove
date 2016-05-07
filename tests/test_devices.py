from unittest import TestCase
from zorg_grove.microphone import Microphone
from zorg_grove.rotary_angle_sensor import RotaryAngleSensor
from zorg_grove.servo import Servo
from zorg_grove.temperature_sensor import TemperatureSensor
from .mock_device import MockAdaptor


class TestMicrophone(TestCase):

    def setUp(self):
        self.mic = Microphone({}, MockAdaptor())

    def test_read_decibels(self):
        reading = self.mic.read_decibels()
        self.assertTrue(reading < -13)
        self.assertTrue(reading > -15)


class TestRotaryAngleSensor(TestCase):

    def setUp(self):
        self.sensor = RotaryAngleSensor({}, MockAdaptor())

    def test_read_angle(self):
        # Test reading should approximate to 146.627565982404
        angle = self.sensor.read_angle()
        self.assertTrue(angle > 145)
        self.assertTrue(angle < 147)


class TestServo(TestCase):

        def setUp(self):
            self.servo = Servo({}, MockAdaptor())

        def test_set_angle(self):
            self.servo.set_angle(100)
            self.assertEqual(self.servo.angle, 100)

        def test_get_angle(self):
            self.servo.set_angle(150)
            self.assertEqual(self.servo.get_angle(), 150)


class TestTemperatureSensor(TestCase):

    def setUp(self):
        self.sensor = TemperatureSensor({}, MockAdaptor())

    def test_read_celsius(self):
        """
        Note: We assert almost equal because there are slight
        floating point differences between python 2 and 3.
        """
        self.assertAlmostEqual(
            self.sensor.read_celsius(),
            25.0,
            delta=3
        )

    def test_read_fahrenheit(self):
        """
        Note: We assert almost equal because there are slight
        floating point differences between python 2 and 3.
        """
        self.assertAlmostEqual(
            self.sensor.read_fahrenheit(),
            77.0,
            delta=3
        )

    def test_read_kelvin(self):
        """
        Note: We assert almost equal because there are slight
        floating point differences between python 2 and 3.
        """
        self.assertAlmostEqual(
            self.sensor.read_kelvin(),
            298.15,
            delta=3
        )

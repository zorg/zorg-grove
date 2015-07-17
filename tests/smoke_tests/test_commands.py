from unittest import TestCase
from zorg_grove import LCD


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


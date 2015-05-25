from zorg_i2c import I2CDriver
from time import sleep

# i2c commands
CLEARDISPLAY = 0x01
RETURNHOME = 0x02
ENTRYMODESET = 0x04
DISPLAYCONTROL = 0x08
CURSORSHIFT = 0x10
FUNCTIONSET = 0x20
SETCGRAMADDR = 0x40
SETDDRAMADDR = 0x80

# Flags for display entry mode
ENTRYRIGHT = 0x00
ENTRYLEFT = 0x02
ENTRYSHIFTINCREMENT = 0x01
ENTRYSHIFTDECREMENT = 0x00

# Flags for display on/off control
DISPLAYON = 0x04
DISPLAYOFF = 0x00
CURSORON = 0x02
CURSOROFF = 0x00
BLINKON = 0x01
BLINKOFF = 0x00

# Flags for display/cursor shift
DISPLAYMOVE = 0x08
CURSORMOVE = 0x00
MOVERIGHT = 0x04
MOVELEFT = 0x00

# Flags for function set
EIGHTBITMODE = 0x10
FOURBITMODE = 0x00
TWOLINE = 0x08
ONELINE = 0x00
FIVExTENDOTS = 0x04
FIVExEIGHTDOTS = 0x00

# Flags for backlight control
BACKLIGHT = 0x08
NOBACKLIGHT = 0x00

En = 0x04  # Enable bit
Rw = 0x02  # Read/Write bit
Rs = 0x01  # Register select bit


class LCD(I2CDriver):

    def __init__(self, options, connection):
        super(LCD, self).__init__(options, connection)

        self._backlightVal = NOBACKLIGHT
        self._displayfunction = FOURBITMODE | TWOLINE | FIVExEIGHTDOTS
        self._displaycontrol = DISPLAYON | CURSOROFF | BLINKOFF
        self._displaymode = ENTRYLEFT | ENTRYSHIFTDECREMENT

        self.commands = [
            "clear", "home", "setCursor", "displayOff",
            "displayOn", "cursorOff", "cursorOn", "blinkOff",
            "blinkOn", "backlightOff", "backlightOn", "print_string"
        ]

    def start(self):

        # initialise device
        self.connection.i2c_write(self.address, 0, 0)
        self.connection.i2c_write(self.address, 1, 0)

        sleep(0.05)

        self._expanderWrite(self._backlightVal)

        sleep(0.1)

        self._write4bits(0x03 << 4)

        sleep(0.04)

        self._write4bits(0x03 << 4)

        sleep(0.04)

        self._write4bits(0x03 << 4)
        self._write4bits(0x02 << 4)
        self._sendCommand(FUNCTIONSET | self._displayfunction)

        self.displayOn()
        self.clear()

        # Initialize to default text direction (for roman languages), set entry mode
        self._sendCommand(ENTRYMODESET | self._displaymode)
        self.home()

    def clear(self):
        """
        Clears display and returns cursor to the home position (address 0).
        """
        self._sendCommand(CLEARDISPLAY)
        sleep(2)

    def home(self):
        """
        Returns cursor to home position.
        """
        self._sendCommand(RETURNHOME)
        sleep(2)

    def setCursor(self, col, row):
        """
        Sets cursor position.
        """
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        self._sendCommand(SETDDRAMADDR | (col + row_offsets[row]))

    def displayOff(self):
        """
        Sets Off of all display (D), cursor Off (C) and
        blink of cursor position character (B).
        """
        self._displaycontrol &= ~DISPLAYON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def displayOn(self):
        """
        Sets On of all display (D), cursor On (C) and
        blink of cursor position character (B).
        """
        self._displaycontrol |= DISPLAYON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def cursorOff(self):
        """
        Turns off the cursor.
        """
        self._displaycontrol &= ~CURSORON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def cursorOn(self):
        """
        Turns on the cursor.
        """
        self._displaycontrol |= CURSORON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def blinkOff(self):
        """
        Turns off the cursor blinking character.
        """
        self._displaycontrol &= ~BLINKON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def blinkOn(self):
        """
        Turns on the cursor blinking character.
        """
        self._displaycontrol |= BLINKON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def backlightOff(self):
        """
        Turns off the back light.
        """
        self._backlightVal = NOBACKLIGHT
        self._expanderWrite(0)

    def backlightOn(self):
        """
        Turns on the back light.
        """
        self._backlightVal = BACKLIGHT
        self._expanderWrite(0)

    def backlight_color(self):
        """
        Set RGB color for the back light.
        TODO: Add parameters for values
        """
        self.connection.i2c_write(self.address, 0x08, 0xAA)
        self.connection.i2c_write(self.address, 0x04, 255)
        self.connection.i2c_write(self.address, 0x02, 255)

    def print_string(self, characters):
        """
        Prints characters on the LCD.
        """
        for char in list(characters):
            self._writeData(ord(char))

    def _write4bits(self, val):
        self._expanderWrite(val)
        self._pulseEnable(val)

    def _expanderWrite(self, data):

        print "AAA", data

        x = data | self._backlightVal
        y = x & 0xFF
        self.connection.i2c_write(self.address, 0xFF, data)

    def _pulseEnable(self, data):

        print "????????", data, En

        a = data | En
        self._expanderWrite(data)
        sleep(0.0001)
        b = data & ~En
        self._expanderWrite(b)
        sleep(0.05)

    def _sendCommand(self, value):
        self._sendData(value, 0)

    def _writeData(self, value):
        self._sendData(value, Rs)

    def _sendData(self, val, mode):
        highnib = val & 0xf0
        lownib = (val << 4) & 0xf0

        print "HIGH_LOW", highnib, lownib

        self._write4bits(highnib | mode)
        self._write4bits(lownib | mode)

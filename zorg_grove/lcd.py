from zorg.driver import Driver
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

En = 0x04  # Enable bit
Rw = 0x02  # Read/Write bit
Rs = 0x01  # Register select bit

# I2C addresses for LCD and RGB backlight
DISPLAY_COLOR_ADDRESS = 0x62
DISPLAY_TEXT_ADDRESS = 0x3e


class LCD(Driver):

    def __init__(self, options, connection):
        super(LCD, self).__init__(options, connection)

        self._displayfunction = FOURBITMODE | TWOLINE | FIVExEIGHTDOTS
        self._displaycontrol = DISPLAYON | CURSOROFF | BLINKOFF
        self._displaymode = ENTRYLEFT | ENTRYSHIFTDECREMENT

        self.bus = options.get("bus", 0)

        self.commands = [
            "clear", "home", "set_cursor", "display_off",
            "display_on", "cursor_off", "cursor_on", "blink_off",
            "blink_on", "backlight_off", "backlight_on", "print_string"
        ]

    def start(self):

        # Initialize backlight, set to black (off)
        self.connection.i2c_write(self.bus, DISPLAY_COLOR_ADDRESS, 0x00, 0)
        self.connection.i2c_write(self.bus, DISPLAY_COLOR_ADDRESS, 0x01, 0)
        
        # Currently magic values, but needed to write to rgb.
        # Pulled from https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grove_rgb_lcd/grove_rgb_lcd.py
        self.connection.i2c_write(self.bus, DISPLAY_COLOR_ADDRESS, 0x08, 0xaa)
        
        # 0x04 = R, 0x03 = G, 0x02 = B
        self.connection.i2c_write(self.bus, DISPLAY_COLOR_ADDRESS, 0x04, 0)
        self.connection.i2c_write(self.bus, DISPLAY_COLOR_ADDRESS, 0x03, 0)
        self.connection.i2c_write(self.bus, DISPLAY_COLOR_ADDRESS, 0x02, 0)
        
        sleep(0.04)

        self._write4bits(0x03 << 4)

        sleep(0.04)

        self._write4bits(0x03 << 4)

        sleep(0.04)

        self._write4bits(0x03 << 4)
        self._write4bits(0x02 << 4)
        self._sendCommand(FUNCTIONSET | self._displayfunction)

        self.display_on()
        self.clear()

        # Initialize to default text direction (for roman languages), set entry mode
        self._sendCommand(ENTRYMODESET | self._displaymode)
        self.home()

    def clear(self):
        """
        Clears display and returns cursor to the home position (address 0).
        """
        self._sendCommand(CLEARDISPLAY)
        sleep(0.05)

    def home(self):
        """
        Returns cursor to home position.
        """
        self._sendCommand(RETURNHOME)
        sleep(0.05)

    def set_cursor(self, col, row):
        """
        Sets cursor position.
        """
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        self._sendCommand(SETDDRAMADDR | (col + row_offsets[row]))

    def display_off(self):
        """
        Sets Off of all display (D), cursor Off (C) and
        blink of cursor position character (B).
        """
        self._displaycontrol &= ~DISPLAYON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def display_on(self):
        """
        Sets On of all display (D), cursor On (C) and
        blink of cursor position character (B).
        """
        self._displaycontrol |= DISPLAYON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def cursor_off(self):
        """
        Turns off the cursor.
        """
        self._displaycontrol &= ~CURSORON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def cursor_on(self):
        """
        Turns on the cursor.
        """
        self._displaycontrol |= CURSORON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def blink_off(self):
        """
        Turns off the cursor blinking character.
        """
        self._displaycontrol &= ~BLINKON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def blink_on(self):
        """
        Turns on the cursor blinking character.
        """
        self._displaycontrol |= BLINKON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def backlight_off(self):
        """
        Turns off the back light. Does so by setting the
        color to black.
        """
        self.backlight_color(0, 0, 0)
        
    def backlight_on(self):
        """
        Turns on the back light. Does so by setting the
        color to white
        """
        self.backlight_color(255, 255, 255)

    def backlight_color(self, red, green, blue):
        """
        Set RGB color for the back light.
        """
        self.connection.i2c_write(self.bus, DISPLAY_COLOR_ADDRESS, 0x04, red)
        self.connection.i2c_write(self.bus, DISPLAY_COLOR_ADDRESS, 0x03, green)
        self.connection.i2c_write(self.bus, DISPLAY_COLOR_ADDRESS, 0x02, blue)

    def print_string(self, characters):
        """
        Prints characters on the LCD.
        Automatically wraps text to fit 16 character wide display.
        """

        # Clear the display
        self.clear()

        self._sendCommand(0x08|0x04) # display on, no cursor
        self._sendCommand(0x28) # 2 lines
        sleep(0.05)
        count = 0
        row=0

        for c in characters:
            if c == '\n':
                count = 0
                row = 1
                self._sendCommand(0xc0)
                continue
            if count == 16 and row == 0:
                self._sendCommand(0xc0)
                row += 1
            count += 1
            self.connection.i2c_write(self.bus, DISPLAY_TEXT_ADDRESS, 0x40, ord(c))

    def _write4bits(self, val):
        self._pulseEnable(val)

    def _pulseEnable(self, data):

        a = data | En
        sleep(0.0001)
        b = data & ~En
        sleep(0.05)

    def _sendCommand(self, value):
        self.connection.i2c_write(self.bus, DISPLAY_TEXT_ADDRESS, 0x80, value)
        #self._sendData(value, 0)

    def _writeData(self, value):
        self._sendData(value, Rs)

    def _sendData(self, val, mode):
        highnib = val & 0xf0
        lownib = (val << 4) & 0xf0

        print "HIGH_LOW", highnib, lownib

        self._write4bits(highnib | mode)
        self._write4bits(lownib | mode)

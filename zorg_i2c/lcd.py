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

En = 0x04, # Enable bit
Rw = 0x02, # Read/Write bit
Rs = 0x01; # Register select bit


class LCD(I2CDriver):

    def __init__(self, options, connection):
        super(LCD, self).__init__(options, connection)

        self.address = options.get("address", 0x27)

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
        sleep(50)

        self._expanderWrite(self._backlightVal)
        sleep(100)

        self._write4bits(0x03 << 4)
        sleep(4)

        self._write4bits(0x03 << 4)
        sleep(4)

        self._write4bits(0x03 << 4)
        self._write4bits(0x02 << 4)
        self._sendCommand(FUNCTIONSET | self._displayfunction)

        self.displayOn()
        self.clear()

        # Initialize to default text direction (for roman languages), set entry mode
        self._sendCommand(ENTRYMODESET | self._displaymode)
        self.home()

        '''
        while True:
            self._expanderWrite(self._backlightVal)
        '''

    def clear(self):
        self._sendCommand(CLEARDISPLAY)
        sleep(2)

    def home(self):
        self._sendCommand(RETURNHOME)
        sleep(2)

    def setCursor(self, col, row):
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        self._sendCommand(SETDDRAMADDR | (col + row_offsets[row]))

    def displayOff(self):
        self._displaycontrol &= ~DISPLAYON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def displayOn(self):
        self._displaycontrol |= DISPLAYON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def cursorOff(self):
        self._displaycontrol &= ~CURSORON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def cursorOn(self):
        self._displaycontrol |= CURSORON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def blinkOff(self):
        self._displaycontrol &= ~BLINKON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def blinkOn(self):
        self._displaycontrol |= BLINKON
        self._sendCommand(DISPLAYCONTROL | self._displaycontrol)

    def backlightOff(self):
        self._backlightVal = NOBACKLIGHT
        self._expanderWrite(0)

    def backlightOn(self):
        self._backlightVal = BACKLIGHT
        self._expanderWrite(0)

    def print_string(self, characters):
        for char in characters:
            self._writeData(char)

    def _write4bits(self, val):
        self._expanderWrite(val)
        self._pulseEnable(val)

    def _expanderWrite(self, data):
        self.connection.i2cWrite(self.address, (data | self._backlightVal) & 0xFF)

    def _pulseEnable(self, data):
        self._expanderWrite(data | En)
        sleep(0.0001)
        self._expanderWrite(data & ~En)
        sleep(0.05)

    def _sendCommand(self, value):
        self._sendData(value, 0)

    def _writeData(self, value):
        self._sendData(value, Rs)

    def _sendData(self, val, mode):
        highnib = val & 0xf0
        lownib = (val << 4) & 0xf0

        self._write4bits(highnib | mode)
        self._write4bits(lownib | mode)

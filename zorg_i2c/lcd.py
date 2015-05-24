from .zorg_i2c import I2CDriver
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

        self.address = self.address || 0x27

        self._backlightVal = NOBACKLIGHT
        self._displayfunction = FOURBITMODE | TWOLINE | FIVExEIGHTDOTS
        self._displaycontrol = DISPLAYON | CURSOROFF | BLINKOFF
        self._displaymode = ENTRYLEFT | ENTRYSHIFTDECREMENT

        self.commands = [
            "clear", "home", "setCursor", "displayOff",
            "displayOn", "cursorOff", "cursorOn", "blinkOff",
            "blinkOn", "backlightOff", "backlightOn", "print_string"
        ]

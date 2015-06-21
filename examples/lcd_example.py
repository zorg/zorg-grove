import zorg
import time

def work (my):

    my.lcd.start()

    while True:

        # Display some text and change the backlight color
        my.lcd.print_string("Hello")
        my.lcd.backlight_color(255, 255, 255)

        my.lcd.blinkOff()

        # Wait 400ms before doing it again
        time.sleep(0.4)

robot = zorg.robot({
    "connections": {
        "edison": {
            "adaptor": "zorg_edison.Edison",
        },
    },
    "devices": {
        "led": {
            "connection": "edison",
            "driver": "zorg_gpio.Led",
            "pin": 13, # 13 is the on-board LED
        },
        "lcd": {
            "connection": "edison",
            "driver": "zorg_grove.LCD",
        }
    },
    "name": "example", # Give your robot a unique name
    "work": work, # The method (on the main level) where the work will be done
})

robot.start()

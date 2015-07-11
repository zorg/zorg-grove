import zorg
from time import sleep

def work (my):

    my.lcd.start()
    my.lcd.print_string("Hello!")
    
    sleep(2.0)
    
    my.lcd.cursor_on()
    my.lcd.print_string("Cursor on")

    sleep(2.0)
    
    my.lcd.blink_on()
    my.lcd.print_string("Blink on")
    
    sleep(5.0)
    
    my.lcd.blink_off()
    my.lcd.print_string("Blink off")
    
    sleep(5.0)
    
    my.lcd.cursor_on()
    my.lcd.print_string("Cursor off")
    
    sleep(2.0)
    
    my.lcd.backlight_on()
    my.lcd.print_string("Backlight on")
    
    sleep(2.0)
    
    my.lcd.backlight_off()
    my.lcd.print_string("Backlight off")
    
    sleep(2.0)
    
    my.lcd.backlight_color(255,0,0)
    my.lcd.print_string("Red")
    
    sleep(2.0)
    
    my.lcd.backlight_color(0,255,0)
    my.lcd.print_string("Green")
    
    sleep(2.0)
    
    my.lcd.backlight_color(0,0,255)
    my.lcd.print_string("Blue")
    
    sleep(2.0)
    
    my.lcd.backlight_color(155,255,0)
    my.lcd.print_string("Yellow")
    
    
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
            "address":  0x62,
        }
    },
    "name": "example", # Give your robot a unique name
    "work": work, # The method (on the main level) where the work will be done
})

robot.start()

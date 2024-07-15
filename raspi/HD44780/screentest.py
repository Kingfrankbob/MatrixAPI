import RPi.GPIO as GPIO
from charlcd import direct as lcd
from charlcd.drivers.gpio import Gpio

GPIO.setmode(GPIO.BCM)
g = Gpio()
g.pins = {
    'RS': 13,
    'E': 19,
    'E2': 26,
    'DB4': 12,
    'DB5': 16,
    'DB6':20,
    'DB7':21
}

l = lcd.CharLCD(40, 4, g)
l.init()

l.stream("Test bro")
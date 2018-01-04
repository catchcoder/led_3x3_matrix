
"""
01 Flash LEDs with a Raspberry PI
Parts needed:
    1 x Raspberry PI
   27 x LEDS
    2 x switch non-latching
"""

try:
    import RPi.GPIO as GPIO
except ImportError:
    """
    import fake as GPIO
    https://pypi.python.org/pypi/fakeRPiGPIO/0.2a0
    """
    from RPi import GPIO

import time
import sys

leds = [17, 27, 22, 10, 9, 11, 5, 6, 13]
levels = [2, 3, 4]
run = True
btnstartstop = 19
btnplay = 26
delay = 0.01
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def setupbuttons():
    """ Setup Start/Stop button on GPIO12
    """
    GPIO.setup(btnstartstop, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def setupleds():
    """ Setup GPIOs for LEDS
    """
    for led in leds:
        GPIO.setup(led, GPIO.OUT)


def setuplevels():
    """ Setup negitive for LEDs
    """
    for level in levels:
        GPIO.setup(level, GPIO.OUT)


def alloff():
    """ Turn off all LEDs and set ground voltage to high
    """
    checkifbuttonpressed()
    global leds
    global levels
    for led in leds:
        GPIO.output(led, GPIO.LOW)
    for level in levels:
        GPIO.output(level, GPIO.HIGH)


def checkifbuttonpressed():
    global run
    """ Check if Button pressed
	"""
    if not GPIO.input(btnstartstop):
        run = False


setupbuttons()
setupleds()
setuplevels()

""" Basic light up
"""


def main():

    global run
    try:
        while run:
            for level in levels:
                for led in leds:
                    alloff()
                    if run == False:
                        break
                    GPIO.output(led, GPIO.HIGH)
                    GPIO.output(level, GPIO.LOW)
                    time.sleep(delay)
    except KeyboardInterrupt:
        GPIO.cleanup()

    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    main()

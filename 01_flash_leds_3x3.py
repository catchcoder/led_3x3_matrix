
"""
01 Flash LEDS with a Raspberry PI
Parts needed:
    1 x Raspberry PI
   27 x LEDS
    2 x switch non-latching
"""

try:
    # Try and import GPIO for Raspberry Pi.
    # If it fails import fake GPIO for CI.
    import RPi.GPIO as GPIO
except ImportError:
    # Import fake as GPIO https://pypi.python.org/pypi/fakeRPiGPIO/0.2a0.
    from RPi import GPIO

import time
import sys

LEDS = [17, 27, 22, 10, 9, 11, 5, 6, 13]
LEVELS = [2, 3, 4]
RUN = True
BTNSTARTSTOP = 19
BTNPLAY = 26
DELAY = 0.01
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def setupbuttons():
    """ Setup Start/Stop button on GPIO12.
    """
    GPIO.setup(BTNSTARTSTOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def setupleds():
    """ Setup GPIOs for LEDS.
    """
    for led in LEDS:
        GPIO.setup(led, GPIO.OUT)


def setuplevels():
    """ Setup negitive for LEDS.
    """
    for level in LEVELS:
        GPIO.setup(level, GPIO.OUT)


def alloff():
    """ Turn off all LEDS and set ground voltage to high.
    """
    checkifbuttonpressed()

    for led in LEDS:
        GPIO.output(led, GPIO.LOW)
    for level in LEVELS:
        GPIO.output(level, GPIO.HIGH)


def checkifbuttonpressed():
    """ Check if Button pressed.
    """
    global RUN
    if not GPIO.input(BTNSTARTSTOP):
        RUN = False


setupbuttons()
setupleds()
setuplevels()


def main():
    """ Flash the LEDs.
    """
    try:
        while RUN:
            for level in LEVELS:
                for led in LEDS:
                    alloff()
                    if not RUN:
                        break
                    GPIO.output(led, GPIO.HIGH)
                    GPIO.output(level, GPIO.LOW)
                    time.sleep(DELAY)
    except KeyboardInterrupt:
        GPIO.cleanup()

    GPIO.cleanup()
    sys.exit(0)


if __name__ == '__main__':
    main()


""" Flash LEDS with a Raspberry PI
Parts needed:
    1 x Raspberry PI
   27 x LEDS
    2 x switch non-latching
"""

try:
    # Try and import GPIO for Raspberry Pi,
    # If it fails import fake GPIO for CI.
    import RPi.GPIO as GPIO
except ImportError:
    # Import fake GPIO https://pypi.python.org/pypi/fakeRPiGPIO/0.2a0.
    from RPi import GPIO

import time
import sys
import random

run = True
c_led = 0
DELAY = 0.3  # time delay between LED

LEDS_PINS = [17, 27, 22, 10, 9, 11, 5, 6, 13]
LEVELS_PINS = [2, 3, 4]

BTNSTARTSTOP = 19
BTNPLAY = 26

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def setupbuttons():
    """ Setup Start/Stop button on GPIO12.
    """
    GPIO.setup(BTNSTARTSTOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def setupleds():
    """ Setup GPIOs for LEDS.
    """
    for led in LEDS_PINS:
        GPIO.setup(led, GPIO.OUT)


def setuplevels():
    """ Setup negitive for LEDS.
    """
    for level in LEVELS_PINS:
        GPIO.setup(level, GPIO.OUT)


def alloff():
    """ Turn off all LEDS and set ground voltage to high.
    """
    checkifbuttonpressed()

    for led in LEDS_PINS:
        GPIO.output(led, GPIO.LOW)
    for level in LEVELS_PINS:
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
    """ Basic light up.
    """
    l_led = 0  # LED to light up
    try:
        while run:
            while True:
                c_led = random.choice(LEDS_PINS)
                if c_led != l_led:  # don't light up the same light twice
                    break

            # print (c_led)
            l_led = c_led
            alloff()

            if not run:
                break

            GPIO.output(l_led, GPIO.HIGH)
            for level in LEVELS_PINS:
                GPIO.output(level, GPIO.LOW)
                time.sleep(DELAY)
                GPIO.output(level, GPIO.HIGH)

    except KeyboardInterrupt:
        GPIO.cleanup()

    GPIO.cleanup()
    sys.exit(0)


if __name__ == '__main__':
    main()

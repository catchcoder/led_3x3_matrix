
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

_play = False   # play pattern and next pattern
__run = True    # stop code from running

delay = 0.05  # time delay between LED, default in case not set
pattern_routine = 0  # start pattern with 0, change to start with another

LEDS_PINS = [17, 27, 22, 10, 9, 11, 5, 6, 13]   # GPIO pins used for LED +
LEVELS_PINS = [2, 3, 4]     # GPIO pins used for LED -
PATTERN_TEARS = [
    [9, 2, 9, 3, 9, 4],
    [17, 2, 17, 3, 17, 4, 22, 2, 22, 3, 22, 4, 13, 2, 13, 3, 13, 4, 5, 2, 5, 3,
     5, 4],
    [27, 2, 27, 3, 27, 4, 11, 2, 11, 3, 11, 4, 6, 2, 6, 3, 6, 4, 10, 2, 10, 3,
     10, 4]]

PATTERN_SPIRAL = [
    9, 2, 10, 2, 17, 2, 27, 2, 22, 2, 11, 2, 13, 2, 6, 2, 5, 2, 9, 3, 10, 3,
    17, 3, 27, 3, 22, 3, 11, 3, 13, 3, 6, 3, 5, 3, 9, 4, 10, 4, 17, 4, 27, 4,
    22, 4, 11, 4, 13, 4, 6, 4, 5, 4]

BTNSTARTSTOP = 19   # GPIO pin  used for start, stop and next pattern
BTNRUN = 26       # GPIO pin Used to stop python code from running

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def setupbuttons():
    """ Setup Start/Stop button on GPIO12.
    """
    GPIO.setup(BTNSTARTSTOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BTN_run, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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
    global _play
    global _run
    if not GPIO.input(BTNSTARTSTOP):
        _play = not _play
        time.sleep(0.3)  # stop debounce when pressing button
    if not GPIO.input(BTNRUN):
        __run = False


def pattern_random_rain():
    """ Rain Pattern.
    """
    l_led = 0  # LED to light up
    c_led = 0       # counter for LEDS
    global _play
    delay = 0.05
    try:
        while _play:
            while True:
                c_led = random.choice(LEDS_PINS)
                if c_led != l_led:  # don't light up the same light twice
                    break
            l_led = c_led
            alloff()

            if not _play:
                break

            GPIO.output(l_led, GPIO.HIGH)
            for level in LEVELS_PINS:
                GPIO.output(level, GPIO.LOW)
                time.sleep(delay)
                GPIO.output(level, GPIO.HIGH)

    except KeyboardInterrupt:
        _play = False


def pattern_tears():
    """ Tears routine.
    """
    try:
        print (len(PATTERN_SPIRAL))
        global _play
        delay = 0.3
        while _play:
            for LEDS in PATTERN_TEARS:
                i = 0
                while i < len(LEDS):
                    alloff()
                    if not _play or not _run:
                        break
                    GPIO.output(LEDS[i], GPIO.HIGH)
                    GPIO.output(LEDS[i + 1], GPIO.LOW)
                    time.sleep(delay)
                    i += 2

    except KeyboardInterrupt:
        _play = False


def pattern_spiral():
    """ Spiral
    """
    try:
        global _play
        delay = 0.03
        while _play:
            i = 0
            while i < len(PATTERN_SPIRAL):
                alloff()
                print ("i = ", i)
                if not _play:
                    break
                GPIO.output(PATTERN_SPIRAL[i], GPIO.HIGH)
                GPIO.output(PATTERN_SPIRAL[i + 1], GPIO.LOW)
                time.sleep(delay)
                i += 2
            i = (len(PATTERN_SPIRAL) - 2)
            while i > 0:
                alloff()
                if not _play:
                    break
                GPIO.output(PATTERN_SPIRAL[i], GPIO.HIGH)
                GPIO.output(PATTERN_SPIRAL[i + 1], GPIO.LOW)
                i -= 2
                time.sleep(delay)
    except KeyboardInterrupt:
        _play = False


PATTERN_ROUTINES = {0: pattern_random_rain,
                    1: pattern_tears,
                    2: pattern_spiral}


def main():
    """ Main routine with switch bewtween patterns.
    """
    alloff()  # clear all LEDs.
    try:
        global pattern_routine
        # print ("routines ", len(PATTERN_ROUTINES)
        while _run:
            global pattern_routine
            checkifbuttonpressed()
            if _play:
                print ("pattern ", pattern_routine)
                PATTERN_ROUTINES[pattern_routine]()
                pattern_routine += 1
                if pattern_routine > 2:
                    pattern_routine = 0
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)

    GPIO.cleanup()


setupbuttons()
setupleds()
setuplevels()


if __name__ == '__main__':
    main()


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

play = False
run = True
c_led = 0
delay = 0.05  # time delay between LED

LEDS_PINS = [17, 27, 22, 10, 9, 11, 5, 6, 13]
LEVELS_PINS = [2, 3, 4]
PATTERN = [
    [9, 2, 9, 3, 9, 4],
    [17, 2, 17, 3, 17, 4, 22, 2, 22, 3, 22, 4, 13, 2, 13, 3, 13, 4, 5, 2, 5, 3,
     5, 4],
    [27, 2, 27, 3, 27, 4, 11, 2, 11, 3, 11, 4, 6, 2, 6, 3, 6, 4, 10, 2, 10, 3,
     10, 4]]

BTNSTARTSTOP = 19
BTNRUN = 26

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def setupbuttons():
    """ Setup Start/Stop button on GPIO12.
    """
    GPIO.setup(BTNSTARTSTOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BTNRUN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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
    global play
    global run
    if not GPIO.input(BTNSTARTSTOP):
        play != play
    if not GPIO.input(BTNRUN):
        run = False


def pattern_random_rain():
    """ Rain Pattern.
    """
    l_led = 0  # LED to light up
    global play
    try:
        while play:
            while True:
                c_led = random.choice(LEDS_PINS)
                if c_led != l_led:  # don't light up the same light twice
                    break
            l_led = c_led
            alloff()

            if not play:
                break

            GPIO.output(l_led, GPIO.HIGH)
            for level in LEVELS_PINS:
                GPIO.output(level, GPIO.LOW)
                time.sleep(delay)
                GPIO.output(level, GPIO.HIGH)

    except KeyboardInterrupt:
        play = False


def pattern_tears():
    """ Basic light up.
    """
    global play
    delay = 0.3
    try:
        while play:
            for LEDS in PATTERN:
                alloff()

                if not play:
                    break
                i = 0
                while i < len(LEDS):
                    alloff()
                    GPIO.output(LEDS[i], GPIO.HIGH)
                    GPIO.output(LEDS[i + 1], GPIO.LOW)
                    time.sleep(delay)
                    i += 2
                time.sleep(DELAY)

    except KeyboardInterrupt:
        play = False

def main():
    """ Main routine to loop patterns.
    """
    try:
        while run:
            checkifbuttonpressed()
            if play:
                pattern_random_rain()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)


setupbuttons()
setupleds()
setuplevels()


if __name__ == '__main__':
    main()

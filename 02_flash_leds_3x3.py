
"""
Flash LEDs with a Raspberry PI
Parts needed:
    1 x Raspberry PI
    9 x LEDS
    2 x switch non-latching
"""

import time
import RPi.GPIO as GPIO

leds = [17, 27, 22, 10, 9, 11, 5, 6, 13]
levels = [2, 3, 4]
pattern = [
    [9, 2, 9, 3, 9, 4],
    [17, 2, 17, 3, 17, 4, 22, 2, 22, 3, 22, 4, 13, 2, 13, 3, 13, 4, 5, 2, 5, 3,
     5, 4],
    [27, 2, 27, 3, 27, 4, 11, 2, 11, 3, 11, 4, 6, 2, 6, 3, 6, 4, 10, 2, 10, 3,
     10, 4]]

run = True
btnstartstop = 19
btnplay = 26
delay = 0.05
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
    """ Check if Button pressed
    """
    global run
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
            for leds in pattern:
                alloff()

                if not run:
                    break
                i = 0
                while i < len(leds):
                    alloff()
                    GPIO.output(leds[i], GPIO.HIGH)
                    GPIO.output(leds[i + 1], GPIO.LOW)
                    time.sleep(0.05)
                    i += 2
                time.sleep(delay)

    except KeyboardInterrupt:
        GPIO.cleanup()

    GPIO.cleanup()


if __name__ == '__main__':
    main()

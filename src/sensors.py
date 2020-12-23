import time
#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BOARD)


class push_button:

    def __init__(self, pin):
        self.pin = pin
        #GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def pushed(self):
        #return GPIO.input(self.pin)
        pass


def reset_gpio():
    # éteindre le GPIO
    #GPIO.cleanup()
    pass

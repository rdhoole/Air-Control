#!/usr/bin/env python
# Ryan Hoole

# Control our fan

import RPi.GPIO as GPIO
from subprocess import Popen, PIPE
import argparse

# setup pin for fan
fan = 17
feedback = 13
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# these are the arguments to be passed into our program
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--option", metavar="OPTION",
                    help="on, off or status")
parser.add_argument("-v", "--verbose", help="outputs more information")
args = parser.parse_args()

# print out more information
v = False
if args.verbose:
    v = True

# functions for doing stuffs
def is_compressor_on():
    return False
#    process = Popen(["python", "compressor-control.py", "-o", "status"], stdout=PIPE)
#    (output, err) = process.communicate()
#    exit_code = process.wait()
#    if output == "on\n":
#        return True
#    else:
#        return False
def fan_on():
    if v:
        print("turning fan on")
    # setup pin for output
    GPIO.setup(fan, GPIO.OUT)
    # set the pin high
    GPIO.output(fan, GPIO.HIGH)

def fan_off():
    if v:
        pass
        #print "checking if compressor is on"
    if not is_compressor_on():
        if v:
            print("turning fan off")
        # setup pin for output
        GPIO.setup(fan, GPIO.OUT)
        # set the pin low
        GPIO.output(fan, GPIO.LOW)
    else:
        if v:
            print("NOT turning fan off, compressor on!")
        else:
            print("compressor on")

def fan_status():
    status = "status: "
    # setup pin for input
    GPIO.setup(feedback, GPIO.IN)
    if GPIO.input(feedback):
        if v:
            print(status+"off")
        else:
            print("off")
    else:
        if v:
            print(status+"on")
        else:
            print("on")


# handle arguments
if args.option:
    opt = args.option

    if (opt == "on"):
        fan_on()
    elif (opt == "off"):
        fan_off()
    elif (opt == "status"):
        fan_status()
    else:
        print(opt+" is an invaild option")

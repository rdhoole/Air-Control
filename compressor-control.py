#!/usr/bin/env python

# Control our compressor

import RPi.GPIO as GPIO
from subprocess import Popen, PIPE
import argparse

# setup pin for compressor
compressor = 27
feedback = 19
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
def is_fan_on():
    process = Popen(["python", "fan-control.py", "-o", "status"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
#    if output == "on\n":
#        return True
#    else:
#        return False
    return True # bypass for now

def compressor_on():
    if v:
        print("checking if fan is on...")
    if is_fan_on():
        if v:
            print("turning compressor on")
        # setup pin for output
        GPIO.setup(compressor, GPIO.OUT)
        # set the pin high
        GPIO.output(compressor, GPIO.HIGH)
    else:
        if v:
            print("NOT turning on compressor, fan not on!")
        else:
            print("fan off")

def compressor_off():
    if v:
        print("turning compressor off")
    # setup pin for output
    GPIO.setup(compressor, GPIO.OUT)
    # set the pin low
    GPIO.output(compressor, GPIO.LOW)    

def compressor_status():
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
        compressor_on()
    elif (opt == "off"):
        compressor_off()
    elif (opt == "status"):
        compressor_status()
    else:
        print(opt+" is an invaild option")

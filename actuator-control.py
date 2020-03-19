#!/usr/bin/env python

# Control our actuator

import RPi.GPIO as GPIO
import argparse

# setup pin for actuator
actuator = 22
feedback = 26
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
def actuator_on():
    if v:
        print("turning actuator on")
    # setup pin for output
    GPIO.setup(actuator, GPIO.OUT)
    # set the pin high
    GPIO.output(actuator, GPIO.HIGH)

def actuator_off():
    if v:    
        print("turning actuator off")
    # setup pin for output
    GPIO.setup(actuator, GPIO.OUT)
    # set the pin low
    GPIO.output(actuator, GPIO.LOW)    

def actuator_status():
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
        actuator_on()
    elif (opt == "off"):
        actuator_off()
    elif (opt == "status"):
        actuator_status()
    else:
        print(opt+" is an invaild option")

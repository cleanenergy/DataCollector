#coding: utf-8

################################################################
# CLEAN ENERGY SOLUTIONS - 2018
#
# Signal Processing Layer
#
# Create by: Renato Pereira Nominato, Emílio Palote Santos
#
# Repository: https://github.com/cleanenergy/DataCollector
#
# This layer treats the signal obtained from the meter and 
# accumulates solar generation values
#
################################################################

import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep
import DAL


wh = 0.0
timestamp = ""

# Pulse of the meter: 
#       Min duration = 100ms
#       Máx duration = 120ms
# The program waits debouncingTime for debouncing
# Default: 50 ms
debouncingTime = 0.05

timestamp, wh = DAL.readFromFile()


def configurePi():
    # Configure the I/O ports of the Raspberry and the interruption events
    #       GPIO 26 : pulse of meter every 0.5 wh generated

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(26, GPIO.RISING, callback=recordPulse)


def recordPulse(channel):
    # Record every pulse of the meter and write it on log measure file
    
    # Starts a global variables
    global wh
    global debouncingTime
    global timestamp
    
    timeNow = datetime.now()

    # Wait debouncing time
    sleep(debouncingTime)
    
    # If debouncing is OK, save the data
    if GPIO.input(26):
        
        wh = float(wh) + 0.5
        timestamp = timeNow.strftime(DAL.getDateFormat())
        
        DAL.writeToFile(timestamp, str(wh))

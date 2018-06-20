import RPi.GPIO as GPIO
from datetime import datetime
from datetime import timedelta
from time import sleep
import DAL


kwh = 0.0
timestamp = ""
pulseDuration = timedelta(seconds=0.5)
timestamp, kwh = DAL.readFromFile()


def configurePi():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(26, GPIO.RISING, callback=recordPulse)


def recordPulse(channel):
    
    global kwh
    global pulseDuration
    global timestamp
    
    timeNow = datetime.now()
    sleep(0.050)
    
    if GPIO.input(26):
        
        kwh = float(kwh) + 0.5
        timestamp = timeNow.strftime("%Y-%m-%d %H:%M:%S")
        
        DAL.writeToFile(timestamp, str(kwh))

import RPi.GPIO as GPIO
from datetime import datetime
from datetime import timedelta
import DAL


kwh = 0
timestamp = ""
timeRef = datetime.now()
pulseDuration = timedelta(seconds=0.5)
timestamp, kwh = DAL.readFromFile()


def configurePi():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(26, GPIO.RISING, callback=recordPulse)


def recordPulse(channel):
    
    global kwh
    global timeRef
    global pulseDuration
    global timestamp
    
    timeNow = datetime.now()
    
    if (timeNow - timeRef) >= pulseDuration:
        
        kwh = kwh + 0.005*1000
        timestamp = timeNow.strftime("%Y-%m-%d %H:%M:%S")
        timeRef = timeNow
        
        DAL.writeToFile(timestamp, kwh)

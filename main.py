#! DataCollector
#coding: utf-8

################################################################
# CLEAN ENERGY SOLUTIONS - 2018
#
# Main code
#
# Create by: Renato Pereira Nominato, Emílio Palote Santos
#
# Repository: https://github.com/cleanenergy/DataCollector
#
# This code has the main code to monitoring a solar energy
# production system with cloud sending data.
#
################################################################

import DAL
import SPL
import json
import sys
from time import sleep
from datetime import datetime
from tkinter import *

def main():
    
    # Configure a Raspberry I/O
    SPL.configurePi()

    # Create a GUI info system 
    root = Tk()
    root.title("Running monitoring system...")
    message = StringVar()
    message.set("Initializing...")
    Label(root, textvariable=message, width = 50, height = 10).pack()
    root.update()

    while(1):
        try:
            config = json.load(open("config.json"))
            fs = config["sensor"]["fs"]
        except:
            print("Error reading configurations")
        
        sleep(fs)

        DAL.printLog("\n\n\n---------------------------\nInitializing a sending routine...\n")
        print("\n\n\n---------------------------\nInitializing a sending routine...\n")

        # Get the last measure
        wh = DAL.getLastMeasure()

        # Get the now time
        timestamp = datetime.now().strftime(DAL.getDateFormat())

        # Send data to cloud server
        DAL.sendData(timestamp, wh)

        # Try send unsent data from the queue
        DAL.resendQueue()

        DAL.printLog("Finished a sending routine.\n\n\nWaiting for the next time...")
        print("Finished a sending routine.\n\n\nWaiting for the next time...")

        # Restart a window message display
        try:
            root.destroy()
        except:
            pass

        root = Tk()
        root.title("Running monitoring system...")
        message = StringVar()
        message.set("The system is running...\n Last update: " + timestamp + "\n Everything working fine!\n\n" + str(float(wh)/1000) + " kWh\n is the acumulated energy generated")
        Label(root, textvariable=message, width = 50, height = 10).pack()
        root.update()
    
if __name__ == "__main__":
    main()
    
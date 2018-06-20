#coding: utf-8
################################################################
# CLEAN ENERGY SOLUTIONS - 2018
#
# Data Access Layer - DAL
#
# Create by: Renato Pereira Nominato, Emílio Palote Santos
#
# Repository: https://github.com/cleanenergy/DataCollector
#
# This code has the functions to send to cloud and save locally 
# the informations about de generate energy.
#
################################################################

import requests
import json
import ast
import csv
from datetime import datetime, timedelta


def sendData(timestamp, value):
    # Send Data to de cloud server
    #      - timestamp: Date timestamp format "%Y-%m-%d %H:%M:%S"
    #      - value: Measure of energy
    
    result = ""

    # Get URL and UG id informations in configurations 
    config = json.load(open("config.json"))
    url = config["site"]["url"]
    ug = config["client"]["ug"]

    # Make a log info about the data will be send
    data = {'ug':ug, 'data_hora':timestamp, 'medida':value}
    print(str(data) + " | Sending...")
    printLog(str(data) + " | Sending...")
    
    # Try post the data
    try:
        r = requests.post(url, data=data)
        print("Uploaded data!")
        printLog("Uploaded data!")
    except Exception as e:
        print("Error sending data: " + str(e))
        printLog("Error: sending data" + str(e))
        print("Adding data to queue...")
        printLog("Adding data to queue...")
        addToQueue(timestamp, value)

    # Try get post response informations
    try:
        result = r.content
        result = result.decode("utf-8")
        result = ast.literal_eval(result)
        print("Status: " + result["status"])
        printLog("Status: " + result["status"])
    except:
        result = {"status":"fail"}
        print("Status: " + result["status"])
        printLog("Status: " + result["status"])
    
    return result

def getMeasure():
    # Return the last measure data
    timestamp, wh = readFromFile()
    return wh

def getDateFormat():
    # Return a date format string
    return "%Y-%m-%d %H:%M:%S"

def readFromFile():
    # Read a last measure energy computed on csv file

    # Get the name of measures log atual    
    fileName = getFileName()
    data = []
    timestamp = datetime.now().strftime(getDateFormat())    
    wh = 0
    
    # Try open the today's measure log
    try:
        f = open(fileName, 'r')
        spamreader = csv.reader(f, delimiter=";", quotechar="|")

        try:
            data = list(spamreader)
            lastRow = data[-1]
            timestamp = lastRow[0]
            wh = lastRow[1]
        except:
            print("Error reading the last measure of the file!")
            printLog("Error reading the last measure of the file!")

        f.close()

    # If it still not exist, get a yesterday last measure and 
    # save this on today's log measure

    except IOError:
        fileName = getFileName(daysBefore=1)
        try:
            f = open(fileName, 'r')
            spamreader = csv.reader(f, delimiter=";", quotechar="|")
            data = list(spamreader)
            lastRow = data[-1]
            timestamp = lastRow[0]
            wh = lastRow[1]
            writeToFile(timestamp, wh)
            print("Today's log measure does not exist. Yesterday's last measure used.")
            printLog("Today's log measure does not exist. Yesterday's last measure used.")
        # If yesterday log archive does not exist, 
        # return now as timestamp and 0 as measure
        except:
            print("Yesterday log measure does not exist. Zero was returned")
            printLog("Yesterday log measure does not exist. Zero was returned")
            writeToFile(timestamp, wh)
        f.close()

    return timestamp, wh


def writeToFile(timestamp, wh):
    # Write a measure in the csv file
    
    fileName = getFileName()
    
    with open(fileName,"a") as f:
        spamwriter = csv.writer(f, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([timestamp, wh])


def addToQueue(timestamp, wh):
    # Adds a measure not sent in the queue

    with open("./data/queue.csv","a") as f:
        spamwriter = csv.writer(f, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([timestamp, wh])
    print("Data added to queue!")
    printLog("Data added to queue!")

def resendQueue():
    #Resend queue of unsent measures
    queue = getFromQueue()

    for measure in queue:
        print("Resending measure... | " + measure[0] + ": " + measure[1])
        printLog("Resending measure... | " + measure[0] + ": " + measure[1])
        sendData(measure[0], measure[1])

def getFromQueue():
    # Gets the queue of unsent measures

    data = []
    
    try:
        print("Trying to retrieve the unsent data queue...")
        printLog("Trying to retrieve the unsent data queue...")
        f = open("./data/queue.csv","r")
        spamreader = csv.reader(f, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        data = list(spamreader)
        f.close()
        print("Queue of unsent data retrieved")
        printLog("Queue of unsent data retrieved")
    except IOError:
        print("There is no queue file.")
        printLog("There is no queue file.")

    try:
        print("Starting a new queue...")
        printLog("Starting a new queue...")
        f = open("./data/queue.csv","w")
        f.close()
        print("New queue of unsent data started")
        printLog("New queue of unsent data started")
    except IOError:
        print("Error starting a new queue! " + IOError)
        printLog("Error starting a new queue!" + IOError)
    
    return data


def getFileName(daysBefore=0):
    # Get a measure log file name.
    #       - daysBefore: number os days before today

    date = datetime.today() - timedelta(days=daysBefore)
    fileName = "./data/" + date.strftime("%Y%m%d") + ".csv"
    return fileName

def printLog(message):

    fileName = "./data/runlog.csv"

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " :"

    with open(fileName,"a") as f:
        f.write(date + message)











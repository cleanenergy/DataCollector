import requests
import json
import ast
import csv
from datetime import datetime


fileName = "data.csv"


def sendData(timestamp, value):
    
    result = ""
    config = json.load(open("config.json"))

    url = config["site"]["url"]
    ug = config["client"]["ug"]


    data = {'ug':ug, 'data_hora':timestamp, 'medida':value}
    print(data)
    
    try:
        r = requests.post(url, data=data)
    except Exception as e:
        print("Error: " + str(e))

    try:
        result = r.content
        result = result.decode("utf-8")
        result = ast.literal_eval(result)
    except:
        result = {"status":"fail"}
        
    return result


def readFromFile():
    
    global fileName
    data = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    kwh = 0
    
    with open(fileName, "r") as f:
        spamreader = csv.reader(f, delimiter=";", quotechar="|")
        try:
            data = list(spamreader)
            lastRow = data[-1]
            timestamp = lastRow[0]
            kwh = lastRow[1]
        except:
            print("Error reading file")

    return timestamp, kwh


def writeToFile(timestamp, kwh):
    
    global fileName
    
    with open(fileName,"a") as f:
        spamwriter = csv.writer(f, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([timestamp, kwh])


def addToQueue(timestamp, kwh):

    with open("queue.csv","a") as f:
            spamwriter = csv.writer(f, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([timestamp, kwh])
    

def getFromQueue():
    data = []
    
    with open("queue.csv","r") as f:
        spamreaderspamwriter = csv.reader(f, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        data = list(spamreader)
    
    return data
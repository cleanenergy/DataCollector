import requests
import json
import ast
import csv
from datetime import datetime, timedelta


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
    
    fileName = getFileName()
    data = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    kwh = 0
    
    try:
        f = open(fileName, 'r')
    except IOError:
        fileName = getFileName(delta=1)
        f = open(fileName, 'r')
        spamreader = csv.reader(f, delimiter=";", quotechar="|")
        try:
            data = list(spamreader)
            lastRow = data[-1]
            timestamp = lastRow[0]
            kwh = lastRow[1]
        except:
            print("Error reading file")

        f.close()
        
        fileName = getFileName()
        f = open(fileName, 'w')
        f.close
        writeToFile(timestamp, kwh)
        fileName = getFileName()
        f = open(fileName, 'r')

    spamreader = csv.reader(f, delimiter=";", quotechar="|")

    try:
        data = list(spamreader)
        lastRow = data[-1]
        timestamp = lastRow[0]
        kwh = lastRow[1]
    except:
        print("Error reading file")

    f.close()

    return timestamp, kwh


def writeToFile(timestamp, kwh):
    
    fileName = getFileName()
    
    with open(fileName,"a") as f:
        spamwriter = csv.writer(f, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([timestamp, kwh])


def addToQueue(timestamp, kwh):

    with open("./data/queue.csv","a") as f:
        spamwriter = csv.writer(f, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([timestamp, kwh])
    

def getFromQueue():
    data = []
    
    try:
        f = open("./data/queue.csv","r")
        spamreaderspamwriter = csv.reader(f, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        data = list(spamreader)
        f.close
    except IOError:
        print("There is no queue file")
    
    return data


def getFileName(delta=0):
    date = datetime.today() - timedelta(days=delta)
    fileName = "./data/" + date.strftime("%Y%m%d") + ".csv"
    return fileName
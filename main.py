import DAL
import SPL
import json
from time import sleep

def main():
    
    SPL.configurePi()

    while(1):
        try:
            config = json.load(open("config.json"))
            fs = config["sensor"]["fs"]
        except:
            print("Error reading configurations")
        
        sleep(fs)
        timestamp, kwh = DAL.readFromFile()
        result = DAL.sendData(timestamp, kwh)
        try:
            print(result["status"])
        except:
            print("Error sending data")
            

    
if __name__ == "__main__":
    main()
    
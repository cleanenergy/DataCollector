import DAL
import SPL
from time import sleep

def main():
    
    config = json.load(open("config.json"))
    fs = config["sensor"]["fs"]
    
    SPL.configurePi()

    while(1):
        
        sleep(fs)
        timestamp, kwh = DAL.readFromFile()
        result = DAL.sendData(timestamp, kwh)
        try:
            print(result["status"])
        except:
            print("Error sending data")
            

    
if __name__ == "__main__":
    main()
    
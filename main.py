import DAL
import SPL
from time import sleep

def main():
    
    SPL.configurePi()

    while(1):
        
        sleep(60)
        timestamp, kwh = DAL.readFromFile()
        result = DAL.sendData(timestamp, kwh)
        try:
            print(result["status"])
        except:
            print("Error sending data")
            

    
if __name__ == "__main__":
    main()
    
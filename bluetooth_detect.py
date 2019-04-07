#Author: s3634919 Renning Liu
from monitorAndNotify import Sending
import logging, time, os, json
import bluetooth
from sense_hat import SenseHat

"""search the bluetooth around, if exist, record it to the log file and show the message about temp and humidity
if the temp and humidity is in the range"""
def search():
    while True:
        dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
        print("\nCurrently: {}".format(dt))
        time.sleep(3) 
        nearby_devices = bluetooth.discover_devices()

        root_path = os.path.dirname(os.path.abspath(__file__))
        logging.basicConfig(filename="{}.log".format(os.path.join(root_path,"Log_File/Bluetooth")),level=logging.INFO)
        json_path = os.path.join(root_path,"config.json")
        with open(json_path,'r') as fp:
            data = json.load(fp)

        for mac_address in nearby_devices:
            if mac_address is not None:
                sense = SenseHat()
                print("Hi! Your phone has the MAC address: {}".format(mac_address))
                logging.info("Find MAC address: {}".format(mac_address))
                sense.show_message("Hi! Your phone has the MAC address: {}".format(mac_address))
                send = Sending()
                tim,temp,hum,press=send.getSenseHatData()
                if temp > data['min_temprature'] and temp < data['max_temprature']:
                    if hum > data['min_humidity'] and hum < data['max_humidity']:
                        print("Hi! Current time is {}, temparature is {}*c, humidity is {}, pressure is {}".format(tim,temp,hum,press))
                        sense.show_message("Hi! Current time is {}, temparature is {}*c, humidity is {}, pressure is {}".format(tim,temp,hum,press), scroll_speed=0.05)
                time.sleep(1)
        else:
            logging.info("Could not find target device nearby...")
            print("Could not find target device nearby...")
            sense.show_message("Could not find target device nearby...")
            


if __name__ == "__main__":
    search()
import sys
import csv
import paho.mqtt.client as paho
from datetime import datetime



path_to_directory = "/Users/jakehopkins/Downloads/mqtt_test"
filepath = f"{path_to_directory}/data.csv"
client = paho.Client()
print("the filepath is", filepath)

headers="room, time_on, time_off"

def add_headers(file_path, headers): #wipes file, then adds headers for readability, runs once
    with open(file_path, 'w', newline='') as file:
     writer = csv.writer(file)
     writer.writerow([headers])
     print("added data")
add_headers(filepath, headers)

def add_data(file_path, payload): #adds data from esp32
    with open(file_path, 'a', newline='') as file:
     writer = csv.writer(file)
     writer.writerow([payload])
     print("added data")


def message_handling(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"{msg.topic}: {payload}")
    add_data(filepath, payload)

client = paho.Client()
client.on_message = message_handling

if client.connect("192.168.4.75", 1883, 60) != 0:
    print("Couldn't connect to the mqtt broker")
    sys.exit(1)

client.subscribe("esp32/text")








#ends mqtt conection
try:
    print("Press CTRL+C to exit...")
    client.loop_forever()
except Exception:
    print("Caught an Exception, something went wrong...")
finally:
    print("Disconnecting from the MQTT broker")
    client.disconnect()


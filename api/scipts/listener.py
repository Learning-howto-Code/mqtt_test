import sys
import csv
import paho.mqtt.client as paho
from datetime import datetime

path_to_directory = "/Users/jakehopkins/Downloads/mqtt_test"
filepath = f"{path_to_directory}/data.csv"
client = paho.Client()
print("the filepath is", filepath)

headers = "room,time_on,time_off"

# Keep start times outside to remember them between calls
start_times = {}

def add_headers(file_path, headers):  # wipes file, then adds headers
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers.split(','))  # split into columns
        print("added headers")

add_headers(filepath, headers) # calls funtion

def add_row(file_path, room, time_on, time_off): #funtion to add row everytie we get a new sensor input
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([room, time_on, time_off])
        print(f"added row: {room}, {time_on}, {time_off}")

def message_handling(client, userdata, msg):
    payload = msg.payload.decode().strip().lower()
    print(f"{msg.topic}: {payload}")

    parts = payload.split()

    room, status = parts # splits message into room and on/off
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if status == "start":
        start_times[room] = now
        print(f"Recorded start time for {room}: {now}") # if sesnor = on, reocords it to wait untll it turns off.
    elif status == "end": 
        if room in start_times:
            time_on = start_times.pop(room)
            time_off = now
            add_row(filepath, room, time_on, time_off) # once we get end message, adds room start and end tiems to csv
        
client.on_message = message_handling

if client.connect("192.168.4.75", 1883, 60) != 0: # If mqtt sever isn't running on RPi stops code
    print("Couldn't connect to the mqtt broker")
    sys.exit(1)

client.subscribe("esp32/text") #Sets the listenor to the correct "channel"

try:
    print("Press CTRL+C to exit...") #message on how to stop code
    client.loop_forever()
except Exception:
    print("Caught an Exception, something went wrong...") #if code trips error with mqtt, end code
finally:
    print("Disconnecting from the MQTT broker") # Diconnects to mqtt
    client.disconnect()

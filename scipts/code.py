import time
import wifi
import socketpool
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import random

# Wi-Fi credentials
ssid = "LuckySonic"
password = "Luckysmile"

# MQTT broker info
mqtt_server = "192.168.4.75"
mqtt_port = 1883
client_id = "esp32_text_publisher"
topic_pub = "esp32/text"

# Connect to Wi-Fi
print("Connecting to Wi-Fi...")
wifi.radio.connect(ssid, password)
print("Connected to WiFi:", wifi.radio.ipv4_address)

# Create socket pool
pool = socketpool.SocketPool(wifi.radio)

# Create MQTT client (no connector needed)
mqtt_client = MQTT.MQTT(
    broker=mqtt_server,
    port=mqtt_port,
    socket_pool=pool,
    client_id=client_id,
)

print("Connecting to MQTT broker...")
mqtt_client.connect()
print("Connected to MQTT")

# Loop to publish text
while True:
    rooms = ["shower", "bathroom_sink", "kitchen_sink", "Toilet"]
    message = random.choice(rooms) 
    mqtt_client.publish(topic_pub, message + " start")
    print("Published:", message + " start")
    time.sleep(random.randrange(5))
    mqtt_client.publish(topic_pub, message + " end")
    print("Published:", message+" start")
    time.sleep(1)
    
        


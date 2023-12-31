import grovepi
import time
import sys
import paho.mqtt.client as mqtt
import socket


broker_address = "eclipse.usc.edu"
port = 1883
topic = "sensor/data"
range_val = 5

def read_sensor_data():
    return grovepi.ultrasonicRead(ultrasonic_ranger)
    
# Create a MQTT client
client = mqtt.Client()

# Connect to the broker
time.sleep(5) 
client.connect(host="test.mosquitto.org", port=1883, keepalive=60)

# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
ultrasonic_ranger = 4
button_port = 3

grovepi.pinMode(button_port, "INPUT")

while True:
    try:
        # Read distance value from Ultrasonic
        if(grovepi.digitalRead(button_port)):
        	time.sleep(0.1)
        	range_val = read_sensor_data()
        	time.sleep(0.1)
        	client.publish(topic, payload=str(range_val), qos=0)
        	time.sleep(0.1)
        	print(range_val)
    except Exception as e:
        print ("Error:{}".format(e))
    
    time.sleep(0.1) # don't overload the i2c bus


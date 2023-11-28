import grovepi
import time
import sys
import paho.mqtt.publish as publish

MQTT_SERVER = "192.168.64.5"
MQTT_PATH = "dist"

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
        	range_val = grovepi.ultrasonicRead(ultrasonic_ranger)
        	time.sleep(0.1)
        	print(range_val)
        	publish.single(MQTT_PATH, range_val, hostname=MQTT_SERVER)
    except Exception as e:
        print ("Error:{}".format(e))
    
    time.sleep(0.1) # don't overload the i2c bus


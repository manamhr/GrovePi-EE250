import sys
"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
sys.path.append('../../Software/Python/')
import grovepi
from grovepi import *
from grove_rgb_lcd import *

global led, ultraSonic, button
led=3
ultraSonic=4
button=7

grovepi.pinMode(button, "INPUT")
grovepi.pinMode(led, "OUTPUT")

def on_connect(client, userdata, flags, rc):
	print("Connected to server/broker with result code "+str(rc))
	client.subscribe("anrg-pi6/led")
	client.message_callback_add("anrg-pi6/led", callback_led)
	client.subscribe("anrg-pi6/lcd")
	client.message_callback_add("anrg-pi6/lcd", callback_lcd)
    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
	print("On message: " + msg.topic + " " + str(msg.payload, "utf-8")) #changed this

def callback_led(client, userdata, msg):
	print("callback_led:" + msg.topic + " " + str(msg.payload, "utf-8"))
	
	data = str(msg.payload, "utf-8")
	
	if (data == "LED_ON"):
		digitalWrite(3 ,1)
		print("LED on")
		time.sleep(1)

	elif(data == "LED_OFF"):
		digitalWrite(3 ,0)
		print("LED off")
		time.sleep(1)

	print("test2")

def callback_lcd(client, userdata,msg):
	setText(str(msg.payload, "utf-8"))

if __name__ == '__main__':
	#this section is covered in publisher_and_subscriber_example.py
	client = mqtt.Client()
	client.on_message = on_message
	client.on_connect = on_connect
	client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
	client.loop_start()
	
	setRGB(0,0,255)
	
	while True:
		
		if (grovepi.digitalRead(button)>0):
			client.publish("anrg-pi6/button", "Button pressed!")
			print("Button Pressed!")

		client.publish("anrg-pi6/ultrasonicRanger", grovepi.ultrasonicRead(4))
		print(grovepi.ultrasonicRead(4))
		time.sleep(1) #timer           


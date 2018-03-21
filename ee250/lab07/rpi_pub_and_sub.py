"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
from pynput import keyboard
from grovepi import *
import groverpi
from grove_rpg_lcd import *

led=3

#ultraSonic=4
button=5

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    grovepi.pinMode(button, "Press a button")
    client.subscribe("anrg-pi6/led")
    client.msg_callback("aneg-pi6/led", callback_led)
    client.subscribe("anrg-pi6/lcd")
    client.msg_callback("anrg-pi6/lcd", callback_lcd)
    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload))

def callback_led(client,userdata, msg):
	if ("LED_ON" in str(msg.payload)):
		try:
			digitalWrite(led,1)
	        print("callback_led:"+msg.topic+" " +std(msg.payload))
        	print("callback_led:msg.payload  has a type of : " + str(type(msg.payload)))

	elif("LED_OFF" in str(msg.payload)):
		try: 
			digitalWrite(led,0)
	        print("callback_led:" +msg.topic+" " +str(msg.payload))
        	print ("callback_led: msg.payload has a type of : " + str(type(msg.payload)))

def callback_lcd(client, userdata,msg):
	setText(str(msg.payload))
def on_press(key):
if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        
	if (grovepi.digitalRead(button)>0):
		client.publish("anrg-pi6/button", "Button pressed!")
		setText("Button Pressed!")

	        time.sleep(1)
            


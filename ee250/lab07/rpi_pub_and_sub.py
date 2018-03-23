import sys
"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

#import socket
import paho.mqtt.client as mqtt
#import RPi.GPIO as GPIO
import time
sys.path.append('../../Software/Python/')
import grovepi
#from grovepi import *
from grove_rgb_lcd import *

global led, ultraSonic, button
led=3
ultraSonic=4
button=7
lcd=8

def on_connect(client, userdata, flags, rc):
	print("Connected to server/broker with result code "+str(rc))
	grovepi.pinMode(button, "INPUT") #button is an input
	client.subscribe("anrg-pi6/led")
	#client.msg_callback("anrg-pi6/led", callback_led)
	client.subscribe("anrg-pi6/lcd")
	#client.msg_callback("anrg-pi6/lcd", callback_lcd)
    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
	print("On message: " + msg.topic + " " + str(msg.payload, "utf-8")) #changed this

def callback_led(client, userdata, msg):
	print("test")
	if ("LED_ON" in str(msg.payload, "utf-8")):
		#try:
		digitalWrite(3 ,1)
		print("LED on")
			#print("callback_led:" + msg.topic + " " + str(msg.payload,"utf-8"))
			#print("callback_led:msg.payload  has a type of : " + str(type(msg.payload, "utf-8")))
			#print("callback_led:"+msg.topic+" " +str(msg.payload, "utf-8"))
			#print("callback_led:msg.payload has a type of : " + str(type(msg.payload, "utf-8")))
		#except IOError:
		#	print("You have an Error!!")

	elif("LED_OFF" in str(msg.payload, "utf-8")):
		#try:
		digitalWrite(3 ,0)
		print("LED off")
			#print("callback_led:" + msg.topic + " " + str(msg.payload, "utf-8"))
			#print("callback_led: msg.payload has a type of : " + str(type(msg.payload, "utf-8")))
			#print("callback_led:" +msg.topic+" " +str(msg.payload, "utf-8"))
			#print("callback_led: msg.payload has a type of : " + str(type(msg.payload, "utf-8")))
		#except IOError:
		#	print("You have an Error!!")
			
	client.message_callback_add("anrg-pi6/led", callback_led)
	print("test2")
	print("callback_led:" + msg.topic + " " + str(msg.payload, "utf-8"))
	print("callback_led: msg.payload has a type of : " + str(type(msg.payload, "utf-8")))

def callback_lcd(client, userdata,msg):
	setText(str(msg.payload, "utf-8"))


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
			print("Button Pressed!")

		client.publish("anrg-pi6/ultrasonicRanger", grovepi.ultrasonicRead(4))
		print(grovepi.ultrasonicRead(4))
		time.sleep(1) #timer           


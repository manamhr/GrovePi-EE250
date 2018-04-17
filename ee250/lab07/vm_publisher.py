"""EE 250L Lab 07 Skeleton Code

Run vm_publisher.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
import grovepi

#from pynput import keyboard
from grovepi import *
from grove_rgb_lcd import *

#added

dht_sensor_port = 7
lcd = 8
led=4
#check to call ports, edit message
def on_connect(client, userdata, flags, rc):
	print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
	print("on_message: " + msg.topic + " " + str(msg.payload))
	
def callback_led(client, userdata, msg):
	print("callback_led:" + msg.topic + " " + str(msg.payload, "utf-8"))
	print("callback_led: msg.payload has a type of : " + str(type(msg.payload, "utf-8")))
	client.publish("anrg-pi6/messages", lcd) #added
def on_press_LED(LED_toggle):
	
		client.publish("anrg-pi6/led", "LED_toggle")
		
# do sth for messages
if __name__ == '__main__':
    #setup the keyboard event listener
	#lis = keyboard.Listener(on_press=on_press)
	lis.start() # start to listen on a separate thread

    #this section is covered in publisher_and_subscriber_example.py
	client = mqtt.Client()
	client.on_message = on_message
	client.on_connect = on_connect
	client.callback_led = callback_led #added
	client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
	client.loop_start()

	while True:
		try: #added
			[temp, hum] = dht(dht_sensor_port,1) #get temp and hum
			#print "temp=", temp, "C\thumadity =", hum, "%" 
			client.publish("anrg-pi6/temperature", temp)
			client.publish("anrg-pi6/humidity", hum)
			t = str(temp)
			h = str(hum)

			setRGB(0,128,64)
			setRGB(0,255,0)
			setText("Temp:" +t+ "C      " + "Humidity: "  + h + "%")

		except (IOError,TypeError) as e:
			print ("Error")





		time.sleep(1)
            


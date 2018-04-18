import paho.mqtt.client as mqtt
import time
import grovepi
from grovepi import *
from grove_rgb_lcd import *

global led, dhtPIN
led = 3
dhtPIN = 7

grovepi.pinMode(led, "OUTPUT")

def led_callback(client, userdata, message):
	if (str(message.payload, "utf-8") == "LED_toggle"):
		if (digitalRead(led) == 1):
			digitalWrite(led, 0)
		elif(digitalRead(led) == 0):
			digitalWrite(led, 1)

def lcd_callback(client, userdata, message):
	setText(str(message.payload, "utf-8"))

def on_connect(client, userdata, flags, rc):
	print("Connected to server (i.e., broker) with result code "+str(rc))

	client.subscribe("anrg-pi6/led")
	client.message_callback_add("anrg-pi6/led", led_callback)
	print("Connected to LED")

	client.subscribe("anrg-pi6/lcd")
	client.message_callback_add("anrg-pi6/lcd", lcd_callback)
	print("Connected to LCD")

def on_message(client, userdata, msg):
	print("on_message: " + msg.topic + " " + str(msg.payload))

if __name__ == '__main__':
	client = mqtt.Client()
	client.on_message = on_message
	client.on_connect = on_connect
	client.connect(host = "eclipse.usc.edu", port = 11000, keepalive = 60)
	client.loop_start()
	pinMode(led, "OUTPUT")
	time.sleep(1)
	setRGB(0,0,255)

	while True:
		[temp, hum] = dht(dhtPIN, 1)

		client.publish("anrg-pi6/temperature", str(temp))
		client.publish("anrg-pi6/humidity", str(hum))
		time.sleep(1)

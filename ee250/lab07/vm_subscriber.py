"""EE 250L Lab 07 Skeleton Code

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time

ultrasonic = " "

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    
    client.subscribe("anrg-pi6/unltrasonicRanger")
    client.message_callback_add("anrg-pi6/ultrasonicRanger", custom_callback_ultrasonic)
    client.subscribe("anrg-pi6/button")
    client.message_callback_add("anrg-pi6/button", custom_callback_button)
                                
    #subscribe to the ultrasonic ranger topic here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload))
                                
def custom_callback_ultrasonic(client, userdata, message):
    #ultrasonic = str(message.payload, "utf-8")
    print("custom_callback_ultrasonic: " + message.topic + " " + str(message.payload, "utf-8"))
    print("custom_callback_ultrasonic: message.payload is type " + str(type(message.payload)))
                                
def custom_callback_button(client, userdata, message):
    print(str(message.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    
    while True:
        True
        #print(str(ultrasonic))
        #time.sleep(1)    


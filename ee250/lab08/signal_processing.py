

import requests
import json
from datetime import datetime
import paho.mqtt.client as mqtt
import time

# MQTT variables
broker_hostname = "eclipse.usc.edu"
broker_port = 11000
ultrasonic_ranger1_topic = "ultrasonic_ranger1"
ultrasonic_ranger2_topic = "ultrasonic_ranger2"

# Lists holding the ultrasonic ranger sensor distance readings. Change the 
# value of MAX_LIST_LENGTH depending on how many distance samples you would 
# like to keep at any point in time.
MAX_LIST_LENGTH = 100
ranger1_dist = []
ranger2_dist = []

def ranger1_callback(client, userdata, msg):
    global ranger1_dist
    if(int(msg.payload) <= 125):
        ranger1_dist.append(int(msg.payload))
        #truncate list to only have the last MAX_LIST_LENGTH values
    else:
        ranger1_dist.append(125)
    ranger1_dist = ranger1_dist[-MAX_LIST_LENGTH:]


def ranger2_callback(client, userdata, msg):
    global ranger2_dist
    if(int(msg.payload) <= 125):
        ranger2_dist.append(int(msg.payload))
        #truncate list to only have the last MAX_LIST_LENGTH values
    else:
        ranger2_dist.append(125)
    ranger2_dist = ranger2_dist[-MAX_LIST_LENGTH:]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(ultrasonic_ranger1_topic)
    client.message_callback_add(ultrasonic_ranger1_topic, ranger1_callback)
    client.subscribe(ultrasonic_ranger2_topic)
    client.message_callback_add(ultrasonic_ranger2_topic, ranger2_callback)

# The callback for when a PUBLISH message is received from the server.
# This should not be called.
def on_message(client, userdata, msg): 
    print(msg.topic + " " + str(msg.payload))

def move_index_left(array):
    for i in range(0, len(array) - 1):
        array[i] = array[i+1]

def average(array, grab):
    sum = 0
    if(len(array) > grab):
        for i in range(len(array) - grab, len(array)):
            sum = sum + array[i]
        return sum/grab
    else:
        return 0

def printlol(array):
    for i in range(0, len(array)):
        print(array[i])


def moving_avg_buffer(mab, array, grab):
    move_index_left(mab)
    average_array = average(array, grab)
    mab[len(mab) - 1] = average_array

def difference(diff_array, dist_array):
    move_index_left(diff_array)

    #added this, now numbers are shit lol
    #created bc problems if diff array is smaller than dist_array
    #for now, try to make them the same, use mab
    size = len(dist_array)
    if(size > len(diff_array)):
        size = len(diff_array)


    for i in range(0,size-1):
        array_difference = dist_array[i+1] - dist_array[i]
        if(abs(array_difference) < 0.5):
            diff_array[i] = 0
        else:
            diff_array[i] = array_difference

def location(mab1, mab2, small, big):

    #LEFT
    #small = 25?
    #tlarge = 100?
    if( (mab1[len(mab1)-1] <= small) & (mab2[len(mab2)-1] >= big) ):
        return "Still-Left"
    elif( (mab1[len(mab1)-1] >= big) & (mab2[len(mab2)-1] <= small) ):
        return "Still-Right"
    elif( (mab1[len(mab1)-1] <= big) & (mab2[len(mab2)-1] <= big) ):
        return "Still-Middle"
    else:
        return "bad :((("


#USE def location to help with the values.
#JDI;SFHS;AOFGHIEWARIUGH;PFAEIOWHNFG;WIQFHKBWER;IFGHEWA;IFGEWA;FUAEWGHFPEORWA;HFGAW;OIAEHRLFGIEWAUGBFLWAIFGUHAERIGHKRWA;
def movement(diff1, diff2):
    if( (abs(diff1[len(diff1)-1]) < 2) & (abs(diff2[len(diff2)-1]) < 2) ):
        return "no move"

    elif( (diff1[len(diff1)-1] > 3) & (diff2[len(diff2)-1] < -3) ):
        return "Moving Right"
    elif( (diff2[len(diff2)-1] > 3) & (diff1[len(diff1)-1] < -3) ):
        return "Moving Left"

    elif( (diff1[len(diff1)-1] > 3) ):
        return "Moving Right"
    elif( (diff2[len(diff2)-1] > 3) ):
        return "Moving Left"

    elif( (diff1[len(diff1)-1] < -3) ):
        return "Moving Left"
    elif( (diff2[len(diff2)-1] < -3) ):
        return "Moving Right"

    else:
        return "garbo values"


if __name__ == '__main__':
    # Connect to broker and start loop    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_hostname, broker_port, 60)
    client.loop_start()

    mab1=[0,0,0,0,0,0,0,0,0,0]
    diff1=[0,0,0,0,0,0,0,0,0,0]
    diff_mab1=[0,0,0,0,0,0,0,0,0,0]

    mab2=[0,0,0,0,0,0,0,0,0,0]
    diff2=[0,0,0,0,0,0,0,0,0,0]
    diff_mab2=[0,0,0,0,0,0,0,0,0,0]
    #flask
    hdr = {
        'Content-Type': 'application/json',
        'Authorization': None
    }
    #flask
    payload = {
        'time': str(datetime.now()),
        'event': movement(diff1, diff2)
    }

    while True:
        """ You have two lists, ranger1_dist and ranger2_dist, which hold a window
        of the past MAX_LIST_LENGTH samples published by ultrasonic ranger 1
        and 2, respectively. The signals are published roughly at intervals of
        200ms, or 5 samples/second (5 Hz). The values published are the 
        distances in centimeters to the closest object. Expect values between 
        0 and 512. However, these rangers do not detect people well beyond 
        ~125cm. """
        
        # TODO: detect movement and/or position
        
        

        print("dist: " + str(ranger1_dist[-1:]) + " " + str(ranger2_dist[-1:]))
        
        #MAB
        moving_avg_buffer(mab1, ranger1_dist, 5)
        moving_avg_buffer(mab2, ranger2_dist, 5)
        print("MAB:     " + str(mab1[len(mab1)-1]) + " " + str(mab2[len(mab2)-1]))

        
        
        
        #Difference:
        difference(diff1, mab1)
        difference(diff2, mab2)
        print("Diff:    " + '%.1f' % diff1[8] + " " + '%.1f' % diff2[8])
        
       

        #Difference MAB
        moving_avg_buffer(diff_mab1, diff1, 6)
        moving_avg_buffer(diff_mab2, diff2, 6)
        print("MAB Diff: " + '%.1f' % diff_mab1[len(diff_mab1)-1] + " " + '%.1f' % diff_mab2[len(diff_mab2)-1])


        print( location(mab1, mab2, 40, 110) )
        print( movement(diff_mab1, diff_mab2) )
        print()

        #flask
        response = requests.post("http://0.0.0.0:5000/post-event", headers = hdr, data = json.dumps(payload))
        #flask
        print (response.json())
        
        
        time.sleep(0.2)
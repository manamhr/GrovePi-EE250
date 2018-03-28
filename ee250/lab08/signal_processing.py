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
    ranger1_dist.append(int(msg.payload))
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger1_dist = ranger1_dist[-MAX_LIST_LENGTH:]

def ranger2_callback(client, userdata, msg):
    global ranger2_dist
    ranger2_dist.append(int(msg.payload))
    #truncate list to only have the last MAX_LIST_LENGTH values
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

if __name__ == '__main__':
    # Connect to broker and start loop    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_hostname, broker_port, 60)
    client.loop_start()

    mab=[0,0,0,0,0,0,0,0,0,0]
    diff=[0,0,0,0,0,0,0,0,0,0]

    while True:
        """ You have two lists, ranger1_dist and ranger2_dist, which hold a window
        of the past MAX_LIST_LENGTH samples published by ultrasonic ranger 1
        and 2, respectively. The signals are published roughly at intervals of
        200ms, or 5 samples/second (5 Hz). The values published are the 
        distances in centimeters to the closest object. Expect values between 
        0 and 512. However, these rangers do not detect people well beyond 
        ~125cm. """
        
        # TODO: detect movement and/or position
        
        
        print("ranger1: " + str(ranger1_dist[-1:]))#s + ", ranger2: ")
        #print(len(ranger1_dist))
        moving_avg_buffer(mab, ranger1_dist, 10)
        #print(mab[len(mab)-1])
        ranger_one = ranger1_dist[-1:]
        difference(diff, mab)
        print('%.1f' % diff[8])
        str(ranger1_dist[-1:])

        print()
        
        time.sleep(0.2)
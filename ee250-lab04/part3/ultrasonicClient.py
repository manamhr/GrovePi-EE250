import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `from grovepi import *`
sys.path.append('../../Software/Python/')

from grovepi import *

#use UDP

import time
#from grovepi import *

#from grovepi import *

def Main():
   	host = '192.168.1.237'
   	port = 1024
	server_addr = '192.168.1.237'



   	s = socket.socket()
	s.connect((host,port))

	ultrasonic_range =4
	while true:
		try:
		print(grovepi.ultrasonicRead(unltrasonic_range))

	


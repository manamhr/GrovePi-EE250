import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `from grovepi import *`
sys.path.append('../../Software/Python/')

from grovepi import *

#use UDP
import socket

def Main():
	host = '127.0.0.1'
	port = 5000

	s=socket.socket()
	s.connect((host,port))

	message = input 

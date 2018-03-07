import sys
# By appending the folder of all the GrovePi libraries to the system path here,
<<<<<<< HEAD:ee250-lab04/part3/ledServer.py
# we are successfully `from grovepi import *`
#sys.path.append('../../Software/Python/')



#import sys
import socket
#sys.path.append('../../Software/Python/')

import time
#from grovepi import *

#from grovepi import *

led = 3

def Main():
	host = '192.168.1.237'
	port = 5000
	server_addr='192.168.1.237'
	s = socket.socket()
	s.bind((host,port))

	s.listen(1)
	c, addr = s.accept()
	print("Connection")

	while True:
		#data = c.recv(1024).decode('utf-8')
		#execfile('../../Software/Python/grove_led_blink.py')
		data = c.recv(1024).decode('utf-8')
		if data == "LED_ON":
			try:
				digitalWrite(led, 1)
				data = "LED on"
				#time.sleep(1)

		elif data == "LED_OFF":
			try:
				digitalWrite(led, 0)
				print("LED off")
				#time.sleep(1)
=======
# we are successfully `import grovepi`
sys.path.append('../../../Software/Python/')
>>>>>>> upstream/sp18-master:ee250/lab04/part3/ledServer.py

		c.send(data.encode('utf-8'))
	c.close()

if __name__ == '__main__':
	Main()

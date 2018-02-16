import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `from grovepi import *`
#sys.path.append('../../Software/Python/')



#import sys
import socket
#sys.path.append('../../Software/Python/')

import time
#from grovepi import *

#from grovepi import *

def Main():
    host = '192.168.1.237'
    port = 1024
    server_addr = '192.168.1.237'

    s = socket.socket()
    s.connect((host,port))

   message = input("->")

    while message != 'q'
    s.send (message.encode('utf-8')
        #data = c.recv(1024).decode('utf-8')
        #execfile('../../Software/Python/grove_led_blink.py')
        data = c.recv(1024).decode('utf-8')
        message = input("->")
        
    s.close()

if __name__ == '__main__':
    Main()

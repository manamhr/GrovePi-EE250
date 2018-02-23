import socket
import sys

sys.path.append('../../Software/Python/')


import grovepi
def Main():
    # Change the host and port as needed. For ports, use a number in the 9000 
    # range. 
	host = '192.168.1.112'
	port = 8000
	ultrasonic_ranger = 4


	server_addr = '192.168.1.235'

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host,port))

    # UDP is connectionless, so a client does not formally connect to a server
    # before sending a message.
	dst_port = input("destination port-> ")
	#message = input("message-> ")
	while True:
        #tuples are immutable so we need to overwrite the last tuple
		server = (server_addr, int(dst_port))

        # for UDP, sendto() and recvfrom() are used instead
		message = str(grovepi.ultrasonicRead(ultrasonic_ranger))
		print(message)
		s.sendto(message.encode('utf-8'), server)

	s.close()

if __name__ == '__main__':
	Main()

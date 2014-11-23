#!/usr/bin/python2
from bluetooth import *
import uuid

UUID = "841eba55-800a-48eb-9e39-335265d8d23f"
SERVICE_NAME = "SIRS"

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))

print str(server_sock.getpeername())

server_sock.listen(1)

port = server_sock.getsockname()[1]


advertise_service( server_sock, SERVICE_NAME,
                   service_id = UUID,
                   service_classes = [ UUID, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ])
          

while True: 
	print "Waiting for connection on RFCOMM channel %d" % port
	client_sock, client_info = server_sock.accept()
	print "Accepted connection from ", client_info

	try:
	    while True:
			print "Waiting for new messages..."
			data = client_sock.recv(1024)
			if len(data) != 0: 
				print "received [%s]" % data
			client_sock.send("Pong")
	except IOError:
	    pass

	print "disconnected"
	client_sock.close()

server_sock.close()
print "all done"

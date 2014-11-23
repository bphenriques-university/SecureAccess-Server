#!/usr/bin/python2
# -*- coding: UTF-8 -*-

from bluetooth import *
from AbstractServerState import ServerState
from SecurityScripts.DiffieHellman import *

#State machine
class ServerApplication():

	def __init__(self):
		self._UUID = "841eba55-800a-48eb-9e39-335265d8d23f"
		self._SERVICE_NAME = "SIRS"
		self._client_sock = None
		self._server_sock = None
				
		#The initial state is Start
		self._server_state = StartState()
	
	def getClientSocket(self):
		return self._client_sock
		
	def setClientSocket(self, client_socket):
		self._client_sock = client_socket
		
	def getServerSocket(self):
		return self._client_sock
		
	def setServerSocket(self, client_socket):
		self._client_sock = client_socket
	
	def start(self):
		try:
			while True:
				self._server_state.handle(self)
				#raw_input("Press any key to continue...")
		except Exception as e:
			print "[ERROR IN APPLICATION] - %s" % str(e)
			
			if self._client_sock is not None:
				self._client_sock.close()
			if self._server_sock is not None:
				self._server_sock.close()
			
			return -1

#
#	Server advertises service
#
class StartState(ServerState):

	def __init__(self):
		ServerState.__init__(self)

	def handle(self, server_instance):
		
		server_instance.setServerSocket(BluetoothSocket(RFCOMM))
		s_socket = server_instance.getServerSocket();		
		
		s_socket.bind(("",PORT_ANY))
		print str(s_socket.getpeername())
		s_socket.listen(1)
		
		port = s_socket.getsockname()[1]
		UUID = server_instance._UUID
		SERVICE_NAME = server_instance._SERVICE_NAME
		
		advertise_service(	s_socket, SERVICE_NAME,
							service_id = UUID,
							service_classes = [ UUID, SERIAL_PORT_CLASS ],
							profiles = [ SERIAL_PORT_PROFILE ])

		print "#################################"
		print "##### Advertised Service:    ####" 
		print "#"
		print "# UUID: %s" % UUID
		print "# Name: %s" % SERVICE_NAME
		print "# Port: %s" % port
		print "#"
		print "#################################"
		
		#work to be done here
		server_instance._server_state = IdleState(port)

#
#	Server waits for new connections
#

class IdleState(ServerState):
	def __init__(self, port):
		ServerState.__init__(self)
		self.__port = port

	def handle(self, server_instance):
		
		s_socket = server_instance.getServerSocket();
		
		print "Waiting for connection"
		client_sock, client_info = s_socket.accept()
		
		server_instance.setClientSocket(client_sock)
		print "Accepted connection from ", client_info
		
		#work to be done here
		server_instance._server_state = StartConnectionState()
		
#
#	Server waits for new connections
#

class StartConnectionState(ServerState):
	def __init__(self):
		ServerState.__init__(self)
		self.__expectedCommand = "CONN"
		self.__base = None
		self.__prime = None
		self.__yDevice = None

	def parse_data(self, data):
		# arguments are separated by '#'
		if len(data) == 0:
			return False
			
		if len(data) != 0: 
			data_to_parse = str(data)
			data_to_parse = data_to_parse.split("#")
			command = data_to_parse[0]
			if command == self.__expectedCommand and len(data_to_parse) == 4:
				self.__base = long(data_to_parse[1])
				self.__prime = long(data_to_parse[2])
				self.__yDevice = long(data_to_parse[3])
			else:
				return False
		
		return True

	def handle(self, server_instance):
		s_socket = server_instance.getServerSocket();
		c_socket = server_instance.getClientSocket();
		
		print "Waiting for diffie-hellman-keys"
		data = c_socket.recv(1024)
		if self.parse_data(data):
			print "######## Start of connection ########"
			print "# Base: %s"  % self.__base
			print "# Prime: %s"  % self.__prime
			print "# yDevice: %s"  % self.__yDevice
		else:
			print "Bad Start of connection"	
			
		print "#"
		
		dh = DiffieHellman(p = self.__prime, g = self.__base)
		
		dh.generateKey(self.__yDevice)
		print "# Session Key: %s"  % str(dh.getKey())
		
		msg_to_send = "CONN-R#" + str(dh.getPublicKey())
		c_socket.send(msg_to_send)
		
		#loop in this state
		server_instance._server_state = StartConnectionState()

class PingPongState(ServerState):
	def __init__(self):
		ServerState.__init__(self)

	def handle(self, server_instance):
		s_socket = server_instance.getServerSocket();
		c_socket = server_instance.getClientSocket();
		
		print "Waiting for new messages..."
		data = c_socket.recv(1024)
		if len(data) != 0: 
			print "received [%s]" % data
		c_socket.send("Pong")
		
		#loop in this state
		server_instance._server_state = PingPongState()


if __name__ == "__main__":
	bm = ServerApplication()
	bm.start()

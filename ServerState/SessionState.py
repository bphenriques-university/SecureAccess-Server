#!/usr/bin/python2
# -*- coding: UTF-8 -*-

from AbstractSessionState import AbstractSessionState

#State machine MANAGER
class Session():
	def __init__(self, client_id, client_sock):
		self._client_id = client_id
		self._client_sock = client_sock		
		#The initial state is Start
		self._session_state = StartState()
	
	def getClientSocket(self):
		return self._client_sock

	def getClientId(self):
		return self._client_id

	def setNextState(self, new_state):
		self._session_state = new_state

	def start(self):
		try:
			while True:
				self._session_state.handle(self)
				#raw_input("Press any key to continue...")
		except Exception as e:
			print "[SESSION ERROR] - %s" % str(e)
			if self._client_sock is not None:
				self._client_sock.close()
			return -1

#
#	Authentication State
#
class StartState(AbstractSessionState):
	def __init__(self):
		AbstractSessionState.__init__(self)

	def handle(self, session_manager):
		print ("[" + str(session_manager.getClientId()) + "] - Start State: Waiting for CONNECT MESSAGE")
		
		#work to be done here
		session_manager.setNextState(EchoReplyState())

#
#	Server waits for new connections
#

class EchoReplyState(AbstractSessionState):
	def __init__(self):
		AbstractSessionState.__init__(self)

	def handle(self, session_manager):
		print ("[" + str(session_manager.getClientId()) + "] - Start State: Waiting for CONNECT MESSAGE")		
		c_socket = session_manager.getClientSocket();
		session_manager.setNextState(EchoReplyState())
			
	
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
#data = c_socket.recv(1024)
#c_socket.send(msg_to_send)

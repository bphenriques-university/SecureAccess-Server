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
		self._is_interrupted = False
	
	def getClientSocket(self):
		return self._client_sock

	def getClientId(self):
		return self._client_id

	def setNextState(self, new_state):
		self._session_state = new_state

	def interrupt(self):
		self._is_interrupted = True

	def log(self, msg):
		print ("[" + str(self._client_id) + "] - " + msg)

	def start(self):
		try:
			while not self._is_interrupted:
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
		self.__COMMAND = "CONN"
		self.__challenge = None

	def parse_data(self, data):
		# arguments are separated by '#'
		if len(data) == 0:
			return False
			
		if len(data) != 0: 
			data_to_parse = str(data)
			data_to_parse = data_to_parse.split("#")
			command = data_to_parse[0]
			if command == self.__COMMAND and len(data_to_parse) == 2:
				self.__challenge = int(data_to_parse[1])
			else:
				return False

		return True

	def handle(self, session_manager):
		session_manager.log("Start State: Waiting for CONNECT MESSAGE")
		c_socket = session_manager.getClientSocket();

		data = c_socket.recv(1024)
		session_manager.log("Start State: Received: " + str(data))
	
		if not self.parse_data(data):
			raise Exception("Bad input from client, aborting session")		


		session_manager.log("Start State: Challenge number is: " + str(self.__challenge))
		challenge = self.__challenge
		challenge = challenge - 1

		key = "WWW.OSOCRATESAINDAESTAPRESO.COM"

		response = "CONN_RESPONSE#" + key + "#" + str(challenge)
		
		c_socket.send(response)
			
		#work to be done here
		session_manager.setNextState(EchoReplyState())

#
#	Server waits for new connections
#

class EchoReplyState(AbstractSessionState):
	def __init__(self):
		AbstractSessionState.__init__(self)

	def handle(self, session_manager):
		#session_manager.log("EchoReplyState: Pinging client...")		
		c_socket = session_manager.getClientSocket();
		session_manager.setNextState(EchoReplyState())

	
#data = c_socket.recv(1024)
#c_socket.send(msg_to_send)

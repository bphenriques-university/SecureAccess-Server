#!/usr/bin/python2
# -*- coding: UTF-8 -*-

import sys, time
from random import *
from AbstractSessionState import AbstractSessionState

#State machine MANAGER
class Session():
	def __init__(self, application, client_id, client_info, client_sock):
		self._client_id = client_id
		self._client_sock = client_sock		
		#The initial state is Start
		self._session_state = StartState()
		self._is_interrupted = False
		self._client_info = client_info
		self.__APPLICATION = application
	
	def authenticated(self):
		self.log("SIGNED IN")
		self.__APPLICATION.newAuthenticatedUser(self._client_id, self._client_info)

	def loggedOff(self):
		self.log("LOGGED OFF")
		self.__APPLICATION.disconnectUser(self._client_id, self._client_info)

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
			self.loggedOff()
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

	def parse_connect_request(self, data):
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

	def generate_session_key(self):
		return "ab1bn32b31jknmd102ui4bnfsanocm9123"

	def handle(self, session_manager):
		session_manager.log("Waiting for CONNECT MESSAGE")
		c_socket = session_manager.getClientSocket();


		# RECEIVE CONNECTION REQUEST
		data = c_socket.recv(1024)
		session_manager.log("[DEVICE]: " + str(data))
	
		if not self.parse_connect_request(data):
			raise Exception("Bad input from client, aborting session")		

		# ANSWERING CLIENT REQUEST WITH HIS CHALLENGE - 1 AND A NEW CHALLENGE FOR HIM

		key = self.generate_session_key()

		challenge_client = randint(0, 2147483647)
		response = "CONN_RESPONSE#" + key + "#" + str(self.__challenge-1) + "#" + str(challenge_client)

		session_manager.log("[SERVER]: " + str(response))		
		c_socket.send(response)


		# RECEIVE CLIENT RESPONSE TO HIS CHALLENGE
		data = int(c_socket.recv(1024))
		session_manager.log("[Device]: " + str(data))
		if(data != (challenge_client - 1)):
			raise Exception("Client failed authentication challenge, aborting session")
		
		session_manager.authenticated()
		#work to be done here
		session_manager.setNextState(EchoReplyState())

#
#	Ping-request - Ping-reply State
#

class EchoReplyState(AbstractSessionState):
	def __init__(self):
		AbstractSessionState.__init__(self)
		self.__TIMER_SECONDS = 5
		self.__RESPONSE_COMMAND = "PING_RES"
		self.__challenge = None

	def parse_ping_response(self, data):
		# arguments are separated by '#'
		if len(data) == 0:
			return False
			
		if len(data) != 0: 
			data_to_parse = str(data)
			data_to_parse = data_to_parse.split("#")
			command = data_to_parse[0]
			if command == self.__RESPONSE_COMMAND and len(data_to_parse) == 2:
				self.__challenge = int(data_to_parse[1])
			else:
				return False

		return True

	def handle(self, session_manager):
		#session_manager.log("EchoReplyState: Pinging client...")		
		c_socket = session_manager.getClientSocket();

		#SENDING PING_REQUEST
		challenge_ping = randint(0, 2147483647)		
		ping_request = "PING_REQ#" + str(challenge_ping) 
		session_manager.log("[SERVER]: " + str(ping_request))
		c_socket.send(ping_request)

		#WAITING FOR PING REPLY
		data = c_socket.recv(1024)
		session_manager.log("[DEVICE]: " + str(data))
		if not self.parse_ping_response(data):
			raise Exception("Client failed ping response, aborting session")
		
		if not self.__challenge == challenge_ping - 1:
			raise Exception("Client failed ping response, aborting session") 
		

		#ping device again in TIMER_SECONDS again
		time.sleep(self.__TIMER_SECONDS)
		session_manager.setNextState(EchoReplyState())

	
#data = c_socket.recv(1024)
#c_socket.send(msg_to_send)

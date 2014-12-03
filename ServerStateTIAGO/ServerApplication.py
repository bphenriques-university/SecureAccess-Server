#!/usr/bin/python2
# -*- coding: UTF-8 -*-

import threading
import SetUp
from bluetooth import *
from thread import *
from SessionState import *
import SquidUpdater
from operator import itemgetter

NUMBER_ALLOWED_CLIENTS = 4
DEFAULT_USER = "default_user"

#State machine
class ServerApplication():

	def __init__(self):
		self._UUID = "841eba55-800a-48eb-9e39-335265d8d23f"
		self._SERVICE_NAME = "SecureAccess"
		self._server_sock = None
		self._current_users_logged_in = list()
		self._list_mutex = threading.Lock()
		self._recheck_user = True
	
	def getServerSocket(self):
		return self._client_sock
		
	def setServerSocket(self, client_socket):
		self._client_sock = client_socket
	
	def _handleClient(self, conn, client_id, client_info):
		device_MAC = client_info[0]
		path_MAC = SetUp.USER_DIR_NAME + "/" + device_MAC
		print "[TIAGO]", path_MAC
		if os.path.isdir(path_MAC):
			key_file = open(path_MAC + SetUp.SYM_KEY_FILE, 'r')
			key_francis = key_file.readline()
			print "[TIAGO]", key_francis

			priority_file = open(path_MAC + SetUp.PRIORITY_FILE, 'r')
			priority = int(priority_file.readline())
			print "[TIAGO]", priority
			# esta key_francis esta' em base64
			client_session = Session(self, client_id, client_info, key_francis, priority, conn)
			client_session.start()
		else:
			print "User Inexistente"
	
	def newAuthenticatedUser(self, client_id, client_info, priority):
		self._list_mutex.acquire()
		print "Adding authenticated user [" + str(client_id) + "]: " + str(client_info)
		self._current_users_logged_in.append((client_id, client_info, priority))
		self._current_users_logged_in = sorted(self._current_users_logged_in, key=itemgetter(2,0), reverse=True)
		print self._current_users_logged_in
		self._recheck_user = True
		self._list_mutex.release()

	def disconnectUser(self, client_id, client_info, priority):
		self._list_mutex.acquire()
		self._current_users_logged_in.remove((client_id, client_info, priority))
		self._recheck_user = True
		self._list_mutex.release()

	def _web_blocker(self):

		print "#################################"
		print "##### STARTING WEB_BLOCKER   ####" 
			

		#set default blocks
		print_once = True
		while True:
			self._list_mutex.acquire()
			if not self._recheck_user:
				self._list_mutex.release()
				continue
			
			current_user = None
			if len(self._current_users_logged_in) == 0:
				if print_once:
					print "No users logged in..."
					print_once = False
				SquidUpdater.changeUsr(DEFAULT_USER)
			else:	
				print_once = True
				current_user = self._get_next_user()
				SquidUpdater.changeUsr(current_user[1][0])
				print "Changing privacy to: " + str(current_user)
		
			self._recheck_user = False
			self._list_mutex.release()
					
	def _get_next_user(self):
		return self._current_users_logged_in[0]


	def _create_service(self, uuid, server_name):
		s_socket = BluetoothSocket(RFCOMM)		
		s_socket.bind(("",PORT_ANY))
		print str(s_socket.getpeername())
		s_socket.listen(NUMBER_ALLOWED_CLIENTS)
	
		port = s_socket.getsockname()[1]
	
		advertise_service(s_socket, server_name,
				service_id = uuid,
				service_classes = [ uuid, SERIAL_PORT_CLASS ],
				profiles = [ SERIAL_PORT_PROFILE ])

		return s_socket

	def start(self):
		s_socket = None
		client_sock = None
		try:
			s_socket = self._create_service(self._UUID, self._SERVICE_NAME)
			
			print "#################################"
			print "##### Advertised Service:    ####" 
			print "#"
			print "# UUID: %s" % self._UUID
			print "# Name: %s" % self._SERVICE_NAME
			print "#"
			print "#################################"
			
			start_new_thread(self._web_blocker, ())

			client_id = 0
			print "Waiting for connection"
			while True:
				client_sock, client_info = s_socket.accept()
				client_id = client_id + 1
				
				print("@@ Connection #" + str(client_id) + " from: " + str(client_info))
				start_new_thread(self._handleClient, (client_sock, client_id, client_info))
		
		except Exception as e:
			print "[ERROR IN APPLICATION] - %s" % str(e)

			if client_sock is not None:
				client_sock.close()
			if s_socket is not None:
				s_socket.close()
			
			return -1

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

if __name__ == "__main__":
	bm = ServerApplication()
	bm.start()


from AbstractServerState import ServerState
from SecurityScripts.DiffieHellman import *

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

	def handle(self, data):
		if self.parse_data(data):
			print "######## Start of connection ########"
			print "# Base: %s"  % str(self.__base)
			print "# Prime: %s"  % str(self.__prime)
			print "# yDevice: %s"  % str(self.__yDevice)
		else:
			print "Bad Start of connection"	


		print "#"
		server = DiffieHellman(p = self.__prime, g = self.__base)
		print "# yServer : %s" % str(server.getPublicKey())
		
		server.generateKey(self.__yDevice)
		print "# Session Key: %s"  % str(server.getKey())
		
		
		

if __name__ == "__main__":
	a = StartConnectionState()
	
	P = 13232376895198612407547930718267435757728527029623408872245156039757713029036368719146452186041204237350521785240337048752071462798273003935646236777459223
	G = 5421644057436475141609648488325705128047428394380474376834667300766108262613900542681289080713724597310673074119355136085795982097390670890367185141189796
	YDEVICE = 1418521685869297987538209260728989332618690208764172549180019659548875135213325222765845153480650143393663206190036752034023618954752557133433561356759201
	
	data = "CONN#" + str(G) + "#" + str(P) + "#" + str(YDEVICE)
	
	a.handle(data)
	
	
	

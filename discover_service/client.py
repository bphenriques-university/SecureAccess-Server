from bluetooth import *
import sys

MESSAGE_TO_SENT = "HELLLOOOOO"
SERVICE_NAME = "SIRS"
uuid = "841eba55-800a-48eb-9e39-335265d8d23f"

# addr = "CC:52:AF:EF:5B:70"
# addr = "80-E6-50-13-E5-D5"


addr = "localhost"

if len(sys.argv) < 2:
    print("no device specified.  Searching all nearby bluetooth devices")
else:
    addr = sys.argv[1]
    print("Searching for SIRS on %s" % addr)

print "Searching for SIRS on %s" % addr

# search for the SampleServer service
service_matches = find_service(uuid = uuid, address = addr)

if len(service_matches) == 0:
    print "couldn't find the %s service" % SERVICE_NAME
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print "connecting to \"%s\" on %s:%s" % (name, host, port)

# Create the client socket
sock = None
try: 
	sock=BluetoothSocket(RFCOMM)
	sock.connect((host, port))
	print "connected."

	while True:
	    data = MESSAGE_TO_SENT
	    if len(data) == 0: break
	    sock.send(data)

	sock.close()

except Exception as e:
	print(e)
	sock.close()

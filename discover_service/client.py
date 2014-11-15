from bluetooth import *
import sys

MESSAGE_TO_SENT = "HELLLOOOOO"


addr = "CC:52:AF:EF:5B:70"
print "Searching for SampleServer on %s" % addr

# search for the SampleServer service
uuid = "741eba55-800a-48eb-9e39-335265d8d23f"
service_matches = find_service(uuid = uuid, address = addr)

if len(service_matches) == 0:
    print "couldn't find the SampleServer service =("
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print "connecting to \"%s\" on %s" % (name, host)

# Create the client socket
sock=BluetoothSocket( RFCOMM )
sock.connect((host, port))

print "connected."
while True:
    data = MESSAGE_TO_SENT
    if len(data) == 0: break
    sock.send(data)

sock.close()
"""
Shows how to send "Hello world" over a RFCOMM client socket.
"""
import lightblue

# ask user to choose the device to connect to
#hostaddr = lightblue.selectdevice()[0]        
#hostaddr = "localhost"
hostaddr = "80:E6:50:13:E5:D5"

# find the EchoService advertised by the simple_server.py example

listservices = lightblue.findservices(addr=hostaddr, name="EchoService")


print("-------")
print(listservices)
print("-------")
echoservice = listservices[0]
serviceport = echoservice[1]

s = lightblue.socket()

try:
	print("trying to connect to:")
	print("Address: %s" % hostaddr)
	print("Port: %s" % serviceport)
	a = s.connect((hostaddr, serviceport))
	print(a)	
	print(s)
	s.send("Hello world!")
	print "Sent data, waiting for echo..."
	data = s.recv(1024)
	print "Got data:", data
	s.close()
except Exception as e:
	print(e)
	s.close()


# Note:
# Instead of calling selectdevice() and findservices(), you could do:
#       hostaddr, serviceport, servicename = lightblue.selectservice()
# to ask the user to choose a service (instead of just choosing the device).

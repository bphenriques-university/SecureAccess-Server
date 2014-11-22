#!/usr/bin/env python
from bluetooth import *
from PyOBEX.client import BrowserClient
 
# bluetooth device address
address = '50:56:63:4F:BF:4B'
 
# find OBEX port using SDP
svc = find_service(address=address, uuid=OBEX_FILETRANS_CLASS)
channel = svc[0]['port']
 
# send file
print 'sending file to %s...'%address
client = BrowserClient(address, channel)
client.connect()
client.put('test.txt', 'HelloWorld!')
client.disconnect()

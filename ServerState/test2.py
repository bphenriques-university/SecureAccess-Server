from Crypto.Cipher import AES
import base64
import os
import sys

from Crypto.Util import Counter
from Crypto import Random
from base64 import b64encode, b64decode

key = "E8ffc7e56311679f12b6fc91aa77a5eb"
plaintext = "Bruno Henriques 12345";

random_generator = Random.new()
print str(random_generator.read(8))

# Create counter for encryptor
iv = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
print str(iv)
ctr_e = Counter.new(64, prefix = iv)

encryptor = AES.new(key, AES.MODE_CTR, counter = ctr_e)
#ciphertext = encryptor.encrypt(plaintext)
#print b64encode(ciphertext)


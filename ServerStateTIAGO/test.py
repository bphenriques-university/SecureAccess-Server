import base64
from Crypto import Random
from Crypto.Cipher import AES

from base64 import b64encode, b64decode

class AESCipher:

    def __init__(self, key, iv):
		self.iv = iv
		self.bs = 32
		self.key = key #hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        
        print str(AES.block_size)
        iv = self.iv #Random.new().read(AES.block_size)
        
        cipher = AES.new(self.key, AES.MODE_CBC, str(iv))
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        self.iv = iv #iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
        
if __name__ == "__main__":
	iv = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
	key = "E8ffc7e56311679f12b6fc91aa77a5eb"
	cipher = AESCipher(key, iv)
	text = "Bruno Henriques 12345"
	ciphered = cipher.encrypt(text)
	print b64encode(ciphered)

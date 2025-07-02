from Crypto.Cipher import DES3, AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

def des3_encrypt(data, key):
    key = key[:24].ljust(24, '0').encode()
    cipher = DES3.new(key, DES3.MODE_ECB)
    ct = cipher.encrypt(pad(data.encode(), 8))
    return b64encode(ct).decode()

def des3_decrypt(data, key):
    key = key[:24].ljust(24, '0').encode()
    cipher = DES3.new(key, DES3.MODE_ECB)
    pt = unpad(cipher.decrypt(b64decode(data)), 8)
    return pt.decode()

def aes_encrypt(data, key):
    key = key[:32].ljust(32, '0').encode()
    cipher = AES.new(key, AES.MODE_ECB)
    ct = cipher.encrypt(pad(data.encode(), 16))
    return b64encode(ct).decode()

def aes_decrypt(data, key):
    key = key[:32].ljust(32, '0').encode()
    cipher = AES.new(key, AES.MODE_ECB)
    pt = unpad(cipher.decrypt(b64decode(data)), 16)
    return pt.decode()

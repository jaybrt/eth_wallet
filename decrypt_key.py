from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Util.Padding import pad, unpad
import json
from getpass import getpass
from generate_wallet import get_public_key, get_address

file_address = input('File Name: ')
password = getpass()

with open(file_address +  '.json') as f:
    file_data = json.load(f)

salt = file_data['salt']
iv = file_data['initialization vector']
encrypted_private_key = file_data['encrypted private key']

salt = bytes.fromhex(salt)
iv = bytes.fromhex(iv)
encrypted_private_key = bytes.fromhex(encrypted_private_key)

key = scrypt(password, salt, 32, N = 2**20, r = 8, p=1)

cipher = AES.new(key, AES.MODE_CBC, iv)

private_key = unpad(cipher.decrypt(encrypted_private_key), AES.block_size)
public_key = get_public_key(private_key)

print(private_key.decode('utf-8'))
print(public_key)
print(get_address(public_key))

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import json
import generate_wallet as wallet
from getpass import getpass

password = bytes(getpass(), 'utf-8')
file_address = input('File Name: ')
salt = get_random_bytes(16)

key = scrypt(password, salt, 32, N = 2**20, r = 8, p = 1)

private_key, public_key, address = wallet.new_wallet()
private_key_data = str(private_key).encode('utf-8')

cipher = AES.new(key, AES.MODE_CBC)
cipher_text_bytes = cipher.encrypt(pad(private_key_data, AES.block_size))

salt = salt.hex()
iv = cipher.iv.hex()
cipher_text = cipher_text_bytes.hex()

output = {'salt': salt, 'initialization vector': iv, 'encrypted private key': cipher_text}

with open(file_address + '.json', 'w') as f:
    json.dump(output, f)

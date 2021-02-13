from tinyec.ec import SubGroup, Curve
from Crypto.Random.random import randint
from web3 import Web3

p = int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F', 16)
n = int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141', 16)
h = 1

x = int('79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798', 16)
y = int('483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8', 16)
g = (x,y)

field = SubGroup(p, g, n, h)
curve = Curve(a = 0, b = 7, field = field, name = 'secp256k1')


def new_wallet():
    private_key = randint(1, n)
    #private_key = int("f8f8a2f43c8376ccb0871305060d7b27b0554d2cc72bccf41b2705608452f315", 16)

    private_key_hex = Web3.toHex(private_key)[2:]
    public_key_hex = get_public_key(private_key_hex)

    address = get_address(public_key_hex)

'''
    print(private_key_hex, public_key_hex, address)
'''

    return private_key_hex, public_key_hex, address

def get_public_key(priv_key):
    priv_key = int(priv_key, 16)
    pub_key = priv_key * curve.g
    pub_key_hex = Web3.toHex(pub_key.x)[2:] + Web3.toHex(pub_key.y)[2:]
    return pub_key_hex

def get_address(pub_key):
    address = Web3.keccak(hexstr = pub_key).hex()
    address = '0x' + address[-40:]
    address = Web3.toChecksumAddress(address)
    return address

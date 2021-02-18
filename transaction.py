from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import json
from infura_credentials import project_id, project_secret, endpoint
import decrypt_key
from generate_wallet import get_address, get_public_key
import dai_abi

w3 = Web3(Web3.HTTPProvider(endpoint))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

print(w3.isConnected())

private_key, *_  = decrypt_key.get_key()

abi = json.loads(dai_abi.abi)
dai_address = '0xc3dbf84Abb494ce5199D5d4D815b10EC29529ff8'
dai = w3.eth.contract(address = dai_address, abi=abi)

print(dai.functions.totalSupply().call())

address = lambda x: get_address(get_public_key(x))

print(w3.eth.get_balance(address(private_key)))

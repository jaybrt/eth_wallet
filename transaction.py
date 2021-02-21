from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import json
from infura_credentials import project_id, project_secret, endpoint
import decrypt_key
from generate_wallet import get_address, get_public_key
import dai_abi

def make_txn(destination, pk, amount):
    txn = dict(
    nonce = w3.eth.getTransactionCount(address(pk)),
    gasPrice = w3.eth.gasPrice,
    gas = 100000,
    to = destination,
    value = amount,
    data = b'',
    chainId = 4
    )

    signed_txn = w3.eth.account.signTransaction(txn, private_key)

    return signed_txn

def login():
    private_key, *_  = decrypt_key.get_key()
    return private_key

if __name__ == '__main__':
    w3 = Web3(Web3.HTTPProvider(endpoint))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    if w3.isConnected():print('Connected')

    private_key = login()

    abi = json.loads(dai_abi.abi)
    dai_address = '0xc3dbf84Abb494ce5199D5d4D815b10EC29529ff8'
    dai = w3.eth.contract(address = dai_address, abi=abi)

    print(dai.functions.totalSupply().call())

    address = lambda x: get_address(get_public_key(x))

    #print(w3.eth.get_balance(address(private_key)))
    #print(w3.eth.getTransactionCount(address(private_key)))


    #txn = make_txn('0x6D677F67d6C0ceE0Be87dBEB701C1577361799b8', private_key, 1)
    #txn_hash = w3.eth.sendRawTransaction(txn.rawTransaction)
    #print(txn_hash)

    while True:
        action = input('Type 1 to send transaction and 2 to check balance or 3 to logout\n')
        if action == '1':
            receiver = input('To whom?\n')
            amt = int(float(input('For what amount?(ETH)\n'))*1_000_000_000_000_000_000)
            txn = make_txn(receiver, private_key, amt)
            txn_hash = w3.eth.sendRawTransaction(txn.rawTransaction)
            print(f"Hash: {txn_hash.hex()}")
        elif action == '2':
            print(w3.eth.get_balance(address(private_key))/1000000000000000000)
        elif action == '3':
            exit()

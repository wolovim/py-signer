from web3 import Web3, EthereumTesterProvider
w3 = Web3(EthereumTesterProvider())

# pip install ../eth-account
# example provided in docs
# import json
from eth_account import Account
from eth_account.messages import encode_typed_data

# all domain properties are optional
domain_data = {
    "name": "Ether Mail",
    "version": "1",
    "chainId": 1,
    "verifyingContract": "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC",
    "salt": b"decafbeef",
}
# custom types
msg_types = {
    "Person": [
        {"name": "name", "type": "string"},
        {"name": "wallet", "type": "address"},
    ],
    "Mail": [
        {"name": "from", "type": "Person"},
        {"name": "to", "type": "Person"},
        {"name": "contents", "type": "string"},
    ],
}
# the data to be signed
msg_data = {
    "from": {
        "name": "Cow",
        "wallet": "0xCD2a3d9F938E13CD947Ec05AbC7FE734Df8DD826",
    },
    "to": {
        "name": "Bob",
        "wallet": "0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB",
    },
    "contents": "Hello, Bob!",
}

private_key = "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
signable_msg = encode_typed_data(domain_data, msg_types, msg_data)
signed_msg = Account.sign_message(signable_msg, private_key)
print(signed_msg.messageHash)
# HexBytes('0xc5bb16ccc59ae9a3ad1cb8343d4e3351f057c994a97656e1aff8c134e56f7530')

# recover the message signer
signer = Account.recover_message(signable_msg, signature=signed_msg.signature)

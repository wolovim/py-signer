import click
from ape.cli import NetworkBoundCommand, network_option
from ape import project, accounts
from eth_account import Account
from eth_account.messages import encode_typed_data
from hexbytes import HexBytes


@click.command(cls=NetworkBoundCommand)
@network_option()
def cli(network):
    if "foundry" not in network:
        raise click.ClickException("This script is only for the Foundry network")

    # set up accounts
    user1 = accounts.test_accounts[0]
    user2 = accounts.test_accounts[1]

    # deploy the contract
    contract = user1.deploy(project.Verifier)

    domain_data = {
        "name": "Ether Mail",
        "version": "1",
        "chainId": 31337,  # Foundry/Anvil
        "verifyingContract": contract.address,
        # "salt": b"decafbeef",
    }

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

    # user2 signs a message; PK taken from Anvil terminal output
    # (( note: store your keys securely! this is only for demo purposes ))
    user2_pk = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"

    # encode + sign in two steps:
    signable_msg = encode_typed_data(domain_data, msg_types, msg_data)
    # signed_msg = Account.sign_message(signable_msg, user2_pk)

    # or one step combined:
    signed_msg = Account.sign_typed_data(user2_pk, domain_data, msg_types, msg_data)

    # verify the message signer in python - note: no domain verification here
    print("\nVerifying signer via eth-account...")
    msg_signer = Account.recover_message(signable_msg, signature=signed_msg.signature)
    assert msg_signer == user2.address
    print("Success!")

    # Ape/web3.py can't handle dicts; convert values to tuple:
    msg_data_tuple = (
        (msg_data["from"]["name"], msg_data["from"]["wallet"]),
        (msg_data["to"]["name"], msg_data["to"]["wallet"]),
        msg_data["contents"],
    )

    # verify the message signer + domain in the contract
    print("\nVerifying signer and domain via smart contract...")
    signer_712 = contract.recoverAddress(msg_data_tuple, signed_msg.signature)
    assert signer_712 == user2.address
    print("Success!")

    # EIP-5267 specifies how contracts can advertise what domain fields
    # they support and is part of OpenZeppelin's 712 util library
    # https://eips.ethereum.org/EIPS/eip-5267
    print("\nReading supported EIP-712 domain fields...")
    domain = contract.eip712Domain()
    assert domain["fields"] == HexBytes("0x0f")  # bitmap of supported fields
    assert domain["name"] == "Ether Mail"
    assert domain["version"] == "1"
    assert domain["chainId"] == 31337  # Anvil chain id
    assert domain["verifyingContract"] == contract.address
    assert domain["salt"] == HexBytes(
        "0x0000000000000000000000000000000000000000000000000000000000000000"
    )
    assert domain["extensions"] == []  # list of supported extension EIP numbers
    print("Success!")

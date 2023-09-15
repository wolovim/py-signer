import click
import json
from ape.cli import NetworkBoundCommand, network_option
from ape import project, accounts
from eth_account import Account
from .utils import signable_msg
from hexbytes import HexBytes


@click.command(cls=NetworkBoundCommand)
@network_option()
def cli(network):
    if "foundry" not in network:
        raise click.ClickException("This script is only for the foundry network")

    # set up accounts
    user1 = accounts.test_accounts[0]
    user2 = accounts.test_accounts[1]

    # deploy the contract
    contract = user1.deploy(project.Verify)
    print("Contract address: ", contract.address)

    # parse the ABI
    contract_abi = json.loads(contract.contract_type.json())["abi"]

    print(f"CONTRACT_ADDRESS='{contract.address}'")
    print(f"CONTRACT_ABI='{contract_abi}'")

    # user2 signs a message
    user2_pk = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"
    signed_msg = Account.sign_message(signable_msg, user2_pk)
    print("Signed message: ", signed_msg.messageHash)

    # verify the message signer in python
    print("\nVerifying message via eth-account...")
    signer = Account.recover_message(signable_msg, signature=signed_msg.signature)
    assert signer == user2.address
    print("Success!")

    # verify the message signer in the contract
    print("\nVerifying message via smart contract...")
    verified = contract.verifyMessage(
        user2.address, signed_msg.messageHash, signed_msg.v, signed_msg.r, signed_msg.s
    )
    assert verified
    print("Success!")

    # TODO: use OpenZeppelin utils to verify signer and domain
    #

    ## Bonus: EIP-5267 specifies how contracts can advertise what domain fields they support
    # https://eips.ethereum.org/EIPS/eip-5267
    # Motivation: "Notably, EIP-712 does not specify any way for contracts to publish which
    #   of these fields they use or with what values. This has likely limited adoption of
    #   EIP-712, as it is not possible to develop general integrations, and instead
    #   applications find that they need to build custom support for each EIP-712 domain."
    print("\nReading supported EIP-712 domain fields...")
    domain = contract.eip712Domain()
    assert domain["fields"] == HexBytes("0x0f")
    assert domain["name"] == "Ether Mail"
    assert domain["version"] == "1"
    assert domain["chainId"] == 31337  # foundry chain id
    assert domain["verifyingContract"] == contract.address
    assert domain["salt"] == HexBytes(
        "0x0000000000000000000000000000000000000000000000000000000000000000"
    )
    assert domain["extensions"] == []
    print("Success!")

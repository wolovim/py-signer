# py-signer

Demo app for signing and verifying signed typed data (EIP-712)

Utilizes:

- [Ape](https://docs.apeworx.io/ape/stable/userguides/quickstart.html) - smart contract development framework for Python devs
- [OpenZeppelin contracts](https://docs.openzeppelin.com/contracts/4.x/api/utils#EIP712) - typed data and cryptography utils
- [Foundry](https://book.getfoundry.sh/) - local test network (Anvil)

## Setup

- `pip install eth-ape eth-account ipython pdbpp`
- Install [Foundry](https://book.getfoundry.sh/getting-started/installation#installation)
- `ape plugins install .`

## Development

- Run `anvil` in one terminal window
- `ape run verify --network ::foundry`

## Resources

- Snake Charmer's explainer blog post - Coming Soon™
- [EIP-712](https://eips.ethereum.org/EIPS/eip-712)
- [Intro to Ape](https://snakecharmers.ethereum.org/intro-to-ape/)
- MetaMask's [eth_signTypedData_v4 docs](https://docs.metamask.io/wallet/how-to/sign-data/#use-eth_signtypeddata_v4)

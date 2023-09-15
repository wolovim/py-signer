// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract Verify {
    // ERC-5267: Retrieval of EIP-712 domain
    // https://eips.ethereum.org/EIPS/eip-5267
    function eip712Domain() external view returns (
        bytes1 fields, // bitmap of fields present
        string memory name,
        string memory version,
        uint256 chainId,
        address verifyingContract,
        bytes32 salt, // unused in this example
        uint256[] memory extensions
    ) {
      return (hex"0f", "Ether Mail", "1", block.chainid, address(this), bytes32(0), new uint256[](0));
    }
    
    function verifyMessage(
        address _signer,
        bytes32 _message,
        uint8 _v,
        bytes32 _r,
        bytes32 _s
    ) public pure returns (bool) {
        return _signer == ecrecover(_message, _v, _r, _s);
    }
}

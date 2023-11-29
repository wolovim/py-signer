// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

// Note: ERC-5267 "Retrieval of EIP-712 domain" baked into OZ's EIP712:
import {EIP712} from "@openzeppelin/utils/cryptography/EIP712.sol";
import {ECDSA} from "@openzeppelin/utils/cryptography/ECDSA.sol";

contract Verifier is EIP712 {
    struct Person {
        string name;
        address wallet;
    }

    struct Mail {
        Person from;
        Person to;
        string contents;
    }

    bytes32 constant PERSON_TYPEHASH = keccak256(
      "Person(string name,address wallet)"
    );

    bytes32 constant MAIL_TYPEHASH = keccak256(
      "Mail(Person from,Person to,string contents)Person(string name,address wallet)"
    );

    // OZ EIP712 sets verifyingContract and chainId
    constructor() EIP712("Ether Mail", "1") {}
    
    function hashString(string calldata _source) private pure returns (bytes32) {
      return keccak256(bytes(_source));
    }
    
    function hashPerson(Person calldata _person) private pure returns (bytes32) {
      return keccak256(abi.encode(PERSON_TYPEHASH, hashString(_person.name), _person.wallet));
    }

    function hashMail(Mail calldata _mail) private pure returns (bytes32) {
      return keccak256(abi.encode(MAIL_TYPEHASH, hashPerson(_mail.from), hashPerson(_mail.to), hashString(_mail.contents)));
    }
    
    function mailHashData(Mail calldata _mail) public view returns (bytes32) {
      bytes32 encoded = hashMail(_mail);
      return _hashTypedDataV4(encoded);
    }
    
    function recoverAddress(Mail calldata _mail, bytes calldata _signature) public view returns (address) {
      bytes32 encoded = mailHashData(_mail);
      return ECDSA.recover(encoded, _signature);
    }
}

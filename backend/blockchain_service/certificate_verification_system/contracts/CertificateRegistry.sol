// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertificateRegistry {
    mapping(bytes32 => address) public ownerOf;
    event CertificateRegistered(bytes32 indexed certHash, address indexed owner, uint256 timestamp);

    function registerCertificate(bytes32 certHash) public {
        require(ownerOf[certHash] == address(0), "Already registered");
        ownerOf[certHash] = msg.sender;
        emit CertificateRegistered(certHash, msg.sender, block.timestamp);
    }

    function isRegistered(bytes32 certHash) public view returns (bool) {
        return ownerOf[certHash] != address(0);
    }

    function getOwner(bytes32 certHash) public view returns (address) {
        return ownerOf[certHash];
    }
}

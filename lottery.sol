pragma solidity >= 0.5.0 <0.9.0;

contract Lottery {
    address public manager;
    address payable[] public participants;

    constructor() {
        manager = msg.sender;
    }

    
    function enter() public payable {
        require(msg.value == 0.002 ether, "Minimum entry is 0.002 ETH");
        participants.push(payable(msg.sender));
    }

    function getBalance() public view returns (uint) {
        require(msg.sender == manager, "Only manager can view balance");
        return address(this).balance;
    }

    function random() public view returns (uint) {
        return uint(keccak256(abi.encodePacked(block.prevrandao, block.timestamp, participants.length)));
    }

  
    function selectwinner() public {
        require(msg.sender == manager, "Only manager can pick winner");
        require(participants.length >= 3, "At least 3 participants required");

        uint r = random();
        uint index = r % participants.length;
        address payable winner = participants[index];

        winner.transfer(getBalance());
        participants = new address payable ;
    }
}

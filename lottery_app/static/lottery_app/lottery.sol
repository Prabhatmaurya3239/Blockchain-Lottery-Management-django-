// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract AdvancedLottery {
    address public manager;
    address public websiteOwner;

    uint public entryFee;
    bool public isActive;
    uint[] public prizeDistribution; // [60, 30, 10] => 1st, 2nd, 3rd
    uint public managerCut;
    uint public ownerCut;

    address payable[] public participants;
    address[] public winners;

    event Entered(address indexed participant);
    event WinnersDeclared(address[] winners, uint totalPrize);
    event Refunded(address indexed participant, uint amount);

    constructor(
        uint _entryFee,
        uint[] memory _prizeDistribution,
        uint _managerCut,
        uint _ownerCut,
        address _websiteOwner
    ) {
        require(_prizeDistribution.length > 0 , "prizeDistribution lenght must not be zero");
        uint totalCut = _managerCut + _ownerCut;
        uint totalPrize = 0;
        for (uint i = 0; i < _prizeDistribution.length; i++) {
            totalPrize += _prizeDistribution[i];
        }
        require(totalCut + totalPrize == 100, "Total percentage must equal 100");

        manager = msg.sender;
        websiteOwner = _websiteOwner;
        entryFee = _entryFee;
        prizeDistribution = _prizeDistribution;
        managerCut = _managerCut;
        ownerCut = _ownerCut;
        isActive = true;
    }

    modifier onlyManager() {
        require(msg.sender == manager, "Only manager allowed");
        _;
    }
   function updatePrizeDistribution(uint[] memory _newDistribution) public onlyManager {
    require(address(this).balance == 0, "Cannot update: Contract balance is not zero");
    require(_newDistribution.length > 0 , "prizeDistribution lenght must not be zero");

    uint total = managerCut+ownerCut;
    for (uint i = 0; i < _newDistribution.length; i++) {
        total += _newDistribution[i];
    }

    require(total == 100, "Total prize distribution must equal 100%");

    prizeDistribution = _newDistribution;
}
    function enter() public payable {
        require(isActive, "Lottery is not active");
        require(msg.value == entryFee , "Incorrect entry fee");
        participants.push(payable(msg.sender));
        emit Entered(msg.sender);
    }

    function getBalance() public view returns (uint) {
        return address(this).balance;
    }

    function status() public view returns (
        address _manager,
        address _websiteOwner,
        uint _totalPrize,
        uint _participants,
        uint[] memory _prizeDistribution,
        uint _managerPercent,
        uint _ownerPercent,
        address[] memory _winners,
        bool _isActive
    ) {
        return (
            manager,
            websiteOwner,
            address(this).balance,
            participants.length,
            prizeDistribution,
            managerCut,
            ownerCut,
            winners,
            isActive
        );
    }

    function random() internal view returns (uint) {
        return uint(keccak256(abi.encodePacked(block.prevrandao, block.timestamp, participants.length)));
    }

    function declareWinners() public onlyManager {
    require(participants.length >= prizeDistribution.length, "Not enough participants");

    uint total = address(this).balance;
    uint remaining = total;

    delete winners;

    // Manual copy to memory
    address payable[] memory tempParticipants = new address payable[](participants.length);
    for (uint i = 0; i < participants.length; i++) {
        tempParticipants[i] = participants[i];
    }

    for (uint i = 0; i < prizeDistribution.length; i++) {
        uint r = random() % tempParticipants.length;
        address payable winner = tempParticipants[r];
        winners.push(winner);

        uint amount = (total * prizeDistribution[i]) / 100;
        winner.transfer(amount);
        remaining -= amount;

        // Remove winner from list
        tempParticipants[r] = tempParticipants[tempParticipants.length - 1];
        assembly { mstore(tempParticipants, sub(mload(tempParticipants), 1)) }
    }

    // Manager and website owner cut
    uint managerAmount = (total * managerCut) / 100;
    uint ownerAmount = (total * ownerCut) / 100;

    payable(manager).transfer(managerAmount);
    payable(websiteOwner).transfer(ownerAmount);

    emit WinnersDeclared(winners, total);
    delete participants; // Reset for next round
}


    function cancelLottery() public onlyManager {
        require(isActive, "Already inactive");
        isActive = false;

        for (uint i = 0; i < participants.length; i++) {
            participants[i].transfer(entryFee);
            emit Refunded(participants[i], entryFee);
        }

        delete participants;
    }

    function restartLottery() public onlyManager {
        require(!isActive, "Already active");
        isActive = true;
    }
    function stopLottery() public onlyManager{
        require(getBalance() == 0, "Balance must be 0 for stop other option cancel to lottery");
        isActive = false;
    }

    receive() external payable {
        enter();
    }
}

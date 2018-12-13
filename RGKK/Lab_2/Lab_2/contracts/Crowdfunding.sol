pragma solidity ^0.4.24;

import "./Timer.sol";

/// This contract represents the most simple crowdfunding campaign.
/// This contract does not protect investors from not receiving goods
/// they were promised from the crowdfunding owner. This kind of contract
/// might be suitable for campaigns that do not promise anything to the
/// investors except that they will start working on the project.
/// (e.g. almost all blockchain spinoffs.)
contract Crowdfunding {

  address private owner;
  uint256 private goal;
  mapping (address => uint256) public investments;

  Timer private timer;
  uint256 private endTimestamp;

  constructor(
    address _owner,
    Timer _timer,
    uint256 _goal,
    uint256 _endTimestamp
  ) public {
    owner = _owner == 0 ? msg.sender : _owner;
    timer = _timer;
    goal = _goal;
    endTimestamp = _endTimestamp;
  }


  //use "emit ScreamSomething(...)" as a primitive printline command
  event ScreamBoolean(bool boolean);
  event ScreamInteger(uint256 integer);
  event ScreamAddress(address add);



  function invest() public payable {
    require(IsBeforeEnd(), "The end has been reached!");

    investments[msg.sender] += msg.value;
  }

  function claimFunds() public {
    require(IsOwner(), "Not the owner!");
    require(IsAfterEnd(), "The end has not been reached!");
    require(IsGoalMet(), "The goal has not been met!");


    uint256 money = GetContractBalance();
    owner.transfer(money);
  }

  function refund() public {
    require(IsAfterEnd(), "The end has not been reached!");
    require(IsGoalUnmet(), "The goal has been met!");

    uint256 amount = investments[msg.sender];
    investments[msg.sender] = 0;
    msg.sender.transfer(amount);
  }



  function IsGoalMet() private view returns (bool) {
    if (GetContractBalance() >= goal) {
      return true;
    }
    return false;
  }

  function IsGoalUnmet() private view returns (bool) {
    if (GetContractBalance() < goal) {
      return true;
    }
    return false;
  }

  function GetContractBalance() private view returns (uint256) {
    return address(this).balance;
  }

  function IsOwner() private view returns (bool) {
    if (owner == msg.sender) {
      return true;
    }
    return false;
  }

  function IsAfterEnd() private view returns (bool) {
    if (endTimestamp < timer.getTime()) {
      return true;
    }
    return false;
  }

  function IsBeforeEnd() private view returns (bool) {
    if (endTimestamp >= timer.getTime()) {
      return true;
    }
    return false;
  }

}

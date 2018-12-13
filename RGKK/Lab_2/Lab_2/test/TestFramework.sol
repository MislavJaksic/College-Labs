pragma solidity ^0.4.24;

import "../contracts/Auction.sol";
import "../contracts/DutchAuction.sol";
import "../contracts/Crowdfunding.sol";
import "../contracts/EnglishAuction.sol";
import "../contracts/Timer.sol";
import "../contracts/TreasureHunt.sol";
import "truffle/Assert.sol";


// Needs to be defined here or else Truffle complains
contract TestFramework{
    //can receive money
    function() public payable {}
}

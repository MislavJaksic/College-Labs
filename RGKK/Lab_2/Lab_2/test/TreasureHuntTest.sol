pragma solidity ^0.4.24;

import "./TestFramework.sol";

contract TreasureHuntTest {

    uint public initialBalance = 1 ether;

    function () public payable {}

    constructor () public payable {}

    // If you want to solve this task uncomment this test.

    /*function testTreasureHuntSolution() public {
        TreasureHunt treasureHunt = new TreasureHunt({_price: 0.1 ether});
        TreasureHuntSolution solution = new TreasureHuntSolution();
        treasureHunt.openTreasure.value(0.1 ether).gas(200000)(solution.getSolution());
        Assert.isTrue(address(treasureHunt).balance == 0.0, "No balance should be transferred.");
    }*/
}

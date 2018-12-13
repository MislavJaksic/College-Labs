pragma solidity ^0.4.24;

import "./TestFramework.sol";

contract DutchAuctionBidder {

    DutchAuction auction;

    constructor(DutchAuction _auction) public {
        auction = _auction;
    }

    //wrapped call
    function bid(uint bidValue) public returns (bool success) {
        success = address(auction).call.value(bidValue).gas(2000000)(bytes4(keccak256("bid()")));
    }

    //can receive money
    function() public payable {}
}

contract DutchAuctionTest {

    DutchAuction testAuction;
    MockTimer timer;

    // Adjust this to change the test code's initial balance
    uint public initialBalance = 1000000000 wei;

    //can receive money
    function() public payable {}

    constructor() public payable {}

    function setupContracts() public {
        timer = new MockTimer(0);
        testAuction = new DutchAuction(
            this,  // Seller
            0,     // Judge -> if no judge, anybody can call settle.
            timer, // Timer
            300,   // Initial price
            10,    // Bidding period
            20     // Offer price decrement
        );
    }

    event LogEvent(bool value, string msg);
    event BalanceEvent(uint balance);
    function makeBid(
        uint bidValue,
        uint bidTime,
        uint expectedPrice,
        bool expectedResult,
        string message
    ) internal {
        DutchAuctionBidder bidder = new DutchAuctionBidder(testAuction);
        address(bidder).transfer(bidValue); // Give bidder money to bid
        timer.setTime(bidTime); // Set up time
        address previousHighestBidder = testAuction.getHighestBidder();
        uint initialAuctionBalance = address(testAuction).balance;
        bool result = bidder.bid(bidValue); // Expected result
        if (expectedResult == false) {
            Assert.isFalse(result, message);
            Assert.equal(previousHighestBidder, testAuction.getHighestBidder(), "No highest bidder should be declared after invalid bid");
        } else {
            emit LogEvent(result, "Result should be true");
            Assert.isTrue(result, message);
            Assert.equal(address(testAuction).balance, initialAuctionBalance + expectedPrice, "Auction should retain final price");
            Assert.equal(address(bidder).balance, bidValue - expectedPrice, "Bidder should be refunded excess bid amount");
            Assert.equal(bidder, testAuction.getHighestBidder(), "Bidder should be declared the highest bidder");
        }
    }

    function testCreateDutchAuction() public {
        setupContracts();
    }

    function testLowBids() public {
        setupContracts();
        makeBid(299, 0, 0, false, "Low bid should be rejected");
        makeBid(240, 2, 0, false, "Low bid should be rejected");
        makeBid(100, 5, 0, false, "Low bid should be rejected");
    }

    function testExactBid() public {
        setupContracts();
        makeBid(300, 0, 300, true, "Exact bid should be accepted");
        setupContracts();
        makeBid(280, 1, 280, true, "Exact bid should be accepted");
        setupContracts();
        makeBid(120, 9, 120, true, "Exact bid should be accepted");
    }

    function testValidBidAfterInvalid() public {
        setupContracts();
        makeBid(299, 0, 0, false, "Low bid should be rejected");
        makeBid(300, 0, 300, true, "Valid bid after failed bid should succeed");
    }

    function testLateBid() public {
        setupContracts();
        makeBid(300, 11, 0, false, "Late bid should be rejected");
    }

    function testSecondValidBid() public {
        setupContracts();
        makeBid(280, 1, 280, true, "Exact bid should be accepted");
        makeBid(300, 0, 0, false, "Second bid should be rejected");
    }

    function testRefundHighBid() public {
        setupContracts();
        makeBid(300, 2, 260, true, "High bid should be accepted");
    }

}

pragma solidity ^0.4.24;

import "./TestFramework.sol";

contract SimpleAuction is Auction {

    // constructor
    constructor(
        address _sellerAddress,
        address _judgeAddress,
        Timer _timer
    ) public payable Auction(_sellerAddress, _judgeAddress, _timer) {}

    function finish(Auction.Outcome _outcome, address _highestBidder) public {
        // This is for the test purposes and exposes finish auction to outside.
        finishAuction(_outcome, _highestBidder);
    }

    //can receive money
    function() public payable {}
}

contract Participant {

    Auction auction;

    constructor() public {}

    function setAuction(Auction _auction) public {
        auction = _auction;
    }

    //wrapped call
    function callSettle() public returns (bool success) {
        success = address(auction).call.gas(200000)(bytes4(keccak256("settle()")));
    }

    //wrapped call
    function callRefund() public returns (bool success)  {
        success = address(auction).call.gas(200000)(bytes4(keccak256("refund()")));
    }

    //can receive money
    function() public payable {}
}


contract AuctionTest {

    SimpleAuction testAuction;

    // Adjust this to change the test code's initial balance
    uint public initialBalance = 1000000000 wei;
    Participant judge;
    Participant seller;
    Participant highestBidder;
    Participant other;

    //can receive money
    function() public payable {}

    constructor() public payable {}

    function setupContracts(bool hasJudge) public {
        judge = new Participant();
        highestBidder = new Participant();
        seller = new Participant();
        other = new Participant();
        Timer timer = new MockTimer(0);
        testAuction = hasJudge
                    ? new SimpleAuction(seller, judge, timer)
                    : new SimpleAuction(seller, address(0), timer);

        address(testAuction).transfer(100 wei);

        judge.setAuction(testAuction);
        seller.setAuction(testAuction);
        highestBidder.setAuction(testAuction);
        other.setAuction(testAuction);
    }

    function testCreateContracts() public {
        setupContracts({hasJudge: true});
        Assert.isFalse(false, "this test should not fail");
        Assert.isTrue(true, "this test should never fail");
        Assert.equal(uint(7), uint(7), "this test should never fail");
    }

    ////////////////////////////////////////////////////////////////////////
    //                        Settle tests                                //
    ////////////////////////////////////////////////////////////////////////

    function testEarlySettle() public {
        setupContracts({hasJudge: true});
        Assert.isFalse(judge.callSettle(), "Settle with no declared highest bidder should be rejected");
    }

    function testUnauthorizedSettle() public {
        setupContracts({hasJudge: true});
        testAuction.finish(Auction.Outcome.SUCCESSFUL, address(highestBidder));
        Assert.isFalse(seller.callSettle(), "Unauthorized Settle call should be rejected");
        Assert.isFalse(other.callSettle(), "Unauthorized Settle call should be rejected");
    }

    function testJudgeSettle() public {
        setupContracts({hasJudge: true});
        testAuction.finish(Auction.Outcome.SUCCESSFUL, address(highestBidder));
        Assert.isTrue(judge.callSettle(), "Judge Settle call should succeed");
        Assert.equal(address(seller).balance, 100, "seller should receive funds after Settle");
    }

    function testHighestBidderSettle() public {
        setupContracts({hasJudge: true});
        testAuction.finish(Auction.Outcome.SUCCESSFUL, address(highestBidder));
        Assert.isTrue(highestBidder.callSettle(), "Highest bidder Settle call should succeed");
        Assert.equal(address(seller).balance, 100, "seller should receive funds after Settle");
    }

    function testPublicSettle() public {
        setupContracts({hasJudge: false});
        testAuction.finish(Auction.Outcome.SUCCESSFUL, address(highestBidder));
        Assert.isTrue(other.callSettle(), "Public Settle call should succeed");
        Assert.equal(address(seller).balance, 100, "seller should receive funds after Settle");
    }

    function testSettleWhenNoBidsPlacedWithJudge() public {
        setupContracts({hasJudge: true});
        testAuction.finish(Auction.Outcome.NOT_SUCCESSFUL, address(0));
        Assert.isFalse(judge.callSettle(), "Judge Settle call should not succeed");
    }

    function testSettleWhenNoBidsPlacedWithNoJudge() public {
        setupContracts({hasJudge: false});
        testAuction.finish(Auction.Outcome.NOT_SUCCESSFUL, address(0));
        Assert.isFalse(other.callSettle(), "Settle should not succeed with no bids.");
    }

    ////////////////////////////////////////////////////////////////////////
    //                        Refund tests                                //
    ////////////////////////////////////////////////////////////////////////

    function testEarlyRefund() public {
        setupContracts({hasJudge: true});
        Assert.isFalse(judge.callRefund(), "Refund with no declared highest bidder should be rejected");
    }

    function testUnauthorizedRefund() public {
        setupContracts({hasJudge: true});
        testAuction.finish(Auction.Outcome.NOT_SUCCESSFUL, address(highestBidder));
        Assert.isFalse(highestBidder.callRefund(), "Unauthorized refund call should be rejected");
        Assert.isFalse(other.callRefund(), "Unauthorized refund call should be rejected");
    }

    function testJudgeRefund() public {
        setupContracts({hasJudge: true});
        testAuction.finish(Auction.Outcome.NOT_SUCCESSFUL, address(highestBidder));
        Assert.isTrue(judge.callRefund(), "Judge refund call should succeed");
        Assert.equal(address(highestBidder).balance, 100, "Highest bidder should receive funds after refund.");
    }

    function testSellerRefund() public {
        setupContracts({hasJudge: true});
        testAuction.finish(Auction.Outcome.NOT_SUCCESSFUL, address(highestBidder));
        Assert.isTrue(seller.callRefund(), "Seller refund call should succeed");
        Assert.equal(address(highestBidder).balance, 100, "Highest bidder should receive funds after refund.");
    }

    function testPublicRefund() public {
        setupContracts({hasJudge: false});
        testAuction.finish(Auction.Outcome.NOT_SUCCESSFUL, address(highestBidder));
        Assert.isTrue(other.callRefund(), "Public refund call should succeed");
        Assert.equal(address(highestBidder).balance, 100, "Highest bidder should receive funds after refund.");
    }

    function testRefundWhenNoBidsPlaced() public {
        setupContracts({hasJudge: true});
        testAuction.finish(Auction.Outcome.NOT_SUCCESSFUL, address(0));
        Assert.isFalse(judge.callRefund(), "Refund call should not succeed, with no bids.");

        setupContracts({hasJudge: true});
        testAuction.finish(Auction.Outcome.NOT_SUCCESSFUL, address(0));
        Assert.isFalse(seller.callRefund(), "Refund call should not succeed, with no bids.");

        setupContracts({hasJudge: false});
        testAuction.finish(Auction.Outcome.NOT_SUCCESSFUL, address(0));
        Assert.isFalse(other.callRefund(), "Refund call should not succeed, with no bids.");
        Assert.isFalse(highestBidder.callRefund(),  "Refund call should not succeed, with no bids.");
    }
}

pragma solidity ^0.4.24;

import "./Auction.sol";

contract EnglishAuction is Auction {

  uint internal initialPrice;
  uint internal biddingPeriod;

  uint internal minimumPriceIncrement;

  address internal highestBidder;
  uint internal highestBid;
  uint internal lastBidTimestamp;

  constructor(
    address _sellerAddress,
    address _judgeAddress,
    Timer _timer,
    uint _initialPrice,
    uint _biddingPeriod,
    uint _minimumPriceIncrement
  ) public Auction(_sellerAddress, _judgeAddress, _timer) {
    initialPrice = _initialPrice;
    biddingPeriod = _biddingPeriod;
    minimumPriceIncrement = _minimumPriceIncrement;
    lastBidTimestamp = time();
  }



  function bid() public payable {
    require(IsBidEqualOrGreaterThenAskingPrice(), "Bid too low!");
    require(IsWithinBiddingPeriod(), "Bidding finished!");

    AcceptNewBid();
  }

  function getHighestBidder() public returns (address) {
    if (IsBiddingPeriodOver()) {
      if (IsReceivedAtLeastOneBid()) {
        finishAuction(Outcome.SUCCESSFUL, highestBidder);
      } else {
        finishAuction(Outcome.NOT_SUCCESSFUL, address(0));
      }
    }
    return highestBidderAddress;
  }



  function IsWithinBiddingPeriod() private view returns (bool) {
    uint elapsed_time = GetElapsedTimeFromLastBid();
    if (elapsed_time < biddingPeriod) {
      return true;
    }
    return false;
  }

  function IsBiddingPeriodOver() private view returns (bool) {
    uint elapsed_time = GetElapsedTimeFromLastBid();
    if (elapsed_time >= biddingPeriod) {
      return true;
    }
    return false;
  }


  function GetElapsedTimeFromLastBid() private view returns (uint) {
    return (time() - lastBidTimestamp);
  }

  function AcceptNewBid() private { //an ungraceful, but "transfer last" solution
    bool is_return_previous_bid = false;
    if (IsReceivedAtLeastOneBid()) {
      address previous_highest_bidder = highestBidder;
      uint previous_highest_bid = GetPreviousHighestBid();
      is_return_previous_bid = true;
    }

    highestBidder = msg.sender;
    highestBid = msg.value;
    lastBidTimestamp = time();

    if (is_return_previous_bid) {
      previous_highest_bidder.transfer(previous_highest_bid);
    }
  }

  function GetPreviousHighestBid() private view returns (uint) {
    return GetContractBalance() - msg.value;
  }

  function IsBidEqualOrGreaterThenAskingPrice() private view returns (bool) {
    uint asking_price = GetCurrentAskingPrice();
    if (msg.value >= asking_price) {
      return true;
    }
    return false;
  }

  function GetCurrentAskingPrice() private view returns (uint) {
    if (IsReceivedAtLeastOneBid()) {
      return highestBid + minimumPriceIncrement;
    }
    return initialPrice;
  }

  function IsReceivedAtLeastOneBid() private view returns (bool) {
    if (highestBid != 0) {
      if (highestBidder != address(0)) {
        return true;
      }
    }
    return false;
  }
}

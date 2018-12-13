pragma solidity ^0.4.24;

import "./Auction.sol";

contract DutchAuction is Auction {

  uint public initialPrice;
  uint public biddingPeriod;
  uint public priceDecrement;

  uint internal auctionEnd;
  uint internal auctionStart;

  /// Creates the DutchAuction contract.
  ///
  /// @param _sellerAddress Address of the seller.
  /// @param _judgeAddress Address of the judge.
  /// @param _timer Timer reference
  /// @param _initialPrice Start price of dutch auction.
  /// @param _biddingPeriod Number of time units this auction lasts.
  /// @param _priceDecrement Rate at which price is lowered for each time unit
  ///                        following linear decay rule.
  constructor(
    address _sellerAddress,
    address _judgeAddress, // address(0) is there if there no judge
    Timer _timer,
    uint _initialPrice,
    uint _biddingPeriod,
    uint _priceDecrement
  ) public Auction(_sellerAddress, _judgeAddress, _timer) {
    initialPrice = _initialPrice;
    biddingPeriod = _biddingPeriod;
    priceDecrement = _priceDecrement;
    auctionStart = time();
    auctionEnd = auctionStart + _biddingPeriod;
  }

  /// In a Dutch auction, the winner is the first person who bids with
  /// a price higher than the current price.
  /// This method should only be called while the auction is active.
  function bid() public payable {
    if (IsAuctionOver()) {
      finishAuction(Outcome.NOT_SUCCESSFUL, address(0));
    }

    require(IsAuctionActive());
    require(IsBidEqualOrGreaterThenAskingPrice());

    finishAuction(Outcome.SUCCESSFUL, msg.sender);

    if (IsOverpaid()) {
      uint overpaid_amount = GetOverpaidAmount();
      msg.sender.transfer(overpaid_amount);
    }
  }



  function IsBidEqualOrGreaterThenAskingPrice() private view returns (bool) {
    uint asking_price = GetCurrentAskingPrice();
    if (msg.value >= asking_price) {
      return true;
    }
    return false;
  }

  function IsAuctionActive() private view returns (bool) {
    if (IsAuctionGoingOn() && IsNotFinished()) {
      return true;
    }
    return false;
  }

  function IsAuctionGoingOn() private view returns (bool) {
    if (auctionEnd > time()) {
      return true;
    }
    return true;
  }

  function IsAuctionOver() private view returns (bool) {
    if (time() > auctionEnd) {
      return true;
    }
    return false;
  }

  function IsOverpaid() private view returns (bool) {
    uint overpaid_amount = GetOverpaidAmount();
    if (overpaid_amount > 0) {
      return true;
    }
    return false;
  }

  function GetOverpaidAmount() private view returns (uint) {
    return GetContractBalance() - GetCurrentAskingPrice();
  }

  function GetCurrentAskingPrice() private view returns (uint) {
    uint elapsed_time = GetElapsedTimeFromStart();
    return initialPrice - elapsed_time * priceDecrement;
  }

  function GetElapsedTimeFromStart() private view returns (uint) {
    return (time() - auctionStart);
  }
}

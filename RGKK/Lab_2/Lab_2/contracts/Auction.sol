pragma solidity ^0.4.24;

import "./Timer.sol";

/// This contract represents abstract auction.
contract Auction {

  /// Enum that shows the state of the auction.
  enum Outcome {
    NOT_FINISHED,
    NOT_SUCCESSFUL,
    SUCCESSFUL
  }

  Timer private timer;

  address private judgeAddress;
  address private sellerAddress;

  /// This should be set when the auction is over.
  address internal highestBidderAddress;
  Outcome internal outcome;

  constructor(
    address _sellerAddress,
    address _judgeAddress,
    Timer _timer
  ) public {
    timer = _timer;
    judgeAddress = _judgeAddress;
    sellerAddress = _sellerAddress;
    if (sellerAddress == address(0)) {
      sellerAddress = msg.sender;
    }
    outcome = Outcome.NOT_FINISHED;
  }

  /// Internal function used to finish an auction.
  /// Auction can finish in three different scenarios:
  /// 1.) Somebody won the auction and seller has the rights to receive the
  ///     funds to this contract.
  /// 2.) Auction finished with a highest bidder, but for some reason the
  ///     highest bidder does not have the right to claim the auction item
  ///     (e.g. minimal item price is not reached).
  /// 3.) Not one bid has been placed for an item.
  ///
  /// The values that should be used with this function call for each of
  /// the cases are:
  /// 1.) In the case of the first outcome, contract should call this method with
  ///     _highestBidderAddress != address(0) and _outcome should be equal to
  ///     Auction.Outcome.SUCCESSFUL.
  /// 2.) In the case of the second outcome, contract should call this method
  ///     with _outcome == AuctionOutcome.NOT_SUCCESSFUL and arbitrary value
  ///     for the _highestBidderAddress parameter.
  /// 3.) In the third case when not a single bid was placed, then this function
  ///     should be called with _outcome == NOT_SUCCESSFUL and
  ///     _highestBidderAddress should be equal to address(0).
  ///
  /// @param _outcome Outcome of the auction.
  /// @param _highestBidder Address of the highest bidder or address(0) if auction did not finish successfully.
  function finishAuction(Outcome _outcome, address _highestBidder) internal {
    require(_outcome != Outcome.NOT_FINISHED); // This should not happen.
    outcome = _outcome;
    highestBidderAddress = _highestBidder;
  }

  /// Settles the auction and sends the funds to the auction seller.
  /// This function can only be called when the auction has finished successfully.
  /// If no judge is specified for an auction then anybody can request
  /// the transfer of funds to the seller. If the judge is specified,
  /// then only the judge or highest bidder can transfer the funds to the seller.
  function settle() public {
    require(IsSuccessful());

    uint256 money;
    if (IsJudgeDefined()) {
      require(IsJudge() || IsHighestBidder());

      money = GetContractBalance();
      sellerAddress.transfer(money);
    } else {
      money = GetContractBalance();
      sellerAddress.transfer(money);
    }
  }

  // Returns the money to the highest bidder only in the case of unsuccessful
  // auction outcome. If the judge is specified then only the judge or
  // the seller can return the money to the highest bidder. If no judge is
  // specified then anybody should be able to request the transfer of funds
  // to the highest bidder (if such exists).
  function refund() public {
    require(IsUnsuccessful());
    require(IsHighestBidderDefined());

    uint256 money;
    if (IsJudgeDefined()) {
      require(IsJudge() || IsSeller());

      money = GetContractBalance();
      highestBidderAddress.transfer(money);
    } else {
      money = GetContractBalance();
      highestBidderAddress.transfer(money);
    }
  }



  function IsNotFinished() internal view returns (bool) {
    if (outcome == Outcome.NOT_FINISHED) {
      return true;
    }
    return false;
  }

  function IsSuccessful() private  view returns (bool) {
    if (outcome == Outcome.SUCCESSFUL) {
      return true;
    }
    return false;
  }
  function IsUnsuccessful() private view returns (bool) {
    if (outcome == Outcome.NOT_SUCCESSFUL) {
      return true;
    }
    return false;
  }

  function GetContractBalance() internal view returns (uint256) {
    return address(this).balance;
  }

  function IsJudgeDefined() private view returns (bool) {
    if (judgeAddress != address(0)) {
      return true;
    }
    return false;
  }

  function IsHighestBidderDefined() private view returns (bool) {
    if (highestBidderAddress != address(0)) {
      return true;
    }
    return false;
  }

  function IsJudge() private view returns (bool) {
    if (judgeAddress == msg.sender) {
      return true;
    }
    return false;
  }

  function IsHighestBidder() private view returns (bool) {
    if (highestBidderAddress == msg.sender) {
      return true;
    }
    return false;
  }

  function IsSeller() private view returns (bool) {
    if (sellerAddress == msg.sender) {
      return true;
    }
    return false;
  }



  // This is provided for testing
  // You should use this instead of block.number directly
  // You should not modify this function.
  function time() public view returns (uint) {
      return timer.getTime();
  }

  /// Function that returns highest bidder address or address(0) if
  /// auction is not yet over.
  function getHighestBidder() public returns (address) {
      return highestBidderAddress;
  }
}

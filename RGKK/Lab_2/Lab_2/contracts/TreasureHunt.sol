pragma solidity ^0.4.24;

contract TreasureHuntSolution {

    function getSolution() public pure returns (uint256) {
        return 42;
    }
}

contract TreasureHunt {

    uint256 secret;
    uint256 lastTimePlayed;

    address owner;
    uint256 price; // This is how much it costs to open treasure

    PlayerGuess[] guesses;

    struct PlayerGuess {
        address playerAddress;
        uint256 guess;
    }

    function() public payable {}

    constructor(uint256 _price) public payable {
        owner = msg.sender;
        price = _price;
        lastTimePlayed = 0;
        string memory message = "The answer to life,  the universe and everything.";
        bytes memory encodedMsg = bytes(message);
        secret = uint(encodedMsg[42]) ^ 83;
    }

    function openTreasure(uint256 guess) public payable {
        require(msg.value >= price);

        // Log player game
        PlayerGuess playerGuess;
        playerGuess.playerAddress = msg.sender;
        playerGuess.guess = guess;
        guesses.push(playerGuess);

        if (guess == secret) {
            // You guessed correctly :D
            msg.sender.transfer(address(this).balance);
        }

        lastTimePlayed = now;
    }

    function kill() public {
        if (msg.sender == owner) {
            // Redeem funds from contract and remove it from the blockchain.
            selfdestruct(msg.sender);
        }
    }
}

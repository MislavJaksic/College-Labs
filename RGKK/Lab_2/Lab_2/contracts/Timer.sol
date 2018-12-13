pragma solidity ^0.4.24;

// Simple contract that serves as time provider.
interface Timer {

    function getTime() external view returns (uint);
}

/// Implementation of Timer contract that provides the user with
/// system time (UNIX time).
contract UnixTimer is Timer {

    function getTime() external view returns (uint) {
        return now;
    }
}

/// Implementation of Timer contract which allows user to programmatically
/// manipulate time. MockTimes is used by other objects which depend on
/// time and in order to test the implementation of those contracts it
/// is useful to be able to set the time as we like. This pattern of mocking
/// a component should be always performed as it provides the ability to
/// test components independently of each other, meaning that tests are
/// easier to write and reason about. You may notice that you already
/// have all tests written out for each contract you need to implement.
/// This way of programming (first write tests then implementation) is
/// called Test Driven Development and it fits into smart contract programming
/// really well. This is because smart contracts are in essence just state machines,
/// and usually they do not have too many states - so it is easy to write tests
/// for them, and sometimes possible to write a test for all possible states.
/// (You should strive to write tests that test all possible states and
/// transitions, especially when writing smart contracts which can not have
/// a bug or security exploit).
contract MockTimer is Timer {

    uint time;
    uint startTime;
    address owner;

    // constructor
    constructor(uint _startTime) public {
        owner = msg.sender;
        time = _startTime;
        startTime = _startTime;
    }

    function getTime() public view returns (uint) {
        return time;
    }

    function resetTime() public ownerOnly {
        time = startTime;
    }

    function setTime(uint _newTime) public ownerOnly {
        time = _newTime;
    }

    function offsetTime(uint _offset) public ownerOnly {
        time += _offset;
    }
    
    modifier ownerOnly {
        if (msg.sender != owner) {
            revert();
        }
        _;
    }
}

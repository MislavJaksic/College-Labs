#!/bin/bash

# Stars server with 1000000000000 gasLimit; 10 gasPrice and UnlimitedContractSize (Needed for tests).
# This starts local node in current terminal session. You will need new terminal session for running
# Truffle commands.
./node_modules/.bin/ganache-cli -l 1000000000000 -g 10 --allowUnlimitedContractSize

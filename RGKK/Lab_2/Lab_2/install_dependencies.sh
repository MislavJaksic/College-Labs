#!/bin/bash

if [[ ! -d "node_modules" ]]; then
    # If no node_models are present than install them
    npm install truffle mocha web3 ganache-cli ethereumjs-abi ethereumjs-util bignumber
fi
ABI = '''[
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "vrfCoordinatorV2",
        "type": "address"
      },
      {
        "internalType": "bytes32",
        "name": "_gasLane",
        "type": "bytes32"
      },
      {
        "internalType": "uint64",
        "name": "subscriptionId",
        "type": "uint64"
      },
      {
        "internalType": "uint32",
        "name": "callbackGasLimit",
        "type": "uint32"
      },
      {
        "internalType": "uint256",
        "name": "_playersNeeded",
        "type": "uint256"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "have",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "want",
        "type": "address"
      }
    ],
    "name": "OnlyCoordinatorCanFulfill",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "Raffle__NotOpen",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "Raffle__TransferFailed",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "currentBalance",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "noPlayers",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "RaffleState",
        "type": "uint256"
      }
    ],
    "name": "Raffle__upkeepNotNeeded",
    "type": "error"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "player",
        "type": "address"
      }
    ],
    "name": "RaffleEnter",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "requestId",
        "type": "uint256"
      }
    ],
    "name": "RequestedRaffleWinner",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "winner",
        "type": "address"
      }
    ],
    "name": "WinnerPicked",
    "type": "event"
  },
  {
    "inputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "name": "checkUpkeep",
    "outputs": [
      {
        "internalType": "bool",
        "name": "upkeepNeeded",
        "type": "bool"
      },
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "enterRaffle",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "fund",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getLatestTimestamp",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getNumWords",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getNumberOfPlayers",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "playerId",
        "type": "uint256"
      }
    ],
    "name": "getPlayer",
    "outputs": [
      {
        "internalType": "address payable",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getRaffleState",
    "outputs": [
      {
        "internalType": "enum Raffle.RaffleState",
        "name": "",
        "type": "uint8"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getRecentWinner",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getRequestConfirmations",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "name": "performUpkeep",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "requestId",
        "type": "uint256"
      },
      {
        "internalType": "uint256[]",
        "name": "randomWords",
        "type": "uint256[]"
      }
    ],
    "name": "rawFulfillRandomWords",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_playersNeeded",
        "type": "uint256"
      }
    ],
    "name": "updatePlayersNeeded",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]'''

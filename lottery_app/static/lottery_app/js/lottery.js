let web3;
let userAccount;
let contract;

const CONTRACT_ADDRESS = "0xdC3A27d2421b08B5CC7aAD9F744e20C2CE583A79";
const ABI =[
	{
		"inputs": [],
		"name": "selectwinner",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"stateMutability": "payable",
		"type": "receive"
	},
	{
		"inputs": [],
		"name": "getBalance",
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
		"name": "manager",
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
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "participants",
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
		"name": "random",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
];

// Initialize Web3
async function initWeb3() {
    if (window.ethereum) {
        web3 = new Web3(window.ethereum);
        try {
            // Request account access
            await window.ethereum.request({ method: 'eth_requestAccounts' });
            
            // Check network ID (example for Ropsten)
            const chainId = await web3.eth.getChainId();
            if (chainId !== 11155111) { // Change this to your network ID
                Swal.fire({
                    title: "Wrong Network",
                    text: "Please connect to the correct Ethereum network",
                    icon: "warning"
                });
                return;
            }
            
            contract = new web3.eth.Contract(ABI, CONTRACT_ADDRESS);
            updateUI();
        } catch (error) {
            console.error("User denied account access", error);
        }
    } else {
        console.log("Non-Ethereum browser detected");
        Swal.fire("MetaMask Required", "Please install MetaMask to use this dApp", "warning");
    }
}

// Update UI with contract data
async function updateUI() {
    try {
        const accounts = await web3.eth.getAccounts();
        if (accounts.length === 0) {
            console.log("No accounts found");
            return;
        }
        
        userAccount = accounts[0];
        document.getElementById("wallet-address").innerText = `Connected: ${userAccount.substring(0, 6)}...${userAccount.substring(38)}`;
        
        // Add timeout for contract calls
        const timeoutPromise = new Promise((_, reject) => 
            setTimeout(() => reject(new Error('Timeout exceeded')), 10000)
        );

        // Wrap contract calls with Promise.race
        const manager = await Promise.race([
            contract.methods.manager().call(),
            timeoutPromise
        ]);
        document.getElementById("manager-address").innerText = `Manager: ${manager}`;
        
        const balance = await Promise.race([
            contract.methods.getBalance().call(),
            timeoutPromise
        ]);
        const etherBalance = web3.utils.fromWei(balance, 'ether');
        document.getElementById("contract-balance").innerText = `Contract Balance: ${etherBalance} ETH`;
        
        await updateParticipants();
    } catch (error) {
        console.error("UI update error:", error);
        Swal.fire("Error", "Couldn't fetch contract data. Please try again.", "error");
    }
}

// Get all participants
async function updateParticipants() {
    try {
        // First try to get count directly if available
        let participantCount;
        try {
            participantCount = await contract.methods.getParticipantsCount().call();
        } catch {
            // Fallback to iteration if direct count not available
            participantCount = await getParticipantCount();
        }
        
        document.getElementById("participant-count").innerText = `Participants: ${participantCount}`;
        
        const participantsList = document.getElementById("participants-list");
        participantsList.innerHTML = "";
        
        // Limit display to first 50 participants for performance
        const displayCount = Math.min(participantCount, 50);
        for (let i = 0; i < displayCount; i++) {
            const participant = await contract.methods.participants(i).call();
            const li = document.createElement("li");
            li.className = "list-group-item";
            li.textContent = `${i+1}. ${participant}`;
            participantsList.appendChild(li);
        }
        
        if (participantCount > 50) {
            const li = document.createElement("li");
            li.className = "list-group-item text-muted";
            li.textContent = `...and ${participantCount - 50} more`;
            participantsList.appendChild(li);
        }
    } catch (error) {
        console.error("Error loading participants:", error);
        document.getElementById("participant-count").innerText = "Could not load participants";
    }
}
// Get participant count (helper function)

async function getParticipantCount() {
    try {
        // Alternative approach if the above doesn't work
        let i = 0;
        while (true) {
            try {
                await contract.methods.participants(i).call();
                i++;
            } catch (e) {
                return i;
            }
        }
    } catch (error) {
        console.error("Error getting participant count:", error);
        return 0;
    }
}

// Enter lottery function
async function enterLottery() {
    const amount = web3.utils.toWei("0.002", "ether");
    try {
        const gasEstimate = await contract.methods.enter().estimateGas({
            from: userAccount,
            value: amount
        });
        
        await contract.methods.enter().send({
            from: userAccount,
            value: amount,
            gas: Math.floor(gasEstimate * 1.2) // Add 20% buffer
        });
        
        Swal.fire("Success!", "You've entered the lottery!", "success");
        await updateParticipants();
        await updateUI();
    } catch (error) {
        console.error("Entry error:", error);
        Swal.fire("Error", error.message, "error");
    }
}

// Select winner function (only manager can call this)
async function selectWinner() {
    try {
        await contract.methods.selectwinner().send({ from: userAccount });
        Swal.fire("Winner Selected!", "The lottery winner has been chosen!", "success");
        await updateUI();
        await updateParticipants();
    } catch (error) {
        Swal.fire("Error", error.message, "error");
    }
}

// Get random number (view function)
async function getRandomNumber() {
    try {
        const randomNum = await contract.methods.random().call();
        document.getElementById("random-number").innerText = `Random Number: ${randomNum}`;
    } catch (error) {
        Swal.fire("Error", error.message, "error");
    }
}

// Initialize when page loads
window.addEventListener('load', async () => {
    await initWeb3();
});
console.log("Contract address:", CONTRACT_ADDRESS);
console.log("Using ABI:", ABI);

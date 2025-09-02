#!/bin/bash
# phase3-web3-demo.sh - Create Web3 demo site

set -euo pipefail

echo "🌐 PHASE 3: Web3 Demo Site Development"

cd apps/web3-demo

# Initialize Next.js Web3 app
cat > package.json << 'EOF'
{
  "name": "@perswade/web3-demo",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev -p 3001",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "15.4.2",
    "react": "19.1.0",
    "react-dom": "19.1.0",
    "wagmi": "^2.0.0",
    "viem": "^2.0.0",
    "@rainbow-me/rainbowkit": "^2.0.0",
    "ethers": "^6.0.0",
    "@perswade/core": "workspace:*",
    "@perswade/transcription": "workspace:*"
  }
}
EOF

# Create Web3 config
cat > src/config/web3.ts << 'EOF'
/*
 * Copyright (c) 2025 VT Infinite, Inc d/b/a Perswade.xyz
 * Licensed under MIT License (see LICENSE file)
 */

import { getDefaultConfig } from '@rainbow-me/rainbowkit';
import { mainnet, polygon, arbitrum, base } from 'wagmi/chains';

export const config = getDefaultConfig({
  appName: 'Perswade Web3 Demo',
  projectId: process.env.NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID!,
  chains: [mainnet, polygon, arbitrum, base],
  ssr: true,
});
EOF

# Create main demo page
cat > pages/index.tsx << 'EOF'
/*
 * Copyright (c) 2025 VT Infinite, Inc d/b/a Perswade.xyz
 * Licensed under MIT License (see LICENSE file)
 */

import { ConnectButton } from '@rainbow-me/rainbowkit';
import { useAccount } from 'wagmi';
import { useState, useEffect } from 'react';
import { TranscriptionService } from '@perswade/transcription';
import { C2PSEngine } from '@perswade/core';

export default function Web3Demo() {
  const { address, isConnected } = useAccount();
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [c2psScore, setC2psScore] = useState(null);

  const startDemo = async () => {
    if (!isConnected) {
      alert('Please connect your wallet first');
      return;
    }

    const transcriptionService = new TranscriptionService(
      process.env.NEXT_PUBLIC_ASSEMBLYAI_KEY!
    );

    const c2psEngine = new C2PSEngine();

    await transcriptionService.startRealtimeTranscription(
      (partial) => setTranscript(partial),
      (final) => {
        const score = c2psEngine.analyzeTranscript(final);
        setC2psScore(score);
        // Record on blockchain
        recordOnChain(address!, score);
      }
    );

    setIsRecording(true);
  };

  const recordOnChain = async (address: string, score: any) => {
    // Implement smart contract interaction
    console.log('Recording score on-chain for:', address, score);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      <div className="backdrop-blur-xl bg-white/10 min-h-screen">
        <nav className="p-6 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-white">
            Perswade <span className="text-purple-400">Web3</span>
          </h1>
          <ConnectButton />
        </nav>

        <main className="container mx-auto px-6 py-12">
          <div className="text-center mb-12">
            <h2 className="text-5xl font-bold text-white mb-4">
              AI Sales Intelligence on the Blockchain
            </h2>
            <p className="text-xl text-gray-300">
              Real-time C²PS analysis with on-chain verification
            </p>
          </div>

          {isConnected ? (
            <div className="bg-white/20 backdrop-blur-lg rounded-2xl p-8 shadow-2xl">
              <button
                onClick={startDemo}
                disabled={isRecording}
                className="w-full py-4 px-8 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-xl font-bold text-xl hover:from-purple-700 hover:to-blue-700 transition-all"
              >
                {isRecording ? 'Recording...' : 'Start Sales Call Demo'}
              </button>

              {transcript && (
                <div className="mt-8 p-6 bg-black/30 rounded-xl">
                  <h3 className="text-white font-bold mb-2">Live Transcript:</h3>
                  <p className="text-gray-300">{transcript}</p>
                </div>
              )}

              {c2psScore && (
                <div className="mt-8 grid grid-cols-2 gap-4">
                  <div className="bg-gradient-to-r from-green-500/20 to-blue-500/20 p-4 rounded-xl">
                    <h4 className="text-white font-bold">Credibility</h4>
                    <p className="text-3xl text-white">{c2psScore.credibility}/10</p>
                  </div>
                  <div className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 p-4 rounded-xl">
                    <h4 className="text-white font-bold">Commonality</h4>
                    <p className="text-3xl text-white">{c2psScore.commonality}/10</p>
                  </div>
                  <div className="bg-gradient-to-r from-yellow-500/20 to-orange-500/20 p-4 rounded-xl">
                    <h4 className="text-white font-bold">Problem</h4>
                    <p className="text-3xl text-white">{c2psScore.problem}/10</p>
                  </div>
                  <div className="bg-gradient-to-r from-cyan-500/20 to-teal-500/20 p-4 rounded-xl">
                    <h4 className="text-white font-bold">Solution</h4>
                    <p className="text-3xl text-white">{c2psScore.solution}/10</p>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center">
              <p className="text-xl text-gray-300 mb-8">
                Connect your wallet to access the demo
              </p>
              <div className="inline-block p-8 bg-white/10 backdrop-blur-lg rounded-2xl">
                <ConnectButton />
              </div>
            </div>
          )}

          <div className="mt-16 grid grid-cols-3 gap-8">
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6">
              <h3 className="text-xl font-bold text-white mb-2">🔐 Token-Gated</h3>
              <p className="text-gray-300">
                Hold PERSWADE tokens for premium features
              </p>
            </div>
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6">
              <h3 className="text-xl font-bold text-white mb-2">📜 On-Chain Proof</h3>
              <p className="text-gray-300">
                Verifiable sales performance records
              </p>
            </div>
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6">
              <h3 className="text-xl font-bold text-white mb-2">🌐 Decentralized</h3>
              <p className="text-gray-300">
                IPFS storage for call recordings
              </p>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
EOF

cd ../..

# Create smart contracts
cat > contracts/PerswadeCore.sol << 'EOF'
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PerswadeCore {
    struct C2PSScore {
        uint8 credibility;
        uint8 commonality;
        uint8 problem;
        uint8 solution;
        uint8 overall;
        uint256 timestamp;
        string ipfsHash;
    }

    mapping(address => C2PSScore[]) public userScores;
    mapping(address => uint256) public salesRepScore;

    event ScoreRecorded(
        address indexed user,
        uint8 overall,
        uint256 timestamp
    );

    function recordScore(
        uint8 _credibility,
        uint8 _commonality,
        uint8 _problem,
        uint8 _solution,
        string memory _ipfsHash
    ) external {
        uint8 overall = (_credibility + _commonality + _problem + _solution) / 4;
        
        C2PSScore memory newScore = C2PSScore({
            credibility: _credibility,
            commonality: _commonality,
            problem: _problem,
            solution: _solution,
            overall: overall,
            timestamp: block.timestamp,
            ipfsHash: _ipfsHash
        });

        userScores[msg.sender].push(newScore);
        
        // Update reputation
        salesRepScore[msg.sender] = (salesRepScore[msg.sender] * 9 + overall * 10) / 10;
        
        emit ScoreRecorded(msg.sender, overall, block.timestamp);
    }

    function getUserScores(address user) external view returns (C2PSScore[] memory) {
        return userScores[user];
    }
}
EOF

echo "✅ Web3 demo site created"
echo "✅ PHASE 3 COMPLETE: Web3 Demo Site"
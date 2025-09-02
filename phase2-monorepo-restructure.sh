#!/bin/bash
# phase2-monorepo-restructure.sh - Transform to monorepo structure

set -euo pipefail

echo "📦 PHASE 2: Monorepo Restructure"

# Create new directory structure
mkdir -p packages/{core,transcription,ml-models,api}/{src,tests}
mkdir -p apps/{web3-demo,dashboard}/{components,pages,hooks}
mkdir -p contracts docs examples .github/workflows

# Move existing code to new structure
echo "🔄 Migrating existing code..."

# Backend → API package
if [ -d "backend" ]; then
    cp -r backend/* packages/api/ 2>/dev/null || true
fi

# Frontend → Dashboard app
if [ -d "frontend" ]; then
    cp -r frontend/* apps/dashboard/ 2>/dev/null || true
fi

# Extract AssemblyAI code
cat > packages/transcription/package.json << 'EOF'
{
  "name": "@perswade/transcription",
  "version": "1.0.0",
  "description": "AssemblyAI real-time transcription service",
  "main": "src/index.js",
  "scripts": {
    "test": "jest",
    "build": "tsc"
  },
  "dependencies": {
    "assemblyai": "^4.0.0"
  }
}
EOF

# Create AssemblyAI service
cat > packages/transcription/src/index.ts << 'EOF'
/*
 * Copyright (c) 2025 VT Infinite, Inc d/b/a Perswade.xyz
 * Licensed under MIT License (see LICENSE file)
 */

import { AssemblyAI, RealtimeTranscriber } from 'assemblyai';

export class TranscriptionService {
  private client: AssemblyAI;
  private transcriber?: RealtimeTranscriber;

  constructor(apiKey: string) {
    this.client = new AssemblyAI({ apiKey });
  }

  async startRealtimeTranscription(
    onPartialTranscript: (text: string) => void,
    onFinalTranscript: (text: string) => void
  ) {
    this.transcriber = this.client.realtime.transcriber({
      sampleRate: 16000,
      wordBoost: ['C2PS', 'credibility', 'commonality', 'problem', 'solution'],
    });

    this.transcriber.on('PartialTranscript', (transcript) => {
      onPartialTranscript(transcript.text);
    });

    this.transcriber.on('FinalTranscript', (transcript) => {
      onFinalTranscript(transcript.text);
    });

    await this.transcriber.connect();
  }

  async stopTranscription() {
    await this.transcriber?.close();
  }
}
EOF

# Create C²PS core engine
cat > packages/core/src/c2ps-engine.ts << 'EOF'
/*
 * Copyright (c) 2025 VT Infinite, Inc d/b/a Perswade.xyz
 * Licensed under MIT License (see LICENSE file)
 */

export interface C2PSScore {
  credibility: number;
  commonality: number;
  problem: number;
  solution: number;
  overall: number;
  conversionProbability: number;
}

export class C2PSEngine {
  analyzeTranscript(transcript: string): C2PSScore {
    // Implement C²PS analysis logic
    const credibility = this.analyzeCredibility(transcript);
    const commonality = this.analyzeCommonality(transcript);
    const problem = this.analyzeProblem(transcript);
    const solution = this.analyzeSolution(transcript);
    
    const overall = (credibility + commonality + problem + solution) / 4;
    const conversionProbability = this.predictConversion(overall);
    
    return {
      credibility,
      commonality,
      problem,
      solution,
      overall,
      conversionProbability
    };
  }

  private analyzeCredibility(text: string): number {
    // Authority markers detection
    const authorityMarkers = [
      'research shows', 'studies indicate', 'data suggests',
      'in my experience', 'we\'ve helped', 'our clients'
    ];
    
    let score = 5; // baseline
    authorityMarkers.forEach(marker => {
      if (text.toLowerCase().includes(marker)) score += 0.5;
    });
    
    return Math.min(10, score);
  }

  private analyzeCommonality(text: string): number {
    // Rapport and alignment detection
    const rapportMarkers = [
      'I understand', 'absolutely', 'exactly right',
      'great point', 'I agree', 'similar situation'
    ];
    
    let score = 5;
    rapportMarkers.forEach(marker => {
      if (text.toLowerCase().includes(marker)) score += 0.5;
    });
    
    return Math.min(10, score);
  }

  private analyzeProblem(text: string): number {
    // Pain point extraction
    const painMarkers = [
      'challenge', 'issue', 'problem', 'struggle',
      'difficult', 'frustrating', 'pain point', 'bottleneck'
    ];
    
    let score = 5;
    painMarkers.forEach(marker => {
      if (text.toLowerCase().includes(marker)) score += 0.5;
    });
    
    return Math.min(10, score);
  }

  private analyzeSolution(text: string): number {
    // Value proposition matching
    const valueMarkers = [
      'solution', 'benefit', 'improve', 'increase',
      'reduce', 'save', 'optimize', 'transform'
    ];
    
    let score = 5;
    valueMarkers.forEach(marker => {
      if (text.toLowerCase().includes(marker)) score += 0.5;
    });
    
    return Math.min(10, score);
  }

  private predictConversion(overallScore: number): number {
    // Simple logistic function for conversion probability
    return 1 / (1 + Math.exp(-0.5 * (overallScore - 5)));
  }
}
EOF

# Root package.json for monorepo
cat > package.json << 'EOF'
{
  "name": "perswade",
  "version": "1.0.0",
  "description": "Open Source AI-Powered Sales Intelligence Platform",
  "private": true,
  "workspaces": [
    "packages/*",
    "apps/*"
  ],
  "scripts": {
    "dev": "concurrently \"npm run dev:api\" \"npm run dev:dashboard\" \"npm run dev:demo\"",
    "dev:api": "cd packages/api && npm run dev",
    "dev:dashboard": "cd apps/dashboard && npm run dev",
    "dev:demo": "cd apps/web3-demo && npm run dev",
    "build": "npm run build:packages && npm run build:apps",
    "build:packages": "npm run build --workspaces --if-present",
    "build:apps": "npm run build --workspace=apps/*",
    "test": "npm run test --workspaces --if-present",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "format": "prettier --write \"**/*.{js,jsx,ts,tsx,json,md}\""
  },
  "devDependencies": {
    "concurrently": "^8.2.0",
    "eslint": "^8.50.0",
    "prettier": "^3.0.0",
    "typescript": "^5.2.0"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  }
}
EOF

echo "✅ Monorepo structure created"
echo "✅ PHASE 2 COMPLETE: Monorepo Restructure"
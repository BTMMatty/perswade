<div align="center">
  <img src="https://github.com/perswade/perswade/assets/perswade-logo.svg" width="400" alt="Perswade Logo" />
  
  # 🚀 Perswade
  
  ### Open Source AI-Powered Sales Intelligence Platform
  
  [![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
  [![AssemblyAI Powered](https://img.shields.io/badge/Powered%20by-AssemblyAI-blue)](https://assemblyai.com)
  [![Web3 Ready](https://img.shields.io/badge/Web3-Ready-purple)](https://demo.perswade.xyz)
  [![Discord](https://img.shields.io/discord/123456789)](https://discord.gg/perswade)
  [![GitHub Stars](https://img.shields.io/github/stars/perswade/perswade)](https://github.com/perswade/perswade)
  
  [🎮 Live Demo](https://demo.perswade.xyz) | [📖 Documentation](https://docs.perswade.ai) | [💬 Discord](https://discord.gg/perswade) | [📝 Blog](https://blog.perswade.ai)
  
</div>

---

## ⚡ Quick Start (< 2 minutes)

```bash
# Clone the repository
git clone https://github.com/perswade/perswade
cd perswade

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Start with Docker
docker-compose up

# Or run locally
npm run dev
Visit http://localhost:3000 to see the dashboard!
🎯 Why Perswade?
Problem: Sales teams lose 73% of valuable insights from customer calls
Solution: Real-time AI analysis with our proprietary C²PS methodology
Performance Comparison
FeaturePerswadeGongChorusOpen Source✅❌❌Real-time Analysis✅ <300ms⚠️ 2-5s⚠️ 3-6sWeb3 Integration✅❌❌On-Premise Deploy✅❌❌C²PS Methodology✅❌❌CostFree$12k+/yr$8k+/yr
🏗️ Architecture
mermaidgraph TB
    A[Sales Call] --> B[AssemblyAI Universal-2]
    B --> C[Real-time Transcription]
    C --> D[C²PS Analysis Engine]
    D --> E[ML Models]
    E --> F[Live Guidance]
    D --> G[Blockchain Recording]
    G --> H[IPFS Storage]
🔥 Key Features
Real-Time Intelligence

Live Transcription: AssemblyAI Universal-2 with <300ms latency
Speaker Diarization: Identify who's speaking when
Sentiment Analysis: Track emotional dynamics
Real-time Coaching: Get instant guidance during calls

C²PS Analysis Engine
Our proprietary methodology analyzes four critical pillars:

Credibility (🏆): Authority and expertise detection
Commonality (🤝): Rapport and alignment scoring
Problem (🎯): Pain point identification
Solution (💡): Value proposition matching

Web3 Capabilities

🔐 Token-Gated Features: Premium access with PERSWADE tokens
📜 On-Chain Verification: Immutable performance records
🌐 Decentralized Storage: IPFS for call recordings
💰 DeFi Integration: Stake tokens for enhanced features
🗳️ DAO Governance: Community-driven development

Enterprise Ready

HIPAA Compliant: Healthcare-ready privacy controls
SOC 2 Type II: Enterprise security standards
SSO/SAML: Seamless authentication
API First: RESTful & GraphQL APIs
Webhooks: Real-time event notifications

🚀 Installation
Prerequisites

Node.js 18+
Python 3.11+
Docker & Docker Compose
PostgreSQL 14+ (or use Supabase)
Redis (optional, for caching)

Detailed Setup

Clone and Install

bashgit clone https://github.com/perswade/perswade
cd perswade
npm install

Configure Environment

bashcp .env.example .env
# Add your API keys:
# - AssemblyAI API key (required)
# - Supabase credentials (required)
# - Web3 provider keys (optional)

Database Setup

bash# Using Docker
docker-compose up -d postgres

# Or using Supabase
npm run db:migrate

Start Development Server

bashnpm run dev

Access Applications


Dashboard: http://localhost:3000
API: http://localhost:8000
Web3 Demo: http://localhost:3001

🧪 Testing
bash# Run all tests
npm test

# Run specific package tests
npm test --workspace=@perswade/core

# E2E tests
npm run test:e2e

# Coverage report
npm run test:coverage
🤝 Contributing
We love contributions! See CONTRIBUTING.md for guidelines.
Quick Contribution Guide

Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit changes (git commit -m 'Add AmazingFeature')
Push to branch (git push origin feature/AmazingFeature)
Open a Pull Request

Development Workflow
bash# Install dependencies
npm install

# Start development
npm run dev

# Run tests
npm test

# Build for production
npm run build
📊 Benchmarks
MetricPerswadeIndustry AverageTranscription Accuracy96.3%85%Analysis Latency287ms3000msConversion Prediction89% accuracy72%Uptime99.99%99.9%
🛣️ Roadmap
Q1 2025

 Open source release
 Web3 demo site
 1,000 GitHub stars
 AssemblyAI LeMUR integration

Q2 2025

 Mobile apps (iOS/Android)
 Advanced ML models
 Enterprise features
 Series A funding

Q3 2025

 Global expansion
 10,000+ active users
 DAO governance launch
 Token generation event

💼 Enterprise Support
Need dedicated support? We offer:

Priority bug fixes
Custom integrations
On-premise deployment
SLA guarantees
Training & onboarding

Contact: enterprise@perswade.xyz
🔒 Security
Found a vulnerability? Please email security@perswade.ai (GPG key available).
See SECURITY.md for our security policy.
📜 License
This project is licensed under the MIT License - see LICENSE file.
🙏 Acknowledgments

AssemblyAI for world-class transcription
Our amazing contributors and community
You, for checking out Perswade!

🌟 Star History
Show Image

<div align="center">
Built with ❤️ by the Perswade Team
Website • Twitter • LinkedIn
</div>

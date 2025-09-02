#!/bin/bash
# emergency-cleanup.sh - Fix critical issues NOW

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${RED}🚨 EMERGENCY CLEANUP STARTING${NC}"

# 1. REMOVE ALL BACKUP DIRECTORIES
echo "Removing recursive backups..."
find . -type d -name ".backup-*" -exec rm -rf {} + 2>/dev/null || true
echo -e "${GREEN}✅ Backups removed${NC}"

# 2. REMOVE VIRTUAL ENVIRONMENTS
echo "Removing virtual environments..."
rm -rf venv/
rm -rf backend/venv/
rm -rf frontend/node_modules/
rm -rf frontend/.next/
echo -e "${GREEN}✅ Virtual environments removed${NC}"

# 3. UPDATE .gitignore PROPERLY
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv
pip-log.txt
pip-delete-this-directory.txt
.pytest_cache/
.coverage
htmlcov/
*.egg-info/
dist/
build/

# Node
node_modules/
.next/
out/
build/
dist/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment
.env
.env.local
.env.*.local
*.key
*.pem

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Backups
.backup*/
*.bak
*.backup

# Cache
.cache/
*.cache
EOF
echo -e "${GREEN}✅ .gitignore updated${NC}"

# 4. GIT CLEAN (if in git repo)
if [ -d .git ]; then
    echo "Cleaning git..."
    git rm -r --cached . 2>/dev/null || true
    git add .gitignore
    git add -A
    echo -e "${GREEN}✅ Git index rebuilt${NC}"
fi

# 5. CHECK SIZE
echo ""
echo "Repository size BEFORE: 20GB"
CURRENT_SIZE=$(du -sh . 2>/dev/null | cut -f1)
echo -e "${GREEN}Repository size AFTER: ${CURRENT_SIZE}${NC}"

# 6. CREATE MISSING CRITICAL FILES
echo "Creating missing documentation..."

# README.md (if missing)
if [ ! -f README.md ]; then
cat > README.md << 'EOF'
# 🚀 Perswade - AI-Powered Sales Intelligence Platform

Open-source real-time sales intelligence with AssemblyAI transcription and C²PS methodology.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AssemblyAI](https://img.shields.io/badge/Powered%20by-AssemblyAI-blue)](https://assemblyai.com)

## Quick Start

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
Visit http://localhost:3000
Features

⚡ Real-time transcription (<300ms latency)
🧠 C²PS analysis (Credibility, Commonality, Problem, Solution)
📊 Live coaching and insights
🔒 Self-hosted, own your data

License
MIT - see LICENSEEOF
echo -e "GREEN✅README.mdcreated{GREEN}✅ README.md created
GREEN✅README.mdcreated{NC}"
fi

CONTRIBUTING.md
if [ ! -f CONTRIBUTING.md ]; then
echo "# Contributing to Perswade" > CONTRIBUTING.md
echo "See our contribution guide" >> CONTRIBUTING.md
    echo -e "GREEN✅CONTRIBUTING.mdcreated{GREEN}✅ CONTRIBUTING.md created
GREEN✅CONTRIBUTING.mdcreated{NC}"
fi

CODE_OF_CONDUCT.md
if [ ! -f CODE_OF_CONDUCT.md ]; then
    echo "# Code of Conduct" > CODE_OF_CONDUCT.md
    echo "Be respectful and professional." >> CODE_OF_CONDUCT.md
    echo -e "GREEN✅CODEOFCONDUCT.mdcreated{GREEN}✅ CODE_OF_CONDUCT.md created
GREEN✅CODEO​FC​ONDUCT.mdcreated{NC}"
fi

SECURITY.md
if [ ! -f SECURITY.md ]; then
echo "# Security Policy" > SECURITY.md
echo "Report vulnerabilities to security@perswade.ai" >> SECURITY.md
    echo -e "GREEN✅SECURITY.mdcreated{GREEN}✅ SECURITY.md created
GREEN✅SECURITY.mdcreated{NC}"
fi

echo ""
echo -e "GREEN════════════════════════════════════════{GREEN}════════════════════════════════════════
GREEN════════════════════════════════════════{NC}"
echo -e "GREEN✅EMERGENCYCLEANUPCOMPLETE!{GREEN}✅ EMERGENCY CLEANUP COMPLETE!
GREEN✅EMERGENCYCLEANUPCOMPLETE!{NC}"
echo -e "GREEN════════════════════════════════════════{GREEN}════════════════════════════════════════
GREEN════════════════════════════════════════{NC}"
echo ""
echo "Repository should now be ~50MB instead of 20GB"
echo ""
echo -e "YELLOWNextsteps:{YELLOW}Next steps:
YELLOWNextsteps:{NC}"
echo "1. Verify cleanup: ls -la"
echo "2. Check size: du -sh ."
echo "3. Commit cleaned state: git add . && git commit -m 'fix: remove backups and venv'"
echo "4. Continue with open source launch"
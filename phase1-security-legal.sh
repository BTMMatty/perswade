#!/bin/bash
# phase1-security-legal.sh - Remove sensitive data, add MIT license, copyright headers

set -euo pipefail

echo "🔐 PHASE 1: Security & Legal Foundation"

# 1.1 SENSITIVE DATA PURGE
cat > remove-secrets.py << 'EOF'
#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

# Patterns for sensitive data
PATTERNS = {
    'api_keys': [
        r'["\']?api[_-]?key["\']?\s*[:=]\s*["\'][a-zA-Z0-9_\-]{20,}["\']',
        r'ASSEMBLYAI_API_KEY\s*=\s*["\'][^"\']+["\']',
        r'sk_[a-zA-Z0-9]{32,}',  # Stripe
        r'pk_[a-zA-Z0-9]{32,}',
        r'SUPABASE_[A-Z_]+\s*=\s*["\'][^"\']+["\']',
    ],
    'tokens': [
        r'["\']?token["\']?\s*[:=]\s*["\'][a-zA-Z0-9_\-]{20,}["\']',
        r'Bearer\s+[a-zA-Z0-9_\-\.]+',
    ],
    'passwords': [
        r'["\']?password["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'["\']?pwd["\']?\s*[:=]\s*["\'][^"\']+["\']',
    ],
    'private_keys': [
        r'-----BEGIN [A-Z]+ PRIVATE KEY-----',
        r'ssh-rsa\s+[A-Za-z0-9+/]+',
    ],
    'urls_with_creds': [
        r'https?://[^:]+:[^@]+@[^\s]+',
        r'mongodb://[^:]+:[^@]+@[^\s]+',
        r'postgresql://[^:]+:[^@]+@[^\s]+',
    ]
}

def scan_file(filepath):
    """Scan file for sensitive data"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        found = []
        for pattern_type, patterns in PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    found.append(pattern_type)
                    # Replace with placeholder
                    content = re.sub(pattern, f'${{{pattern_type.upper()}_PLACEHOLDER}}', content, flags=re.IGNORECASE)
        
        if found:
            # Write cleaned content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return found
    except:
        pass
    return []

def main():
    print("🔍 Scanning for sensitive data...")
    
    sensitive_files = {}
    exclude_dirs = {'.git', 'node_modules', '.next', 'venv', '__pycache__'}
    
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.tsx', '.json', '.env', '.yml', '.yaml')):
                filepath = os.path.join(root, file)
                found = scan_file(filepath)
                if found:
                    sensitive_files[filepath] = found
    
    if sensitive_files:
        print(f"⚠️  Found sensitive data in {len(sensitive_files)} files:")
        for file, types in sensitive_files.items():
            print(f"  - {file}: {', '.join(set(types))}")
        
        # Create .env.example
        with open('.env.example', 'w') as f:
            f.write("""# Perswade Environment Variables
# Copy to .env and fill with your values

# AssemblyAI
ASSEMBLYAI_API_KEY=your_api_key_here

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_KEY=your_service_key_here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/perswade

# Redis (optional)
REDIS_URL=redis://localhost:6379

# Web3
INFURA_PROJECT_ID=your_infura_id
WALLET_CONNECT_PROJECT_ID=your_walletconnect_id

# Analytics (optional)
POSTHOG_API_KEY=your_posthog_key
SENTRY_DSN=your_sentry_dsn
""")
        print("✅ Created .env.example")
    else:
        print("✅ No sensitive data found")

if __name__ == "__main__":
    main()
EOF

python3 remove-secrets.py

# 1.2 MIT LICENSE
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 VT Infinite, Inc d/b/a Perswade.xyz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

echo "✅ MIT License created"

# 1.3 COPYRIGHT HEADERS
cat > add-headers.py << 'EOF'
#!/usr/bin/env python3
import os
from pathlib import Path

HEADER_PY = '''"""
Copyright (c) 2025 VT Infinite, Inc d/b/a Perswade.xyz
Licensed under MIT License (see LICENSE file)
Perswade™ - AI-Powered Sales Intelligence Platform
"""

'''

HEADER_JS = '''/*
 * Copyright (c) 2025 VT Infinite, Inc d/b/a Perswade.xyz
 * Licensed under MIT License (see LICENSE file)
 * Perswade™ - AI-Powered Sales Intelligence Platform
 */

'''

def add_header(filepath, header):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'Copyright (c) 2025' not in content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(header + content)
        return True
    return False

def main():
    print("📝 Adding copyright headers...")
    
    updated = 0
    exclude_dirs = {'.git', 'node_modules', '.next', 'venv', '__pycache__'}
    
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            filepath = os.path.join(root, file)
            
            if file.endswith('.py'):
                if add_header(filepath, HEADER_PY):
                    updated += 1
            elif file.endswith(('.js', '.ts', '.tsx')):
                if add_header(filepath, HEADER_JS):
                    updated += 1
    
    print(f"✅ Added headers to {updated} files")

if __name__ == "__main__":
    main()
EOF

python3 add-headers.py

# 1.4 TRADEMARK POLICY
cat > TRADEMARK.md << 'EOF'
# Perswade™ Trademark Policy

## Overview
"Perswade" is a trademark of VT Infinite, Inc d/b/a Perswade.xyz. While our code is open source under the MIT License, our brand and trademarks are protected.

## Acceptable Use
You MAY:
- ✅ Use "Perswade" to refer to the official project
- ✅ Use "Perswade" to describe compatibility (e.g., "Compatible with Perswade")
- ✅ Use "Perswade" in articles, tutorials, and presentations about the project

## Restricted Use
You MAY NOT without explicit permission:
- ❌ Use "Perswade" in your product/company name
- ❌ Use "Perswade" in domain names
- ❌ Create modified versions called "Perswade"
- ❌ Use our logo without permission
- ❌ Claim official affiliation with Perswade

## Naming Forks
If you fork Perswade, you must:
1. Choose a different name for your project
2. Remove all Perswade branding
3. Clearly state it's a fork of Perswade

## Contact
For trademark usage requests: legal@perswade.xyz

Last updated: $(date +%Y-%m-%d)
EOF

echo "✅ Trademark policy created"

# Update .gitignore
cat >> .gitignore << 'EOF'

# Environment
.env
.env.local
.env.*.local

# Secrets
*.key
*.pem
*.p12
*.pfx

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Python
venv/
__pycache__/
*.pyc
.pytest_cache/

# Node
node_modules/
.next/
out/
build/
dist/

# Logs
*.log
logs/

# Testing
coverage/
.coverage
htmlcov/
EOF

echo "✅ Updated .gitignore"
echo "✅ PHASE 1 COMPLETE: Security & Legal Foundation"
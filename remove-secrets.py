"""
Copyright (c) 2025 VT Infinite, Inc d/b/a Perswade.xyz
Licensed under MIT License (see LICENSE file)
Perswade™ - AI-Powered Sales Intelligence Platform
"""

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
        r'${URLS_WITH_CREDS_PLACEHOLDER}
        r'${URLS_WITH_CREDS_PLACEHOLDER}
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
SUPABASE_URL=${URLS_WITH_CREDS_PLACEHOLDER}

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

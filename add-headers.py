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

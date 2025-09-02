"""
Copyright (c) 2025 VT Infinite, Inc d/b/a Perswade.xyz
Licensed under MIT License (see LICENSE file)
Perswade™ - AI-Powered Sales Intelligence Platform
"""

#!/usr/bin/env python3
"""
Comprehensive Codebase Discovery Script for Perswade
Documents everything that exists in the current codebase
"""

import os
import re
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict
import mimetypes
import ast

class CodebaseDiscovery:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.inventory = {
            "metadata": {},
            "structure": {},
            "technologies": {},
            "files": {},
            "code_analysis": {},
            "documentation": {},
            "configuration": {},
            "dependencies": {},
            "testing": {},
            "version_control": {},
            "build_artifacts": {},
            "ai_ml_components": {},
            "sales_intelligence": {}
        }
        
    def discover_all(self) -> Dict:
        """Execute comprehensive discovery"""
        print("🔍 Starting Comprehensive Codebase Discovery...")
        print("=" * 60)
        
        # Run all discovery modules
        self.collect_metadata()
        self.map_directory_structure()
        self.analyze_file_types()
        self.discover_technologies()
        self.analyze_code_organization()
        self.discover_documentation()
        self.analyze_configuration_files()
        self.discover_dependencies()
        self.analyze_testing()
        self.analyze_version_control()
        self.discover_ai_ml_components()
        self.analyze_sales_intelligence_features()
        self.analyze_assemblyai_integration()
        self.analyze_frontend_structure()
        self.analyze_backend_structure()
        self.discover_database_schema()
        self.analyze_api_endpoints()
        
        return self.inventory
    
    def collect_metadata(self):
        """Collect basic repository metadata"""
        print("📊 Collecting repository metadata...")
        
        # Get repository size
        total_size = 0
        file_count = 0
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                file_count += 1
                try:
                    filepath = Path(root) / file
                    total_size += filepath.stat().st_size
                except:
                    pass
        
        # Git information
        git_info = {}
        if (self.root_path / ".git").exists():
            try:
                # Get current branch
                result = subprocess.run(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    cwd=self.root_path,
                    capture_output=True,
                    text=True
                )
                git_info["current_branch"] = result.stdout.strip()
                
                # Get last commit
                result = subprocess.run(
                    ["git", "log", "-1", "--format=%H %s"],
                    cwd=self.root_path,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    commit_info = result.stdout.strip().split(" ", 1)
                    git_info["last_commit_hash"] = commit_info[0][:8]
                    git_info["last_commit_message"] = commit_info[1] if len(commit_info) > 1 else ""
                
                # Count commits
                result = subprocess.run(
                    ["git", "rev-list", "--count", "HEAD"],
                    cwd=self.root_path,
                    capture_output=True,
                    text=True
                )
                git_info["total_commits"] = result.stdout.strip()
            except:
                pass
        
        self.inventory["metadata"] = {
            "discovery_date": datetime.now().isoformat(),
            "repository_path": str(self.root_path),
            "repository_name": self.root_path.name,
            "total_files": file_count,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "git_info": git_info
        }
    
    def map_directory_structure(self):
        """Map the complete directory structure"""
        print("📁 Mapping directory structure...")
        
        def build_tree(path: Path, max_depth: int = 3, current_depth: int = 0) -> Dict:
            if current_depth >= max_depth:
                return {"type": "directory", "truncated": True}
            
            tree = {}
            try:
                for item in sorted(path.iterdir()):
                    # Skip hidden and build directories
                    if item.name.startswith('.') and item.name not in ['.env', '.gitignore']:
                        continue
                    if item.name in ['node_modules', '__pycache__', 'dist', 'build', '.next']:
                        tree[item.name] = {"type": "directory", "skipped": True}
                        continue
                    
                    if item.is_dir():
                        tree[item.name] = {
                            "type": "directory",
                            "children": build_tree(item, max_depth, current_depth + 1)
                        }
                    else:
                        tree[item.name] = {
                            "type": "file",
                            "size_kb": round(item.stat().st_size / 1024, 2),
                            "extension": item.suffix
                        }
            except PermissionError:
                pass
            
            return tree
        
        # Get root level directories
        root_dirs = []
        root_files = []
        for item in sorted(self.root_path.iterdir()):
            if not item.name.startswith('.') or item.name in ['.env', '.gitignore']:
                if item.is_dir():
                    root_dirs.append(item.name)
                else:
                    root_files.append(item.name)
        
        self.inventory["structure"] = {
            "root_directories": root_dirs,
            "root_files": root_files,
            "tree": build_tree(self.root_path),
            "directory_count": len(list(self.root_path.rglob("**/"))),
        }
    
    def analyze_file_types(self):
        """Analyze all file types and their distribution"""
        print("📄 Analyzing file types...")
        
        extensions = defaultdict(int)
        categories = defaultdict(list)
        
        # Define categories
        category_map = {
            "source_code": ['.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.cpp', '.c', '.go', '.rs'],
            "web": ['.html', '.css', '.scss', '.sass', '.less'],
            "data": ['.json', '.csv', '.xml', '.sql', '.db'],
            "config": ['.yml', '.yaml', '.toml', '.ini', '.conf', '.env'],
            "documentation": ['.md', '.txt', '.rst', '.doc', '.docx', '.pdf'],
            "images": ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico'],
            "scripts": ['.sh', '.bash', '.bat', '.ps1'],
            "test": ['test.py', 'test.js', 'test.ts', 'spec.js', 'spec.ts'],
        }
        
        for root, dirs, files in os.walk(self.root_path):
            # Skip common build/dependency directories
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__', '.next', 'dist']]
            
            for file in files:
                ext = Path(file).suffix.lower()
                if ext:
                    extensions[ext] += 1
                    
                    # Categorize
                    for category, exts in category_map.items():
                        if ext in exts or (category == "test" and any(file.endswith(t) for t in exts)):
                            categories[category].append(file)
        
        # Sort by frequency
        sorted_extensions = sorted(extensions.items(), key=lambda x: x[1], reverse=True)
        
        self.inventory["files"] = {
            "extensions": dict(sorted_extensions[:20]),  # Top 20 extensions
            "total_unique_extensions": len(extensions),
            "categories": {k: len(v) for k, v in categories.items()},
            "most_common_type": sorted_extensions[0] if sorted_extensions else None
        }
    
    def discover_technologies(self):
        """Discover technologies and frameworks in use"""
        print("🔧 Discovering technologies...")
        
        tech_stack = {
            "frontend": [],
            "backend": [],
            "database": [],
            "ai_ml": [],
            "testing": [],
            "devops": [],
            "other": []
        }
        
        # Check package.json for JS/TS technologies
        package_json_path = self.root_path / "package.json"
        frontend_package_json = self.root_path / "frontend" / "package.json"
        
        for pkg_path in [package_json_path, frontend_package_json]:
            if pkg_path.exists():
                with open(pkg_path) as f:
                    pkg = json.load(f)
                    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                    
                    # Frontend technologies
                    if "react" in deps:
                        tech_stack["frontend"].append(f"React {deps.get('react', 'unknown version')}")
                    if "next" in deps:
                        tech_stack["frontend"].append(f"Next.js {deps.get('next', 'unknown version')}")
                    if "vue" in deps:
                        tech_stack["frontend"].append(f"Vue {deps.get('vue', 'unknown version')}")
                    if "tailwindcss" in deps:
                        tech_stack["frontend"].append(f"Tailwind CSS {deps.get('tailwindcss', 'unknown version')}")
                    
                    # Backend/API
                    if "express" in deps:
                        tech_stack["backend"].append(f"Express {deps.get('express', 'unknown version')}")
                    if "fastify" in deps:
                        tech_stack["backend"].append(f"Fastify {deps.get('fastify', 'unknown version')}")
                    
                    # AI/ML related
                    if "assemblyai" in deps or "@assemblyai/realtime" in deps:
                        version = deps.get("assemblyai") or deps.get("@assemblyai/realtime", "unknown")
                        tech_stack["ai_ml"].append(f"AssemblyAI {version}")
                    if "openai" in deps:
                        tech_stack["ai_ml"].append(f"OpenAI {deps.get('openai', 'unknown version')}")
                    
                    # Database
                    if "mongoose" in deps:
                        tech_stack["database"].append("MongoDB (Mongoose)")
                    if "pg" in deps or "postgres" in deps:
                        tech_stack["database"].append("PostgreSQL")
                    if "@supabase/supabase-js" in deps:
                        tech_stack["database"].append(f"Supabase {deps.get('@supabase/supabase-js', 'unknown version')}")
                    
                    # Testing
                    if "jest" in deps:
                        tech_stack["testing"].append("Jest")
                    if "mocha" in deps:
                        tech_stack["testing"].append("Mocha")
                    if "@testing-library/react" in deps:
                        tech_stack["testing"].append("React Testing Library")
        
        # Check Python requirements
        requirements_files = ["requirements.txt", "requirements-dev.txt", "Pipfile", "pyproject.toml"]
        for req_file in requirements_files:
            req_path = self.root_path / req_file
            if req_path.exists():
                with open(req_path) as f:
                    content = f.read().lower()
                    
                    # Backend frameworks
                    if "fastapi" in content:
                        tech_stack["backend"].append("FastAPI")
                    if "django" in content:
                        tech_stack["backend"].append("Django")
                    if "flask" in content:
                        tech_stack["backend"].append("Flask")
                    
                    # AI/ML
                    if "assemblyai" in content:
                        tech_stack["ai_ml"].append("AssemblyAI (Python)")
                    if "torch" in content or "pytorch" in content:
                        tech_stack["ai_ml"].append("PyTorch")
                    if "tensorflow" in content:
                        tech_stack["ai_ml"].append("TensorFlow")
                    if "transformers" in content:
                        tech_stack["ai_ml"].append("HuggingFace Transformers")
                    if "daft" in content:
                        tech_stack["ai_ml"].append("Daft")
                    
                    # Testing
                    if "pytest" in content:
                        tech_stack["testing"].append("Pytest")
                    if "unittest" in content:
                        tech_stack["testing"].append("Unittest")
        
        # Check for Docker
        if (self.root_path / "Dockerfile").exists() or (self.root_path / "docker-compose.yml").exists():
            tech_stack["devops"].append("Docker")
        
        # Check for CI/CD
        if (self.root_path / ".github" / "workflows").exists():
            tech_stack["devops"].append("GitHub Actions")
        if (self.root_path / ".gitlab-ci.yml").exists():
            tech_stack["devops"].append("GitLab CI")
        
        self.inventory["technologies"] = tech_stack
    
    def analyze_code_organization(self):
        """Analyze how code is organized"""
        print("💻 Analyzing code organization...")
        
        code_stats = {
            "languages": defaultdict(lambda: {"files": 0, "lines": 0}),
            "largest_files": [],
            "entry_points": [],
            "modules": [],
            "components": []
        }
        
        # Analyze source files
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__', '.next']]
            
            for file in files:
                filepath = Path(root) / file
                
                # Detect entry points
                if file in ["index.js", "index.ts", "main.py", "app.py", "server.js", "server.py"]:
                    code_stats["entry_points"].append(str(filepath.relative_to(self.root_path)))
                
                # Count lines and language stats
                if filepath.suffix in ['.py', '.js', '.ts', '.tsx', '.jsx']:
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = len(f.readlines())
                            lang = filepath.suffix
                            code_stats["languages"][lang]["files"] += 1
                            code_stats["languages"][lang]["lines"] += lines
                            
                            # Track large files
                            if lines > 300:
                                code_stats["largest_files"].append({
                                    "path": str(filepath.relative_to(self.root_path)),
                                    "lines": lines
                                })
                    except:
                        pass
                
                # Find React components
                if filepath.suffix in ['.jsx', '.tsx'] and 'components' in str(filepath):
                    code_stats["components"].append(filepath.stem)
                
                # Find Python modules
                if filepath.name == "__init__.py":
                    module_path = filepath.parent.relative_to(self.root_path)
                    code_stats["modules"].append(str(module_path))
        
        # Sort largest files
        code_stats["largest_files"] = sorted(
            code_stats["largest_files"], 
            key=lambda x: x["lines"], 
            reverse=True
        )[:10]
        
        # Convert defaultdict to regular dict
        code_stats["languages"] = dict(code_stats["languages"])
        
        self.inventory["code_analysis"] = code_stats
    
    def discover_documentation(self):
        """Find and analyze documentation"""
        print("📚 Discovering documentation...")
        
        docs = {
            "markdown_files": [],
            "readme_files": [],
            "api_docs": [],
            "comments_density": {},
            "docstrings": [],
            "wikis": []
        }
        
        # Find all documentation files
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__']]
            
            for file in files:
                filepath = Path(root) / file
                relative_path = filepath.relative_to(self.root_path)
                
                # Markdown files
                if filepath.suffix == '.md':
                    docs["markdown_files"].append(str(relative_path))
                    
                    # Special documentation files
                    if file.upper().startswith('README'):
                        docs["readme_files"].append(str(relative_path))
                    if 'api' in file.lower() or 'API' in filepath.parts:
                        docs["api_docs"].append(str(relative_path))
                
                # Check for inline documentation in code
                if filepath.suffix == '.py':
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            # Count docstrings
                            docstring_count = len(re.findall(r'"""[\s\S]*?"""', content))
                            if docstring_count > 0:
                                docs["docstrings"].append({
                                    "file": str(relative_path),
                                    "count": docstring_count
                                })
                    except:
                        pass
        
        self.inventory["documentation"] = docs
    
    def analyze_configuration_files(self):
        """Analyze configuration files"""
        print("⚙️ Analyzing configuration files...")
        
        configs = {
            "environment": [],
            "build_configs": [],
            "linting": [],
            "formatting": [],
            "deployment": [],
            "package_managers": []
        }
        
        # Check for various config files
        config_patterns = {
            "environment": [".env", ".env.example", ".env.local", ".env.production"],
            "build_configs": ["webpack.config.js", "vite.config.js", "rollup.config.js", "tsconfig.json", "jsconfig.json"],
            "linting": [".eslintrc", ".eslintrc.json", ".eslintrc.js", ".pylintrc", "tslint.json"],
            "formatting": [".prettierrc", ".prettierrc.json", ".editorconfig", ".black"],
            "deployment": ["vercel.json", "netlify.toml", "Procfile", "app.yaml", "render.yaml"],
            "package_managers": ["package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "Pipfile", "requirements.txt"]
        }
        
        for category, patterns in config_patterns.items():
            for pattern in patterns:
                # Check root and common subdirectories
                for check_path in [self.root_path, self.root_path / "frontend", self.root_path / "backend"]:
                    config_file = check_path / pattern
                    if config_file.exists():
                        configs[category].append(str(config_file.relative_to(self.root_path)))
        
        # Parse key configs for details
        if (self.root_path / "package.json").exists():
            with open(self.root_path / "package.json") as f:
                pkg = json.load(f)
                configs["scripts"] = list(pkg.get("scripts", {}).keys())
        
        self.inventory["configuration"] = configs
    
    def discover_dependencies(self):
        """Discover all project dependencies"""
        print("📦 Discovering dependencies...")
        
        deps = {
            "npm": {"production": {}, "development": {}},
            "python": [],
            "total_count": 0
        }
        
        # NPM dependencies
        for check_path in [self.root_path, self.root_path / "frontend", self.root_path / "backend"]:
            package_json = check_path / "package.json"
            if package_json.exists():
                with open(package_json) as f:
                    pkg = json.load(f)
                    if pkg.get("dependencies"):
                        deps["npm"]["production"].update(pkg["dependencies"])
                    if pkg.get("devDependencies"):
                        deps["npm"]["development"].update(pkg["devDependencies"])
        
        # Python dependencies
        for req_file in ["requirements.txt", "requirements-dev.txt"]:
            req_path = self.root_path / req_file
            if req_path.exists():
                with open(req_path) as f:
                    deps["python"].extend([
                        line.strip() for line in f 
                        if line.strip() and not line.startswith('#')
                    ])
        
        deps["total_count"] = (
            len(deps["npm"]["production"]) + 
            len(deps["npm"]["development"]) + 
            len(deps["python"])
        )
        
        self.inventory["dependencies"] = deps
    
    def analyze_testing(self):
        """Analyze testing setup and coverage"""
        print("🧪 Analyzing testing setup...")
        
        testing = {
            "test_files": [],
            "test_directories": [],
            "testing_frameworks": [],
            "test_commands": []
        }
        
        # Find test files
        test_patterns = ["test_*.py", "*_test.py", "*.test.js", "*.test.ts", "*.spec.js", "*.spec.ts"]
        for pattern in test_patterns:
            test_files = list(self.root_path.rglob(pattern))
            for test_file in test_files:
                testing["test_files"].append(str(test_file.relative_to(self.root_path)))
        
        # Find test directories
        for root, dirs, files in os.walk(self.root_path):
            for dir_name in dirs:
                if dir_name in ["tests", "test", "__tests__", "spec"]:
                    testing["test_directories"].append(
                        str(Path(root) / dir_name).replace(str(self.root_path), "").lstrip("/")
                    )
        
        # Check package.json for test scripts
        if (self.root_path / "package.json").exists():
            with open(self.root_path / "package.json") as f:
                pkg = json.load(f)
                scripts = pkg.get("scripts", {})
                test_scripts = [k for k in scripts if "test" in k.lower()]
                testing["test_commands"] = test_scripts
        
        testing["test_count"] = len(testing["test_files"])
        
        self.inventory["testing"] = testing
    
    def analyze_version_control(self):
        """Analyze version control setup"""
        print("🔄 Analyzing version control...")
        
        vc = {
            "git": False,
            "gitignore": False,
            "gitignore_contents": [],
            "branches": [],
            "remotes": [],
            "hooks": []
        }
        
        if (self.root_path / ".git").exists():
            vc["git"] = True
            
            # Get branches
            try:
                result = subprocess.run(
                    ["git", "branch", "-a"],
                    cwd=self.root_path,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    vc["branches"] = [
                        b.strip().replace("* ", "")
                        for b in result.stdout.split("\n")
                        if b.strip()
                    ]
            except:
                pass
            
            # Get remotes
            try:
                result = subprocess.run(
                    ["git", "remote", "-v"],
                    cwd=self.root_path,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    vc["remotes"] = list(set([
                        line.split()[0]
                        for line in result.stdout.split("\n")
                        if line.strip()
                    ]))
            except:
                pass
        
        # Check .gitignore
        gitignore_path = self.root_path / ".gitignore"
        if gitignore_path.exists():
            vc["gitignore"] = True
            with open(gitignore_path) as f:
                vc["gitignore_contents"] = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith("#")
                ][:20]  # First 20 entries
        
        self.inventory["version_control"] = vc
    
    def discover_ai_ml_components(self):
        """Discover AI/ML specific components"""
        print("🤖 Discovering AI/ML components...")
        
        ai_ml = {
            "models": [],
            "datasets": [],
            "notebooks": [],
            "training_scripts": [],
            "inference_scripts": [],
            "embeddings": [],
            "vector_stores": []
        }
        
        # Find model files
        model_extensions = ['.pkl', '.h5', '.pt', '.pth', '.onnx', '.pb', '.tflite']
        for ext in model_extensions:
            models = list(self.root_path.rglob(f"*{ext}"))
            for model in models:
                ai_ml["models"].append(str(model.relative_to(self.root_path)))
        
        # Find Jupyter notebooks
        notebooks = list(self.root_path.rglob("*.ipynb"))
        ai_ml["notebooks"] = [str(nb.relative_to(self.root_path)) for nb in notebooks]
        
        # Find training/inference scripts
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git']]
            for file in files:
                if re.search(r'(train|training|fine-tune|finetune)', file, re.IGNORECASE):
                    ai_ml["training_scripts"].append(
                        str(Path(root) / file).replace(str(self.root_path), "").lstrip("/")
                    )
                if re.search(r'(inference|predict|serve|model)', file, re.IGNORECASE):
                    ai_ml["inference_scripts"].append(
                        str(Path(root) / file).replace(str(self.root_path), "").lstrip("/")
                    )
        
        self.inventory["ai_ml_components"] = ai_ml
    
    def analyze_sales_intelligence_features(self):
        """Analyze sales intelligence and C²PS specific features"""
        print("💼 Analyzing sales intelligence features...")
        
        sales = {
            "c2ps_mentions": [],
            "sales_keywords": defaultdict(list),
            "crm_integrations": [],
            "call_processing": [],
            "analytics_dashboards": []
        }
        
        # Keywords to search for
        sales_keywords = {
            "c2ps": ["credibility", "commonality", "problem", "solution", "C²PS", "C2PS"],
            "sales_process": ["conversion", "pipeline", "lead", "prospect", "opportunity", "deal"],
            "call_analysis": ["transcript", "recording", "call", "conversation", "meeting"],
            "metrics": ["score", "prediction", "forecast", "probability", "analytics"]
        }
        
        # Search for sales-related code
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__']]
            
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.tsx', '.jsx')):
                    filepath = Path(root) / file
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            
                            for category, keywords in sales_keywords.items():
                                for keyword in keywords:
                                    if keyword.lower() in content:
                                        relative_path = str(filepath.relative_to(self.root_path))
                                        sales["sales_keywords"][category].append(relative_path)
                                        break
                            
                            # Check for CRM integrations
                            crm_systems = ["salesforce", "hubspot", "pipedrive", "zoho", "supabase"]
                            for crm in crm_systems:
                                if crm in content:
                                    sales["crm_integrations"].append({
                                        "system": crm,
                                        "file": str(filepath.relative_to(self.root_path))
                                    })
                    except:
                        pass
        
        # Deduplicate
        for category in sales["sales_keywords"]:
            sales["sales_keywords"][category] = list(set(sales["sales_keywords"][category]))[:5]
        
        self.inventory["sales_intelligence"] = dict(sales)
    
    def analyze_assemblyai_integration(self):
        """Deep dive into AssemblyAI integration"""
        print("🎤 Analyzing AssemblyAI integration...")
        
        assemblyai = {
            "files_with_integration": [],
            "api_usage_patterns": [],
            "streaming_setup": False,
            "features_used": []
        }
        
        # Search for AssemblyAI usage
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git']]
            
            for file in files:
                if file.endswith(('.py', '.js', '.ts')):
                    filepath = Path(root) / file
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                            if 'assemblyai' in content.lower() or 'assembly' in content.lower():
                                assemblyai["files_with_integration"].append(
                                    str(filepath.relative_to(self.root_path))
                                )
                                
                                # Check for specific features
                                if 'RealtimeTranscriber' in content or 'realtime' in content.lower():
                                    assemblyai["streaming_setup"] = True
                                    assemblyai["features_used"].append("Real-time Streaming")
                                
                                if 'speaker_labels' in content or 'diarization' in content:
                                    assemblyai["features_used"].append("Speaker Diarization")
                                
                                if 'sentiment' in content.lower():
                                    assemblyai["features_used"].append("Sentiment Analysis")
                                
                                if 'word_boost' in content:
                                    assemblyai["features_used"].append("Word Boost")
                    except:
                        pass
        
        assemblyai["features_used"] = list(set(assemblyai["features_used"]))
        self.inventory["assemblyai"] = assemblyai
    
    def analyze_frontend_structure(self):
        """Analyze frontend structure in detail"""
        print("🎨 Analyzing frontend structure...")
        
        frontend = {
            "framework": None,
            "pages": [],
            "components": [],
            "styles": [],
            "public_assets": [],
            "routing": None
        }
        
        frontend_path = self.root_path / "frontend"
        if not frontend_path.exists():
            frontend_path = self.root_path  # Check root if no frontend folder
        
        # Check for Next.js
        if (frontend_path / "pages").exists() or (frontend_path / "app").exists():
            frontend["framework"] = "Next.js"
            
            # Get pages
            for page_dir in ["pages", "app"]:
                page_path = frontend_path / page_dir
                if page_path.exists():
                    pages = list(page_path.rglob("*.tsx")) + list(page_path.rglob("*.jsx"))
                    frontend["pages"] = [str(p.relative_to(frontend_path)) for p in pages]
                    frontend["routing"] = "File-based (Next.js)"
        
        # Get components
        components_path = frontend_path / "components"
        if components_path.exists():
            components = list(components_path.rglob("*.tsx")) + list(components_path.rglob("*.jsx"))
            frontend["components"] = [str(c.relative_to(frontend_path)) for c in components]
        
        # Get styles
        styles = list(frontend_path.rglob("*.css")) + list(frontend_path.rglob("*.scss"))
        frontend["styles"] = [str(s.relative_to(frontend_path)) for s in styles][:10]
        
        self.inventory["frontend"] = frontend
    
    def analyze_backend_structure(self):
        """Analyze backend structure"""
        print("⚙️ Analyzing backend structure...")
        
        backend = {
            "framework": None,
            "api_files": [],
            "middleware": [],
            "models": [],
            "controllers": [],
            "services": []
        }
        
        # Check for backend frameworks
        backend_indicators = {
            "FastAPI": ["fastapi", "uvicorn"],
            "Express": ["express", "app.listen"],
            "Django": ["django", "settings.py", "urls.py"],
            "Flask": ["flask", "Flask(__name__)"]
        }
        
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git']]
            
            for file in files:
                filepath = Path(root) / file
                relative_path = str(filepath.relative_to(self.root_path))
                
                # Check for API routes
                if 'api' in file.lower() or 'route' in file.lower() or 'endpoint' in file.lower():
                    backend["api_files"].append(relative_path)
                
                # Check for models
                if 'model' in file.lower() and file.endswith(('.py', '.js', '.ts')):
                    backend["models"].append(relative_path)
                
                # Check for controllers
                if 'controller' in file.lower():
                    backend["controllers"].append(relative_path)
                
                # Check for services
                if 'service' in file.lower():
                    backend["services"].append(relative_path)
                
                # Detect framework
                if file.endswith(('.py', '.js', '.ts')):
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            for framework, indicators in backend_indicators.items():
                                if any(ind in content for ind in indicators):
                                    backend["framework"] = framework
                                    break
                    except:
                        pass
        
        self.inventory["backend"] = backend
    
    def discover_database_schema(self):
        """Discover database schema and migrations"""
        print("🗄️ Discovering database schema...")
        
        database = {
            "migrations": [],
            "schemas": [],
            "seed_files": [],
            "database_type": None
        }
        
        # Look for migrations
        migration_dirs = ["migrations", "migrate", "alembic"]
        for mig_dir in migration_dirs:
            mig_path = self.root_path / mig_dir
            if mig_path.exists():
                migrations = list(mig_path.rglob("*.sql")) + list(mig_path.rglob("*.py"))
                database["migrations"] = [str(m.relative_to(self.root_path)) for m in migrations]
        
        # Look for schema files
        schema_patterns = ["*schema*.sql", "*schema*.prisma", "*model*.py", "*model*.js"]
        for pattern in schema_patterns:
            schemas = list(self.root_path.rglob(pattern))
            database["schemas"].extend([str(s.relative_to(self.root_path)) for s in schemas])
        
        # Look for seed files
        seed_patterns = ["*seed*.sql", "*seed*.js", "*seed*.py", "*fixture*.json"]
        for pattern in seed_patterns:
            seeds = list(self.root_path.rglob(pattern))
            database["seed_files"].extend([str(s.relative_to(self.root_path)) for s in seeds])
        
        # Detect database type
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if file.endswith(('.env', '.env.example')):
                    filepath = Path(root) / file
                    try:
                        with open(filepath) as f:
                            content = f.read()
                            if 'DATABASE_URL' in content or 'DB_' in content:
                                if 'postgres' in content.lower():
                                    database["database_type"] = "PostgreSQL"
                                elif 'mongodb' in content.lower():
                                    database["database_type"] = "MongoDB"
                                elif 'mysql' in content.lower():
                                    database["database_type"] = "MySQL"
                                elif 'supabase' in content.lower():
                                    database["database_type"] = "Supabase (PostgreSQL)"
                    except:
                        pass
        
        self.inventory["database"] = database
    
    def analyze_api_endpoints(self):
        """Analyze API endpoints"""
        print("🔌 Analyzing API endpoints...")
        
        api = {
            "endpoints": [],
            "rest_apis": [],
            "graphql": False,
            "websocket": False,
            "api_documentation": []
        }
        
        # Search for API definitions
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git']]
            
            for file in files:
                if file.endswith(('.py', '.js', '.ts')):
                    filepath = Path(root) / file
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                            # Find REST endpoints
                            rest_patterns = [
                                r'@app\.(get|post|put|delete|patch)\(["\']([^"\']+)',
                                r'router\.(get|post|put|delete|patch)\(["\']([^"\']+)',
                                r'@router\.(get|post|put|delete|patch)\(["\']([^"\']+)',
                            ]
                            
                            for pattern in rest_patterns:
                                matches = re.findall(pattern, content)
                                for match in matches:
                                    method = match[0].upper() if isinstance(match, tuple) else "GET"
                                    path = match[1] if isinstance(match, tuple) else match
                                    api["endpoints"].append({
                                        "method": method,
                                        "path": path,
                                        "file": str(filepath.relative_to(self.root_path))
                                    })
                            
                            # Check for GraphQL
                            if 'graphql' in content.lower() or 'apollo' in content.lower():
                                api["graphql"] = True
                            
                            # Check for WebSocket
                            if 'websocket' in content.lower() or 'socket.io' in content.lower():
                                api["websocket"] = True
                    except:
                        pass
        
        # Look for API documentation
        api_doc_patterns = ["*api*.md", "*swagger*.json", "*openapi*.yaml"]
        for pattern in api_doc_patterns:
            docs = list(self.root_path.rglob(pattern))
            api["api_documentation"] = [str(d.relative_to(self.root_path)) for d in docs]
        
        # Limit endpoints to first 20 for readability
        api["endpoints"] = api["endpoints"][:20]
        
        self.inventory["api"] = api
    
    def generate_markdown_report(self) -> str:
        """Generate comprehensive markdown report of what exists"""
        lines = [
            "# 📦 Perswade Codebase Inventory Report",
            f"\n**Generated:** {self.inventory['metadata']['discovery_date']}",
            f"**Repository:** `{self.inventory['metadata']['repository_name']}`",
            f"**Path:** `{self.inventory['metadata']['repository_path']}`",
            "",
            "## 📊 Repository Overview",
            "",
            f"- **Total Files:** {self.inventory['metadata']['total_files']:,}",
            f"- **Total Size:** {self.inventory['metadata']['total_size_mb']} MB",
            f"- **Total Directories:** {self.inventory['structure']['directory_count']:,}",
        ]
        
        # Git info
        if self.inventory['metadata']['git_info']:
            git = self.inventory['metadata']['git_info']
            lines.extend([
                "",
                "### Git Information",
                f"- **Current Branch:** `{git.get('current_branch', 'N/A')}`",
                f"- **Total Commits:** {git.get('total_commits', 'N/A')}",
                f"- **Last Commit:** {git.get('last_commit_hash', 'N/A')} - {git.get('last_commit_message', 'N/A')}"
            ])
        
        # Directory Structure
        lines.extend([
            "",
            "## 📁 Directory Structure",
            "",
            "### Root Directories",
            "```"
        ])
        for dir_name in self.inventory['structure']['root_directories']:
            lines.append(f"📁 {dir_name}/")
        lines.append("```")
        
        lines.extend([
            "",
            "### Root Files",
            "```"
        ])
        for file_name in self.inventory['structure']['root_files']:
            lines.append(f"📄 {file_name}")
        lines.append("```")
        
        # Technologies
        lines.extend([
            "",
            "## 🔧 Technology Stack",
            ""
        ])
        for category, techs in self.inventory['technologies'].items():
            if techs:
                lines.append(f"### {category.title()}")
                for tech in techs:
                    lines.append(f"- {tech}")
                lines.append("")
        
        # Code Analysis
        lines.extend([
            "## 💻 Code Organization",
            "",
            "### Languages Distribution"
        ])
        for lang, stats in self.inventory['code_analysis']['languages'].items():
            lines.append(f"- **{lang}:** {stats['files']} files, {stats['lines']:,} lines")
        
        if self.inventory['code_analysis']['entry_points']:
            lines.extend([
                "",
                "### Entry Points"
            ])
            for entry in self.inventory['code_analysis']['entry_points'][:5]:
                lines.append(f"- `{entry}`")
        
        if self.inventory['code_analysis']['largest_files']:
            lines.extend([
                "",
                "### Largest Files"
            ])
            for file_info in self.inventory['code_analysis']['largest_files'][:5]:
                lines.append(f"- `{file_info['path']}` ({file_info['lines']} lines)")
        
        # Dependencies
        lines.extend([
            "",
            "## 📦 Dependencies",
            "",
            f"**Total Dependencies:** {self.inventory['dependencies']['total_count']}",
            ""
        ])
        
        if self.inventory['dependencies']['npm']['production']:
            lines.append(f"### NPM Production ({len(self.inventory['dependencies']['npm']['production'])} packages)")
            for pkg, version in list(self.inventory['dependencies']['npm']['production'].items())[:10]:
                lines.append(f"- {pkg}: `{version}`")
            if len(self.inventory['dependencies']['npm']['production']) > 10:
                lines.append(f"- ... and {len(self.inventory['dependencies']['npm']['production']) - 10} more")
            lines.append("")
        
        # Testing
        lines.extend([
            "## 🧪 Testing",
            "",
            f"- **Test Files Found:** {self.inventory['testing']['test_count']}",
            f"- **Test Directories:** {len(self.inventory['testing']['test_directories'])}"
        ])
        if self.inventory['testing']['test_commands']:
            lines.append(f"- **Test Commands:** {', '.join(self.inventory['testing']['test_commands'])}")
        
        # Documentation
        lines.extend([
            "",
            "## 📚 Documentation",
            "",
            f"- **Markdown Files:** {len(self.inventory['documentation']['markdown_files'])}",
            f"- **README Files:** {len(self.inventory['documentation']['readme_files'])}",
            f"- **API Documentation:** {len(self.inventory['documentation']['api_docs'])}"
        ])
        
        # Configuration
        lines.extend([
            "",
            "## ⚙️ Configuration",
            ""
        ])
        for category, files in self.inventory['configuration'].items():
            if files and category != 'scripts':
                lines.append(f"### {category.replace('_', ' ').title()}")
                for file in files[:5]:
                    lines.append(f"- `{file}`")
                lines.append("")
        
        if self.inventory['configuration'].get('scripts'):
            lines.extend([
                "### NPM Scripts",
                "```"
            ])
            for script in self.inventory['configuration']['scripts']:
                lines.append(f"npm run {script}")
            lines.append("```\n")
        
        # AssemblyAI Integration
        if self.inventory.get('assemblyai'):
            lines.extend([
                "## 🎤 AssemblyAI Integration",
                "",
                f"- **Files with Integration:** {len(self.inventory['assemblyai']['files_with_integration'])}",
                f"- **Streaming Setup:** {'✅ Yes' if self.inventory['assemblyai']['streaming_setup'] else '❌ No'}"
            ])
            if self.inventory['assemblyai']['features_used']:
                lines.append(f"- **Features Used:** {', '.join(self.inventory['assemblyai']['features_used'])}")
            lines.append("")
        
        # Sales Intelligence
        lines.extend([
            "## 💼 Sales Intelligence Features",
            ""
        ])
        if self.inventory['sales_intelligence']['sales_keywords']:
            for category, files in self.inventory['sales_intelligence']['sales_keywords'].items():
                if files:
                    lines.append(f"### {category.replace('_', ' ').title()} Files")
                    for file in files[:3]:
                        lines.append(f"- `{file}`")
                    lines.append("")
        
        # Frontend
        if self.inventory.get('frontend'):
            lines.extend([
                "## 🎨 Frontend Structure",
                "",
                f"- **Framework:** {self.inventory['frontend']['framework'] or 'Not detected'}",
                f"- **Pages:** {len(self.inventory['frontend']['pages'])}",
                f"- **Components:** {len(self.inventory['frontend']['components'])}",
                f"- **Routing:** {self.inventory['frontend']['routing'] or 'Not detected'}",
                ""
            ])
        
        # Backend
        if self.inventory.get('backend'):
            lines.extend([
                "## ⚙️ Backend Structure",
                "",
                f"- **Framework:** {self.inventory['backend']['framework'] or 'Not detected'}",
                f"- **API Files:** {len(self.inventory['backend']['api_files'])}",
                f"- **Models:** {len(self.inventory['backend']['models'])}",
                f"- **Controllers:** {len(self.inventory['backend']['controllers'])}",
                f"- **Services:** {len(self.inventory['backend']['services'])}",
                ""
            ])
        
        # Database
        if self.inventory.get('database'):
            lines.extend([
                "## 🗄️ Database",
                "",
                f"- **Type:** {self.inventory['database']['database_type'] or 'Not detected'}",
                f"- **Migrations:** {len(self.inventory['database']['migrations'])}",
                f"- **Schema Files:** {len(self.inventory['database']['schemas'])}",
                f"- **Seed Files:** {len(self.inventory['database']['seed_files'])}",
                ""
            ])
        
        # API
        if self.inventory.get('api'):
            lines.extend([
                "## 🔌 API Structure",
                "",
                f"- **REST Endpoints Found:** {len(self.inventory['api']['endpoints'])}",
                f"- **GraphQL:** {'✅ Yes' if self.inventory['api']['graphql'] else '❌ No'}",
                f"- **WebSocket:** {'✅ Yes' if self.inventory['api']['websocket'] else '❌ No'}",
                f"- **API Documentation:** {len(self.inventory['api']['api_documentation'])}",
                ""
            ])
            
            if self.inventory['api']['endpoints']:
                lines.append("### Sample Endpoints")
                for endpoint in self.inventory['api']['endpoints'][:5]:
                    lines.append(f"- `{endpoint['method']} {endpoint['path']}` in {endpoint['file']}")
                lines.append("")
        
        # Summary
        lines.extend([
            "## 🎯 Key Findings",
            "",
            "### ✅ What Exists:",
            ""
        ])
        
        # Generate dynamic findings based on inventory
        findings = []
        
        if self.inventory['metadata']['git_info']:
            findings.append("Git version control configured")
        
        if self.inventory.get('assemblyai', {}).get('streaming_setup'):
            findings.append("AssemblyAI real-time streaming integration")
        
        if self.inventory['technologies']['frontend']:
            findings.append(f"Frontend built with {', '.join(self.inventory['technologies']['frontend'])}")
        
        if self.inventory['technologies']['backend']:
            findings.append(f"Backend using {', '.join(self.inventory['technologies']['backend'])}")
        
        if self.inventory['testing']['test_count'] > 0:
            findings.append(f"Testing infrastructure with {self.inventory['testing']['test_count']} test files")
        
        if self.inventory['sales_intelligence']['sales_keywords'].get('c2ps'):
            findings.append("C²PS methodology implementation")
        
        for finding in findings:
            lines.append(f"- {finding}")
        
        lines.extend([
            "",
            "---",
            "*This inventory provides a complete picture of the existing codebase structure.*"
        ])
        
        return "\n".join(lines)


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Comprehensive Codebase Discovery for Perswade")
    parser.add_argument("--path", default=".", help="Path to repository root")
    parser.add_argument("--output", default="codebase-inventory.md", help="Output file name")
    args = parser.parse_args()
    
    # Run discovery
    discoverer = CodebaseDiscovery(args.path)
    inventory = discoverer.discover_all()
    
    # Generate markdown report
    markdown_report = discoverer.generate_markdown_report()
    
    # Save report
    output_path = Path(args.output)
    with open(output_path, 'w') as f:
        f.write(markdown_report)
    
    print(f"\n✅ Discovery complete! Report saved to: {output_path}")
    
    # Also save JSON version for programmatic access
    json_output = output_path.with_suffix('.json')
    with open(json_output, 'w') as f:
        json.dump(inventory, f, indent=2, default=str)
    print(f"📄 JSON inventory saved to: {json_output}")
    
    # Print summary
    print("\n📊 Quick Summary:")
    print(f"  - Total Files: {inventory['metadata']['total_files']:,}")
    print(f"  - Code Files: {inventory['code_analysis']['languages']}")
    print(f"  - Technologies: {len([t for cat in inventory['technologies'].values() for t in cat])} detected")
    print(f"  - Test Files: {inventory['testing']['test_count']}")
    
    return 0


if __name__ == "__main__":
    exit(main())
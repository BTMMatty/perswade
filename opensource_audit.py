"""
Copyright (c) 2025 VT Infinite, Inc d/b/a Perswade.xyz
Licensed under MIT License (see LICENSE file)
Perswade™ - AI-Powered Sales Intelligence Platform
"""

#!/usr/bin/env python3
"""
Open Source Readiness Audit Script for Perswade
Evaluates codebase for MIT license open sourcing based on strategic roadmap
"""

import os
import re
import json
import subprocess
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import ast

class OpenSourceAudit:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.report = {
            "summary": {},
            "critical_issues": [],
            "warnings": [],
            "recommendations": [],
            "metrics": {},
            "file_analysis": defaultdict(list)
        }
        self.sensitive_patterns = {
            "api_keys": [
                r'["\']?api[_-]?key["\']?\s*[:=]\s*["\'][^"\']{20,}["\']',
                r'["\']?apikey["\']?\s*[:=]\s*["\'][^"\']{20,}["\']',
                r'["\']?api[_-]?secret["\']?\s*[:=]\s*["\'][^"\']{20,}["\']',
                r'ASSEMBLYAI_API_KEY\s*=\s*["\'][^"\']+["\']',
                r'sk-[a-zA-Z0-9]{48}',  # OpenAI
                r'AIza[0-9A-Za-z-_]{35}',  # Google
            ],
            "credentials": [
                r'["\']?password["\']?\s*[:=]\s*["\'][^"\']+["\']',
                r'["\']?secret["\']?\s*[:=]\s*["\'][^"\']+["\']',
                r'["\']?token["\']?\s*[:=]\s*["\'][^"\']+["\']',
                r'["\']?auth["\']?\s*[:=]\s*["\'][^"\']+["\']',
            ],
            "urls_with_creds": [
                r'https?://[^:]+:[^@]+@[^\s]+',
                r'mongodb\+srv://[^:]+:[^@]+@[^\s]+',
                r'postgres://[^:]+:[^@]+@[^\s]+',
            ],
            "private_keys": [
                r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
                r'-----BEGIN PGP PRIVATE KEY BLOCK-----',
            ]
        }
        self.required_files = {
            "LICENSE": "MIT License file",
            "README.md": "Project documentation",
            "CONTRIBUTING.md": "Contribution guidelines",
            "CODE_OF_CONDUCT.md": "Community standards",
            "SECURITY.md": "Security policy",
            ".gitignore": "Git ignore file"
        }
        self.recommended_structure = {
            "packages/": "Core packages directory",
            "apps/": "Application directory",
            "docs/": "Documentation directory",
            "examples/": "Example implementations",
            ".github/": "GitHub configuration"
        }
        
    def run_audit(self) -> Dict:
        """Execute comprehensive audit"""
        print("🔍 Starting Open Source Readiness Audit...")
        
        # Core checks
        self.check_repository_structure()
        self.check_required_files()
        self.scan_for_sensitive_data()
        self.check_copyright_headers()
        self.analyze_dependencies()
        self.check_documentation_quality()
        self.analyze_code_quality()
        self.check_test_coverage()
        self.check_ci_cd()
        self.check_trademark_concerns()
        self.analyze_c2ps_implementation()
        self.check_assemblyai_integration()
        
        # Generate summary
        self.generate_summary()
        
        return self.report
    
    def check_repository_structure(self):
        """Verify repository follows recommended monorepo structure"""
        print("📂 Checking repository structure...")
        
        existing = []
        missing = []
        
        for path, description in self.recommended_structure.items():
            full_path = self.root_path / path
            if full_path.exists():
                existing.append(path)
            else:
                missing.append((path, description))
        
        if missing:
            for path, desc in missing:
                self.report["warnings"].append(f"Missing recommended directory: {path} ({desc})")
        
        # Check for monorepo indicators
        if (self.root_path / "package.json").exists():
            with open(self.root_path / "package.json") as f:
                pkg = json.load(f)
                if pkg.get("workspaces"):
                    self.report["metrics"]["monorepo"] = True
                    self.report["recommendations"].append("✅ Monorepo structure detected (workspaces)")
        
        if (self.root_path / "lerna.json").exists():
            self.report["metrics"]["monorepo"] = True
            self.report["recommendations"].append("✅ Lerna monorepo detected")
            
    def check_required_files(self):
        """Check for essential open source files"""
        print("📄 Checking required files...")
        
        for filename, description in self.required_files.items():
            filepath = self.root_path / filename
            if not filepath.exists():
                self.report["critical_issues"].append(f"Missing required file: {filename} ({description})")
            else:
                # Check file content quality
                if filename == "LICENSE":
                    self.verify_mit_license(filepath)
                elif filename == "README.md":
                    self.analyze_readme(filepath)
                    
    def verify_mit_license(self, filepath: Path):
        """Verify MIT license is properly configured"""
        with open(filepath) as f:
            content = f.read()
            if "MIT License" not in content:
                self.report["critical_issues"].append("LICENSE file exists but doesn't appear to be MIT")
            if "Copyright (c)" not in content:
                self.report["critical_issues"].append("LICENSE missing copyright notice")
            if "[Your Name/Company]" in content or "[year]" in content:
                self.report["critical_issues"].append("LICENSE contains template placeholders")
                
    def analyze_readme(self, filepath: Path):
        """Analyze README quality based on best practices"""
        with open(filepath) as f:
            content = f.read()
            
        checks = {
            "badges": r'!\[.*\]\(.*badge.*\)',
            "quick_start": r'(quick start|getting started|installation)',
            "demo_link": r'(demo\.|try it|live demo)',
            "architecture": r'(architecture|design|structure)',
            "api_docs": r'(api|documentation)',
            "contributing": r'(contributing|contribution)',
        }
        
        for feature, pattern in checks.items():
            if not re.search(pattern, content, re.IGNORECASE):
                self.report["warnings"].append(f"README missing recommended section: {feature}")
                
        # Check for images/GIFs
        if not re.search(r'!\[.*\]\(.*\.(png|jpg|gif|svg).*\)', content):
            self.report["warnings"].append("README lacks visual content (images/GIFs)")
            
    def scan_for_sensitive_data(self):
        """Scan for API keys, credentials, and sensitive information"""
        print("🔐 Scanning for sensitive data...")
        
        extensions_to_check = ['.py', '.js', '.ts', '.jsx', '.tsx', '.json', '.yaml', '.yml', 
                              '.env', '.config', '.conf', '.ini', '.sh', '.bash']
        
        sensitive_found = defaultdict(list)
        
        for root, dirs, files in os.walk(self.root_path):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'venv', '__pycache__', 'dist', 'build']]
            
            for file in files:
                filepath = Path(root) / file
                
                # Check file extension
                if any(filepath.suffix == ext for ext in extensions_to_check) or file.startswith('.env'):
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        # Check for sensitive patterns
                        for category, patterns in self.sensitive_patterns.items():
                            for pattern in patterns:
                                matches = re.findall(pattern, content, re.IGNORECASE)
                                if matches:
                                    relative_path = filepath.relative_to(self.root_path)
                                    sensitive_found[category].append(str(relative_path))
                                    
                    except Exception as e:
                        pass
        
        # Report findings
        for category, files in sensitive_found.items():
            for file in files[:5]:  # Limit to first 5 per category
                self.report["critical_issues"].append(f"Potential {category} found in: {file}")
                
        if sensitive_found:
            self.report["critical_issues"].append(
                f"⚠️ Found sensitive data in {sum(len(f) for f in sensitive_found.values())} files"
            )
            
    def check_copyright_headers(self):
        """Check for copyright headers in source files"""
        print("©️ Checking copyright headers...")
        
        source_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx']
        files_checked = 0
        files_with_copyright = 0
        files_missing_copyright = []
        
        copyright_pattern = r'Copyright \(c\) \d{4}'
        
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'venv', '__pycache__']]
            
            for file in files:
                filepath = Path(root) / file
                if filepath.suffix in source_extensions:
                    files_checked += 1
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            # Check first 10 lines for copyright
                            head = ''.join(f.readlines()[:10])
                            if re.search(copyright_pattern, head):
                                files_with_copyright += 1
                            else:
                                files_missing_copyright.append(filepath.relative_to(self.root_path))
                    except:
                        pass
        
        if files_checked > 0:
            copyright_percentage = (files_with_copyright / files_checked) * 100
            self.report["metrics"]["copyright_headers"] = f"{copyright_percentage:.1f}%"
            
            if copyright_percentage < 50:
                self.report["critical_issues"].append(
                    f"Only {copyright_percentage:.1f}% of source files have copyright headers"
                )
                
    def analyze_dependencies(self):
        """Analyze project dependencies and their licenses"""
        print("📦 Analyzing dependencies...")
        
        # Check package.json
        if (self.root_path / "package.json").exists():
            with open(self.root_path / "package.json") as f:
                pkg = json.load(f)
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                self.report["metrics"]["npm_dependencies"] = len(deps)
                
                # Check for AssemblyAI
                if "assemblyai" in deps or "@assemblyai/realtime" in deps:
                    self.report["recommendations"].append("✅ AssemblyAI integration detected")
                    
        # Check requirements.txt or pyproject.toml
        if (self.root_path / "requirements.txt").exists():
            with open(self.root_path / "requirements.txt") as f:
                lines = f.readlines()
                py_deps = [l.strip() for l in lines if l.strip() and not l.startswith('#')]
                self.report["metrics"]["python_dependencies"] = len(py_deps)
                
                # Check for key dependencies
                key_deps = ["assemblyai", "daft", "fastapi", "torch", "transformers"]
                for dep in key_deps:
                    if any(dep in d.lower() for d in py_deps):
                        self.report["recommendations"].append(f"✅ {dep} dependency found")
                        
    def check_documentation_quality(self):
        """Evaluate documentation completeness"""
        print("📚 Checking documentation quality...")
        
        docs_path = self.root_path / "docs"
        if docs_path.exists():
            doc_files = list(docs_path.glob("**/*.md"))
            self.report["metrics"]["documentation_files"] = len(doc_files)
            
            # Check for key documentation
            expected_docs = ["getting-started", "api", "c2ps", "integration", "architecture"]
            found_docs = []
            for doc in doc_files:
                content = doc.stem.lower()
                for expected in expected_docs:
                    if expected in content:
                        found_docs.append(expected)
                        
            missing_docs = set(expected_docs) - set(found_docs)
            for doc in missing_docs:
                self.report["warnings"].append(f"Missing documentation for: {doc}")
                
    def analyze_code_quality(self):
        """Basic code quality metrics"""
        print("🎯 Analyzing code quality...")
        
        total_lines = 0
        total_files = 0
        languages = defaultdict(int)
        
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'venv', '__pycache__']]
            
            for file in files:
                filepath = Path(root) / file
                if filepath.suffix in ['.py', '.js', '.ts', '.jsx', '.tsx']:
                    total_files += 1
                    languages[filepath.suffix] += 1
                    try:
                        with open(filepath) as f:
                            total_lines += len(f.readlines())
                    except:
                        pass
                        
        self.report["metrics"]["total_source_files"] = total_files
        self.report["metrics"]["total_lines_of_code"] = total_lines
        self.report["metrics"]["languages"] = dict(languages)
        
    def check_test_coverage(self):
        """Check for test files and coverage"""
        print("🧪 Checking test coverage...")
        
        test_patterns = ["test_*.py", "*_test.py", "*.test.js", "*.test.ts", "*.spec.js", "*.spec.ts"]
        test_files = []
        
        for pattern in test_patterns:
            test_files.extend(self.root_path.glob(f"**/{pattern}"))
            
        self.report["metrics"]["test_files"] = len(test_files)
        
        if len(test_files) == 0:
            self.report["critical_issues"].append("No test files found")
        elif len(test_files) < 10:
            self.report["warnings"].append(f"Limited test coverage: only {len(test_files)} test files found")
            
    def check_ci_cd(self):
        """Check for CI/CD configuration"""
        print("🔄 Checking CI/CD setup...")
        
        github_workflows = self.root_path / ".github" / "workflows"
        if github_workflows.exists():
            workflows = list(github_workflows.glob("*.yml")) + list(github_workflows.glob("*.yaml"))
            self.report["metrics"]["github_workflows"] = len(workflows)
            if workflows:
                self.report["recommendations"].append(f"✅ GitHub Actions configured ({len(workflows)} workflows)")
        else:
            self.report["warnings"].append("No GitHub Actions workflows found")
            
    def check_trademark_concerns(self):
        """Check for trademark and branding consistency"""
        print("™️ Checking trademark concerns...")
        
        # Look for consistent branding
        brand_mentions = []
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'venv']]
            
            for file in files:
                if file.endswith(('.md', '.txt', '.js', '.py', '.ts')):
                    filepath = Path(root) / file
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if re.search(r'Perswade', content, re.IGNORECASE):
                                brand_mentions.append(filepath.relative_to(self.root_path))
                    except:
                        pass
                        
        self.report["metrics"]["brand_mentions"] = len(brand_mentions)
        
        # Check for trademark policy
        if not (self.root_path / "TRADEMARK.md").exists():
            self.report["warnings"].append("No TRADEMARK.md policy file found")
            
    def check_assemblyai_integration(self):
        """Verify AssemblyAI integration setup"""
        print("🎤 Checking AssemblyAI integration...")
        
        assemblyai_files = []
        for ext in ['.py', '.js', '.ts']:
            for file in self.root_path.glob(f"**/*{ext}"):
                try:
                    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if 'assemblyai' in content.lower() or 'assembly' in content.lower():
                            assemblyai_files.append(file.relative_to(self.root_path))
                except:
                    pass
                    
        if assemblyai_files:
            self.report["metrics"]["assemblyai_integration_files"] = len(assemblyai_files)
            self.report["recommendations"].append(f"✅ AssemblyAI integration found in {len(assemblyai_files)} files")
        else:
            self.report["warnings"].append("No AssemblyAI integration code found")
            
    def analyze_c2ps_implementation(self):
        """Check for C²PS methodology implementation"""
        print("🎯 Checking C²PS implementation...")
        
        c2ps_indicators = ["credibility", "commonality", "problem", "solution", "c2ps", "C²PS"]
        c2ps_files = []
        
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'venv']]
            
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.md')):
                    filepath = Path(root) / file
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            if any(indicator.lower() in content for indicator in c2ps_indicators):
                                c2ps_files.append(filepath.relative_to(self.root_path))
                    except:
                        pass
                        
        if c2ps_files:
            self.report["metrics"]["c2ps_implementation_files"] = len(c2ps_files)
            self.report["recommendations"].append(f"✅ C²PS methodology found in {len(c2ps_files)} files")
        else:
            self.report["critical_issues"].append("No C²PS methodology implementation found")
            
    def generate_summary(self):
        """Generate audit summary"""
        critical_count = len(self.report["critical_issues"])
        warning_count = len(self.report["warnings"])
        
        readiness_score = 100
        readiness_score -= critical_count * 15  # Critical issues are serious
        readiness_score -= warning_count * 5    # Warnings are less serious
        readiness_score = max(0, readiness_score)
        
        self.report["summary"] = {
            "audit_date": datetime.now().isoformat(),
            "repository_path": str(self.root_path),
            "readiness_score": readiness_score,
            "critical_issues": critical_count,
            "warnings": warning_count,
            "recommendations": len(self.report["recommendations"])
        }
        
    def generate_markdown_report(self) -> str:
        """Generate comprehensive markdown report"""
        report_lines = [
            "# 🚀 Open Source Readiness Audit Report",
            f"\n**Generated:** {self.report['summary']['audit_date']}",
            f"**Repository:** `{self.report['summary']['repository_path']}`",
            f"\n## 📊 Executive Summary",
            f"\n### Readiness Score: {self.report['summary']['readiness_score']}/100",
            "",
            f"- **Critical Issues:** {self.report['summary']['critical_issues']} ⚠️",
            f"- **Warnings:** {self.report['summary']['warnings']} ⚡",
            f"- **Recommendations:** {self.report['summary']['recommendations']} ✅",
            ""
        ]
        
        # Readiness Assessment
        score = self.report['summary']['readiness_score']
        if score >= 80:
            assessment = "✅ **Ready for Open Source** - Minor improvements recommended"
        elif score >= 60:
            assessment = "⚡ **Nearly Ready** - Address critical issues before launch"
        else:
            assessment = "⚠️ **Not Ready** - Significant work required"
            
        report_lines.extend([
            f"### Overall Assessment: {assessment}",
            ""
        ])
        
        # Critical Issues
        if self.report["critical_issues"]:
            report_lines.extend([
                "## 🚨 Critical Issues (Must Fix)",
                ""
            ])
            for issue in self.report["critical_issues"]:
                report_lines.append(f"- {issue}")
            report_lines.append("")
            
        # Warnings
        if self.report["warnings"]:
            report_lines.extend([
                "## ⚡ Warnings (Should Fix)",
                ""
            ])
            for warning in self.report["warnings"]:
                report_lines.append(f"- {warning}")
            report_lines.append("")
            
        # Recommendations
        if self.report["recommendations"]:
            report_lines.extend([
                "## ✅ Positive Findings",
                ""
            ])
            for rec in self.report["recommendations"]:
                report_lines.append(f"- {rec}")
            report_lines.append("")
            
        # Metrics
        report_lines.extend([
            "## 📈 Code Metrics",
            ""
        ])
        for metric, value in self.report["metrics"].items():
            if isinstance(value, dict):
                report_lines.append(f"**{metric.replace('_', ' ').title()}:**")
                for k, v in value.items():
                    report_lines.append(f"  - {k}: {v}")
            else:
                report_lines.append(f"- **{metric.replace('_', ' ').title()}:** {value}")
        report_lines.append("")
        
        # MIT License Checklist
        report_lines.extend([
            "## 📋 MIT License Readiness Checklist",
            "",
            "### Required Files:",
            f"- {'✅' if (self.root_path / 'LICENSE').exists() else '❌'} LICENSE (MIT)",
            f"- {'✅' if (self.root_path / 'README.md').exists() else '❌'} README.md",
            f"- {'✅' if (self.root_path / 'CONTRIBUTING.md').exists() else '❌'} CONTRIBUTING.md",
            f"- {'✅' if (self.root_path / 'CODE_OF_CONDUCT.md').exists() else '❌'} CODE_OF_CONDUCT.md",
            f"- {'✅' if (self.root_path / 'SECURITY.md').exists() else '❌'} SECURITY.md",
            f"- {'✅' if (self.root_path / '.gitignore').exists() else '❌'} .gitignore",
            "",
            "### Trademark Protection:",
            f"- {'✅' if (self.root_path / 'TRADEMARK.md').exists() else '❌'} TRADEMARK.md policy",
            "- ⚠️ Register 'Perswade' trademark before launch",
            "",
            "### Repository Structure:",
            f"- {'✅' if self.report['metrics'].get('monorepo') else '❌'} Monorepo structure",
            f"- {'✅' if (self.root_path / 'packages').exists() else '❌'} packages/ directory",
            f"- {'✅' if (self.root_path / 'apps').exists() else '❌'} apps/ directory",
            f"- {'✅' if (self.root_path / 'docs').exists() else '❌'} docs/ directory",
            ""
        ])
        
        # Action Items
        report_lines.extend([
            "## 🎯 Priority Action Items",
            "",
            "### Immediate (Before Open Source):",
            "1. Remove all API keys and sensitive data",
            "2. Add MIT LICENSE file with proper copyright",
            "3. Add copyright headers to all source files",
            "4. Create comprehensive README with:",
            "   - Quick start guide",
            "   - Live demo link",
            "   - Architecture diagram",
            "   - Performance metrics",
            "5. Set up GitHub Actions CI/CD",
            "",
            "### Pre-Launch (1 Week Before):",
            "1. Register 'Perswade' trademark",
            "2. Create TRADEMARK.md policy",
            "3. Prepare demo site (demo.perswade.ai)",
            "4. Record demo video",
            "5. Write launch blog post",
            "",
            "### Launch Day:",
            "1. Tag v1.0.0 release",
            "2. Submit to Hacker News",
            "3. Launch on Product Hunt",
            "4. Post on Reddit (r/opensource, r/sales)",
            "5. Publish technical article on Dev.to",
            ""
        ])
        
        # Next Steps
        report_lines.extend([
            "## 🚀 Next Steps",
            "",
            "1. **Review this audit** with your team",
            "2. **Fix critical issues** identified above",
            "3. **Run audit again** after fixes",
            "4. **Prepare launch materials** per the strategy document",
            "5. **Set launch date** once readiness score > 80",
            "",
            "---",
            f"*Audit completed in alignment with Strategic Open Source Roadmap for Perswade*"
        ])
        
        return "\n".join(report_lines)


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Open Source Readiness Audit for Perswade")
    parser.add_argument("--path", default=".", help="Path to repository root")
    parser.add_argument("--output", default="opensource-audit-report.md", help="Output file name")
    args = parser.parse_args()
    
    # Run audit
    auditor = OpenSourceAudit(args.path)
    report = auditor.run_audit()
    
    # Generate markdown report
    markdown_report = auditor.generate_markdown_report()
    
    # Save report
    output_path = Path(args.output)
    with open(output_path, 'w') as f:
        f.write(markdown_report)
    
    print(f"\n✅ Audit complete! Report saved to: {output_path}")
    print(f"📊 Readiness Score: {report['summary']['readiness_score']}/100")
    
    # Also save JSON version for programmatic access
    json_output = output_path.with_suffix('.json')
    with open(json_output, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print(f"📄 JSON report saved to: {json_output}")
    
    return report['summary']['readiness_score']


if __name__ == "__main__":
    exit_code = 0 if main() >= 60 else 1
    exit(exit_code)
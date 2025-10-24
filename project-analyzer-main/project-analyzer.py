import os
import re
import json
import math
import asyncio
from pathlib import Path
from collections import Counter, defaultdict, deque
from typing import Dict, List, Tuple, Any, Set, Optional
import datetime
import hashlib
import subprocess
import tempfile

import humanize
import networkx as nx
import numpy as np
import pandas as pd
from git import Repo, GitCommandError
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
import plotly.graph_objects as go
import plotly.express as px
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import webbrowser
from threading import Timer

class PredictiveRiskAnalyzer:
    """Predictive risk modeling using ML and historical data"""
    
    def __init__(self):
        self.risk_model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        
    def extract_risk_features(self, file_info: Dict, git_history: Dict, complexity_metrics: Dict) -> List[float]:
        """Extract features for risk prediction"""
        features = []
        
        # Code complexity features
        features.extend([
            file_info.get('cognitive_complexity', 0),
            complexity_metrics.get('cyclomatic_complexity', 0),
            complexity_metrics.get('halstead_difficulty', 0),
            file_info.get('code_lines', 0),
            file_info.get('comment_ratio', 0),
        ])
        
        # Git history features
        file_path = str(file_info['path'])
        git_stats = git_history.get('file_churn', {}).get(file_path, {})
        features.extend([
            git_stats.get('commits', 0),
            git_stats.get('additions', 0),
            git_stats.get('deletions', 0),
            git_stats.get('additions', 0) / max(git_stats.get('deletions', 1), 1),  # Churn ratio
        ])
        
        # Temporal features
        file_age_days = self.get_file_age_days(file_info, git_history)
        features.append(file_age_days)
        
        # Dependency features
        features.extend([
            complexity_metrics.get('afferent_coupling', 0),  # Incoming dependencies
            complexity_metrics.get('efferent_coupling', 0),  # Outgoing dependencies
        ])
        
        return features
    
    def get_file_age_days(self, file_info: Dict, git_history: Dict) -> float:
        """Calculate file age in days"""
        if not git_history or 'file_ages' not in git_history:
            return 365.0  # Default to 1 year
        
        file_path = str(file_info['path'])
        if file_path in git_history['file_ages']:
            file_age = git_history['file_ages'][file_path]
            days_old = (datetime.datetime.now() - file_age).days
            return float(days_old)
        
        return 365.0
    
    def train_risk_model(self, training_data: List[Tuple[List[float], int]]):
        """Train a simple risk prediction model"""
        if not training_data:
            return
            
        X, y = zip(*training_data)
        X = np.array(X)
        y = np.array(y)
        
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        
        self.risk_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.risk_model.fit(X_scaled, y)
        
        self.feature_names = [
            'cognitive_complexity', 'cyclomatic_complexity', 'halstead_difficulty',
            'code_lines', 'comment_ratio', 'commit_count', 'additions', 'deletions',
            'churn_ratio', 'file_age_days', 'afferent_coupling', 'efferent_coupling'
        ]
    
    def predict_risk(self, features: List[float]) -> float:
        """Predict risk score (0-1) for a file"""
        if self.risk_model is None:
            # Fallback heuristic if no model trained
            complexity = features[0] if features else 0
            churn = features[5] if len(features) > 5 else 0
            return min(1.0, (complexity * churn) / 1000.0)
        
        features_scaled = self.scaler.transform([features])
        risk_prob = self.risk_model.predict_proba(features_scaled)[0][1]
        return risk_prob

class DynamicCallGraphAnalyzer:
    """Dynamic call graph analysis and impact simulation"""
    
    def __init__(self):
        self.call_graph = nx.DiGraph()
        self.function_locations = {}
        
    def build_call_graph(self, files_data: List[Dict]):
        """Build static call graph from code analysis"""
        for file_info in files_data:
            if file_info['language'] in ['Python', 'JavaScript', 'TypeScript', 'Java']:
                self.analyze_file_calls(file_info)
    
    def analyze_file_calls(self, file_info: Dict):
        """Analyze function calls within a file"""
        content = file_info.get('content', '')
        file_path = str(file_info['path'])
        
        if file_info['language'] == 'Python':
            self.analyze_python_calls(content, file_path)
        elif file_info['language'] in ['JavaScript', 'TypeScript']:
            self.analyze_javascript_calls(content, file_path)
    
    def analyze_python_calls(self, content: str, file_path: str):
        """Extract Python function calls and definitions"""
        # Simple regex-based approach (would use AST in production)
        function_defs = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', content)
        function_calls = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', content)
        
        # Add function definitions as nodes
        for func in function_defs:
            node_id = f"{file_path}::{func}"
            self.call_graph.add_node(node_id, type='function', file=file_path)
            self.function_locations[func] = file_path
        
        # Add call edges (simplified)
        for call in function_calls:
            if call in function_defs:  # Internal call
                caller = f"{file_path}::current"  # Simplified
                callee = f"{file_path}::{call}"
                self.call_graph.add_edge(caller, callee)
            elif call in self.function_locations:  # Cross-file call
                caller = f"{file_path}::current"
                callee = f"{self.function_locations[call]}::{call}"
                self.call_graph.add_edge(caller, callee)
    
    def analyze_javascript_calls(self, content: str, file_path: str):
        """Extract JavaScript function calls and definitions"""
        function_defs = re.findall(r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', content)
        function_defs.extend(re.findall(r'const\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\(', content))
        function_defs.extend(re.findall(r'let\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\(', content))
        
        function_calls = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', content)
        
        for func in function_defs:
            node_id = f"{file_path}::{func}"
            self.call_graph.add_node(node_id, type='function', file=file_path)
        
        for call in function_calls:
            if call in function_defs:
                caller = f"{file_path}::current"
                callee = f"{file_path}::{call}"
                self.call_graph.add_edge(caller, callee)
    
    def simulate_impact(self, target_function: str, change_type: str = "modification") -> Dict:
        """Simulate impact of changing a function"""
        if target_function not in self.call_graph:
            return {"affected_functions": [], "affected_files": set()}
        
        # Find all functions that depend on the target (transitive closure)
        affected_nodes = set()
        if change_type == "deletion":
            # All nodes that directly or indirectly call the target
            affected_nodes = nx.descendants(self.call_graph, target_function)
        else:  # modification
            # Direct callers are most affected
            affected_nodes = set(self.call_graph.predecessors(target_function))
        
        affected_files = {self.call_graph.nodes[node].get('file', '') for node in affected_nodes}
        
        return {
            "affected_functions": list(affected_nodes),
            "affected_files": affected_files,
            "impact_score": len(affected_nodes) / max(len(self.call_graph.nodes), 1)
        }
    
    def identify_hot_paths(self, execution_data: Optional[Dict] = None) -> List[List[str]]:
        """Identify critical execution paths"""
        if execution_data:
            # Use actual execution data if available
            return self.analyze_execution_paths(execution_data)
        else:
            # Use graph centrality measures
            betweenness = nx.betweenness_centrality(self.call_graph)
            central_nodes = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
            return [[node] for node, _ in central_nodes]
    
    def analyze_execution_paths(self, execution_data: Dict) -> List[List[str]]:
        """Analyze actual execution paths from profiling data"""
        # This would integrate with actual profiling data
        return []

class EcosystemIntelligence:
    """Dependency ecosystem and supply chain analysis"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.dependency_tree = {}
        self.vulnerabilities = {}
        
    def analyze_dependencies(self) -> Dict:
        """Analyze project dependencies and their security"""
        dependencies = {}
        
        # Python dependencies
        requirements_files = list(self.project_path.glob("**/requirements.txt"))
        for req_file in requirements_files:
            dependencies.update(self.analyze_python_dependencies(req_file))
        
        # Node.js dependencies
        package_files = list(self.project_path.glob("**/package.json"))
        for pkg_file in package_files:
            dependencies.update(self.analyze_node_dependencies(pkg_file))
        
        # Analyze vulnerability reachability
        self.analyze_vulnerability_reachability(dependencies)
        
        return dependencies
    
    def analyze_python_dependencies(self, requirements_file: Path) -> Dict:
        """Analyze Python dependencies from requirements.txt"""
        dependencies = {}
        
        try:
            with open(requirements_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Parse package name and version
                        if '==' in line:
                            pkg, version = line.split('==', 1)
                        elif '>=' in line:
                            pkg, version = line.split('>=', 1)
                        else:
                            pkg, version = line, 'unknown'
                        
                        dependencies[pkg.strip()] = {
                            'version': version.strip(),
                            'type': 'python',
                            'file': str(requirements_file),
                            'reachable': self.is_package_reachable(pkg.strip())
                        }
        except Exception as e:
            print(f"Error analyzing {requirements_file}: {e}")
        
        return dependencies
    
    def analyze_node_dependencies(self, package_file: Path) -> Dict:
        """Analyze Node.js dependencies from package.json"""
        dependencies = {}
        
        try:
            with open(package_file, 'r') as f:
                package_data = json.load(f)
            
            # Dependencies
            for dep_type in ['dependencies', 'devDependencies']:
                if dep_type in package_data:
                    for pkg, version in package_data[dep_type].items():
                        dependencies[pkg] = {
                            'version': version,
                            'type': 'nodejs',
                            'file': str(package_file),
                            'reachable': self.is_package_reachable(pkg)
                        }
        except Exception as e:
            print(f"Error analyzing {package_file}: {e}")
        
        return dependencies
    
    def is_package_reachable(self, package_name: str) -> bool:
        """Check if a package is actually used in the codebase"""
        # Simple grep-based approach (would use AST in production)
        try:
            # Check for import/require statements
            result = subprocess.run([
                'grep', '-r', '--include=*.py', '--include=*.js', '--include=*.ts',
                package_name, str(self.project_path)
            ], capture_output=True, text=True)
            
            return result.returncode == 0 and len(result.stdout.strip()) > 0
        except:
            return True  # Default to true if we can't determine
    
    def analyze_vulnerability_reachability(self, dependencies: Dict):
        """Analyze which vulnerabilities are actually reachable"""
        # This would integrate with Snyk, OSV, or other vulnerability databases
        for pkg, info in dependencies.items():
            info['vulnerabilities'] = self.check_package_vulnerabilities(pkg, info['version'])
            info['update_readiness'] = self.calculate_update_readiness(pkg, info['version'])
    
    def check_package_vulnerabilities(self, package: str, version: str) -> List[Dict]:
        """Check for known vulnerabilities (placeholder implementation)"""
        # In production, this would call Snyk API, OSV API, etc.
        return []
    
    def calculate_update_readiness(self, package: str, current_version: str) -> float:
        """Calculate how ready the codebase is to update this package"""
        # Analyze usage patterns and breaking changes
        return 0.8  # Placeholder

class AIAugmentedUnderstanding:
    """AI-powered code understanding and documentation analysis"""
    
    def __init__(self):
        self.embedding_model = None
        self.code_embeddings = {}
        
    def load_models(self):
        """Load AI models for code understanding"""
        try:
            # Use a lightweight model for code embeddings
            # Disabled for quick demo - requires internet connection
            # self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            pass
        except Exception as e:
            print(f"Warning: Could not load embedding model: {e}")
    
    def analyze_documentation_quality(self, docstring: str, function_code: str) -> Dict:
        """Analyze documentation quality using heuristic rules"""
        if not docstring:
            return {"score": 0.0, "issues": ["Missing documentation"]}
        
        issues = []
        score = 5.0  # Start with medium score
        
        # Check for common documentation issues
        if len(docstring) < 20:
            issues.append("Documentation too short")
            score -= 2
        
        if "TODO" in docstring or "FIXME" in docstring:
            issues.append("Documentation contains TODOs")
            score -= 1
        
        # Check if documentation explains "why" not just "what"
        why_indicators = ['because', 'since', 'therefore', 'in order to']
        has_why = any(indicator in docstring.lower() for indicator in why_indicators)
        if not has_why:
            issues.append("Documentation may not explain purpose")
            score -= 1
        
        # Check parameter documentation
        if 'param' not in docstring.lower() and function_code:
            # Try to detect parameters in function
            params = self.extract_function_parameters(function_code)
            if params and len(params) > 1:
                issues.append("Parameters may not be documented")
                score -= 1
        
        return {
            "score": max(0.0, min(10.0, score)),
            "issues": issues,
            "has_why_explanation": has_why
        }
    
    def extract_function_parameters(self, function_code: str) -> List[str]:
        """Extract function parameters from code"""
        # Simple regex approach
        param_matches = re.findall(r'def\s+\w+\((.*?)\)', function_code, re.DOTALL)
        if param_matches:
            params = [p.strip() for p in param_matches[0].split(',')]
            return [p for p in params if p and p != 'self']
        return []
    
    def detect_intent_mismatch(self, function_name: str, function_code: str, comments: str) -> Dict:
        """Detect mismatches between function name and implementation"""
        issues = []
        
        # Analyze function name patterns
        name_lower = function_name.lower()
        
        # Check for common intent mismatches
        if any(verb in name_lower for verb in ['get', 'fetch', 'retrieve']):
            if 'set' in function_code.lower() or '=' in function_code:
                issues.append("Get function appears to modify state")
        
        if 'validate' in name_lower or 'check' in name_lower:
            if not any(keyword in function_code.lower() for keyword in ['if', 'assert', 'raise', 'return false']):
                issues.append("Validation function may not return boolean")
        
        if 'create' in name_lower or 'make' in name_lower:
            if 'delete' in function_code.lower() or 'remove' in function_code.lower():
                issues.append("Creation function appears to delete data")
        
        return {
            "issues": issues,
            "mismatch_score": len(issues) / 3.0  # Normalize
        }
    
    def generate_code_summaries(self, files_data: List[Dict]) -> Dict[str, str]:
        """Generate semantic summaries for code files"""
        summaries = {}
        
        for file_info in files_data:
            if self.embedding_model and file_info.get('content'):
                # Use embedding-based clustering for summary
                summary = self.summarize_file_semantic(file_info)
                summaries[str(file_info['path'])] = summary
        
        return summaries
    
    def summarize_file_semantic(self, file_info: Dict) -> str:
        """Generate semantic summary using embedding clustering"""
        content = file_info.get('content', '')
        language = file_info['language']
        
        # Extract key lines for summary
        lines = content.split('\n')
        key_lines = []
        
        # Prioritize function definitions, class definitions, etc.
        for line in lines:
            line_stripped = line.strip()
            if any(pattern in line_stripped for pattern in ['def ', 'class ', 'function ', 'export ', 'public ']):
                key_lines.append(line_stripped)
                if len(key_lines) >= 5:  # Limit summary size
                    break
        
        summary = f"{language} file with {len(key_lines)} key elements"
        if key_lines:
            summary += ": " + "; ".join(key_lines[:3])
        
        return summary

class CodebaseDNAMapper:
    """Track code evolution and lineage"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.code_fingerprints = {}
        
    def analyze_code_evolution(self, git_analysis: Dict) -> Dict:
        """Analyze code evolution patterns"""
        evolution_metrics = {}
        
        if not git_analysis or 'file_churn' not in git_analysis:
            return evolution_metrics
        
        # Calculate code stability metrics
        stable_files = []
        volatile_files = []
        
        for file_path, stats in git_analysis['file_churn'].items():
            churn_rate = stats['commits'] / max(stats.get('age_days', 365), 1)
            
            if churn_rate < 0.01:  # Less than 1 commit per 100 days
                stable_files.append(file_path)
            elif churn_rate > 0.1:  # More than 1 commit per 10 days
                volatile_files.append(file_path)
        
        evolution_metrics.update({
            'stable_files_count': len(stable_files),
            'volatile_files_count': len(volatile_files),
            'stability_ratio': len(stable_files) / max(len(git_analysis['file_churn']), 1),
            'most_stable_files': stable_files[:10],
            'most_volatile_files': volatile_files[:10]
        })
        
        return evolution_metrics
    
    def track_lineage(self, file_path: str, git_analysis: Dict) -> Dict:
        """Track code lineage for a specific file"""
        lineage = {
            'file': file_path,
            'total_commits': 0,
            'authors': set(),
            'major_changes': 0,
            'line_history': []
        }
        
        if git_analysis and 'file_churn' in git_analysis:
            file_stats = git_analysis['file_churn'].get(file_path, {})
            lineage.update({
                'total_commits': file_stats.get('commits', 0),
                'additions': file_stats.get('additions', 0),
                'deletions': file_stats.get('deletions', 0)
            })
        
        return lineage
    
    def detect_refactoring_patterns(self, git_analysis: Dict) -> List[Dict]:
        """Detect code refactoring patterns from history"""
        refactorings = []
        
        # This would require detailed commit message analysis and diff analysis
        # Placeholder implementation
        return refactorings

class AdvancedProjectAnalyzer:
    """Base project analyzer with core functionality"""
    
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.language_extensions = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.h': 'C/C++ Header',
            '.cs': 'C#', '.go': 'Go', '.rs': 'Rust', '.rb': 'Ruby',
            '.php': 'PHP', '.swift': 'Swift', '.kt': 'Kotlin',
            '.scala': 'Scala', '.html': 'HTML', '.css': 'CSS',
            '.jsx': 'React', '.tsx': 'TypeScript React', '.vue': 'Vue',
            '.sql': 'SQL', '.sh': 'Shell', '.bash': 'Bash',
            '.json': 'JSON', '.xml': 'XML', '.yaml': 'YAML', '.yml': 'YAML'
        }
    
    def collect_project_data(self) -> Tuple[Dict, Dict]:
        """Collect basic project data"""
        files_data = []
        git_analysis = {}
        
        # Walk through project directory
        for root, dirs, files in os.walk(self.project_path):
            # Skip common non-source directories
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', 'venv', '.env']]
            
            for file in files:
                file_path = Path(root) / file
                
                try:
                    file_info = self.analyze_file(file_path)
                    if file_info:
                        files_data.append(file_info)
                except Exception as e:
                    print(f"Error analyzing {file_path}: {e}")
        
        # Try to get git analysis
        try:
            if (self.project_path / '.git').exists():
                git_analysis = self.analyze_git_history()
        except Exception as e:
            print(f"Git analysis skipped: {e}")
        
        return {'files': files_data}, {'git_analysis': git_analysis}
    
    def analyze_file(self, file_path: Path) -> Optional[Dict]:
        """Analyze a single file"""
        ext = file_path.suffix.lower()
        language = self.language_extensions.get(ext, 'Unknown')
        
        try:
            stat = file_path.stat()
            size = stat.st_size
            
            # Skip very large files
            if size > 10 * 1024 * 1024:  # 10MB
                return None
            
            # Read file content for text files
            content = ""
            code_lines = 0
            comment_lines = 0
            blank_lines = 0
            
            if language != 'Unknown' and size < 1024 * 1024:  # 1MB
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        lines = content.split('\n')
                        
                        for line in lines:
                            stripped = line.strip()
                            if not stripped:
                                blank_lines += 1
                            elif stripped.startswith('#') or stripped.startswith('//'):
                                comment_lines += 1
                            else:
                                code_lines += 1
                except:
                    pass
            
            return {
                'path': file_path,
                'name': file_path.name,
                'extension': ext,
                'language': language,
                'size': size,
                'content': content,
                'code_lines': code_lines,
                'comment_lines': comment_lines,
                'blank_lines': blank_lines,
                'total_lines': code_lines + comment_lines + blank_lines,
                'comment_ratio': comment_lines / max(code_lines + comment_lines, 1),
                'cognitive_complexity': self.calculate_cognitive_complexity(content, language)
            }
        except Exception as e:
            return None
    
    def calculate_cognitive_complexity(self, content: str, language: str) -> int:
        """Calculate cognitive complexity score"""
        if not content:
            return 0
        
        complexity = 0
        
        # Count nesting indicators
        nesting_keywords = ['if', 'for', 'while', 'switch', 'case', 'catch', 'except']
        for keyword in nesting_keywords:
            complexity += content.count(keyword)
        
        # Count functions/methods
        if language == 'Python':
            complexity += content.count('def ')
        elif language in ['JavaScript', 'TypeScript', 'Java', 'C++', 'C#']:
            complexity += content.count('function ')
            complexity += content.count('=> ')
        
        return complexity
    
    def analyze_git_history(self) -> Dict:
        """Analyze git history"""
        try:
            repo = Repo(self.project_path)
            
            file_churn = defaultdict(lambda: {'commits': 0, 'additions': 0, 'deletions': 0})
            file_ages = {}
            
            # Analyze recent commits (limit for performance)
            commits = list(repo.iter_commits('HEAD', max_count=100))
            
            for commit in commits:
                for item in commit.stats.files:
                    file_churn[item]['commits'] += 1
                    file_churn[item]['additions'] += commit.stats.files[item]['insertions']
                    file_churn[item]['deletions'] += commit.stats.files[item]['deletions']
                    
                    if item not in file_ages:
                        file_ages[item] = commit.committed_datetime
            
            return {
                'file_churn': dict(file_churn),
                'file_ages': file_ages,
                'total_commits': len(commits)
            }
        except Exception as e:
            return {}
    
    def calculate_metrics(self, data: Dict) -> Dict:
        """Calculate basic metrics"""
        files = data['files']
        
        metrics = {
            'total_files': len(files),
            'total_size': sum(f['size'] for f in files),
            'total_lines': sum(f['total_lines'] for f in files),
            'code_lines': sum(f['code_lines'] for f in files),
            'comment_lines': sum(f['comment_lines'] for f in files),
            'blank_lines': sum(f['blank_lines'] for f in files),
        }
        
        # Language distribution
        language_stats = defaultdict(lambda: {'count': 0, 'lines': 0})
        for f in files:
            lang = f['language']
            language_stats[lang]['count'] += 1
            language_stats[lang]['lines'] += f['code_lines']
        
        total_code_lines = max(metrics['code_lines'], 1)
        metrics['language_distribution'] = {
            lang: {
                'count': stats['count'],
                'lines': stats['lines'],
                'percentage': (stats['lines'] / total_code_lines) * 100
            }
            for lang, stats in language_stats.items()
        }
        
        return metrics
    
    def generate_report(self, metrics: Dict) -> str:
        """Generate basic text report"""
        report = []
        
        report.append("=" * 80)
        report.append(">>>> PROJECT ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        report.append(">>� FILE & DIRECTORY STRUCTURE")
        report.append("-" * 40)
        report.append(f"Total Files: {metrics['total_files']:,}")
        report.append(f"Total Size: {humanize.naturalsize(metrics['total_size'])}")
        report.append("")
        
        report.append(">>� CODE METRICS")
        report.append("-" * 40)
        report.append(f"Total Lines: {metrics['total_lines']:,}")
        report.append(f"Code Lines: {metrics['code_lines']:,}")
        report.append(f"Comment Lines: {metrics['comment_lines']:,}")
        report.append(f"Blank Lines: {metrics['blank_lines']:,}")
        report.append("")
        
        report.append(">>� PROGRAMMING LANGUAGES")
        report.append("-" * 40)
        for lang, stats in sorted(metrics['language_distribution'].items(), 
                                   key=lambda x: x[1]['percentage'], reverse=True)[:10]:
            report.append(f"{lang:20} {stats['percentage']:5.1f}% ({stats['count']:3} files, {stats['lines']:6} lines)")
        
        return '\n'.join(report)
    
    def generate_advanced_report(self, basic_metrics: Dict, git_analysis: Dict, advanced_metrics: Dict) -> str:
        """Generate advanced analysis report"""
        report = []
        
        report.append("=" * 80)
        report.append(">>>> ADVANCED ANALYSIS")
        report.append("=" * 80)
        report.append("")
        
        if git_analysis and git_analysis.get('file_churn'):
            report.append(">>>> CODE CHURN & STABILITY")
            report.append("-" * 40)
            
            churn = git_analysis['file_churn']
            sorted_churn = sorted(churn.items(), key=lambda x: x[1]['commits'], reverse=True)[:5]
            
            report.append("Most Modified Files:")
            for file_path, stats in sorted_churn:
                report.append(f"  {Path(file_path).name}: {stats['commits']} commits")
            report.append("")
        
        return '\n'.join(report)

class NextGenProjectAnalyzer(AdvancedProjectAnalyzer):
    """Next-generation project analyzer with predictive analytics and AI"""
    
    def __init__(self, project_path):
        super().__init__(project_path)
        self.predictive_analyzer = PredictiveRiskAnalyzer()
        self.call_graph_analyzer = DynamicCallGraphAnalyzer()
        self.ecosystem_analyzer = EcosystemIntelligence(self.project_path)
        self.ai_understanding = AIAugmentedUnderstanding()
        self.dna_mapper = CodebaseDNAMapper(self.project_path)
        
        # Load AI models
        self.ai_understanding.load_models()
    
    def analyze_advanced_metrics(self, basic_data: Dict, git_analysis: Dict) -> Dict:
        """Perform next-generation advanced analysis"""
        print(">>>> Running predictive risk analysis...")
        risk_analysis = self.analyze_predictive_risk(basic_data['files'], git_analysis)
        
        print(">>>>>> Building dynamic call graph...")
        self.call_graph_analyzer.build_call_graph(basic_data['files'])
        call_graph_analysis = self.analyze_call_graph_patterns()
        
        print(">>>> Analyzing ecosystem intelligence...")
        ecosystem_analysis = self.ecosystem_analyzer.analyze_dependencies()
        
        print(">>>> Running AI-augmented understanding...")
        ai_analysis = self.ai_understanding.generate_code_summaries(basic_data['files'])
        
        print(">>>> Mapping code evolution DNA...")
        evolution_analysis = self.dna_mapper.analyze_code_evolution(git_analysis)
        
        return {
            'predictive_risk': risk_analysis,
            'call_graph': call_graph_analysis,
            'ecosystem': ecosystem_analysis,
            'ai_understanding': ai_analysis,
            'code_evolution': evolution_analysis
        }
    
    def analyze_predictive_risk(self, files_data: List[Dict], git_analysis: Dict) -> Dict:
        """Analyze predictive risk for all files"""
        risk_scores = {}
        
        for file_info in files_data:
            # Extract features for risk prediction
            complexity_metrics = {
                'cyclomatic_complexity': file_info.get('cognitive_complexity', 0) / 10.0,  # Simplified
                'halstead_difficulty': file_info.get('cognitive_complexity', 0) / 5.0,
                'afferent_coupling': len(self.call_graph_analyzer.call_graph.in_edges(str(file_info['path']))),
                'efferent_coupling': len(self.call_graph_analyzer.call_graph.out_edges(str(file_info['path']))),
            }
            
            features = self.predictive_analyzer.extract_risk_features(
                file_info, git_analysis, complexity_metrics
            )
            
            risk_score = self.predictive_analyzer.predict_risk(features)
            risk_scores[str(file_info['path'])] = {
                'risk_score': risk_score,
                'features': dict(zip(self.predictive_analyzer.feature_names[:len(features)], features)),
                'risk_level': self.classify_risk_level(risk_score)
            }
        
        # Sort by risk score
        high_risk_files = sorted(
            [(path, data['risk_score']) for path, data in risk_scores.items()],
            key=lambda x: x[1], reverse=True
        )[:10]
        
        return {
            'risk_scores': risk_scores,
            'high_risk_files': high_risk_files,
            'average_risk': np.mean([data['risk_score'] for data in risk_scores.values()]) if risk_scores else 0
        }
    
    def classify_risk_level(self, risk_score: float) -> str:
        """Classify risk level based on score"""
        if risk_score > 0.8:
            return "CRITICAL"
        elif risk_score > 0.6:
            return "HIGH"
        elif risk_score > 0.4:
            return "MEDIUM"
        elif risk_score > 0.2:
            return "LOW"
        else:
            return "VERY_LOW"
    
    def analyze_call_graph_patterns(self) -> Dict:
        """Analyze call graph patterns and critical paths"""
        call_graph = self.call_graph_analyzer.call_graph
        
        if len(call_graph.nodes) == 0:
            return {"error": "No call graph data available"}
        
        # Calculate graph metrics
        try:
            betweenness = nx.betweenness_centrality(call_graph)
            centrality = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Find potential bottlenecks (high betweenness)
            bottlenecks = [node for node, score in centrality if score > 0.1]
            
            # Analyze connectivity
            if nx.is_weakly_connected(call_graph):
                diameter = nx.diameter(call_graph)
            else:
                diameter = float('inf')
            
            return {
                'total_nodes': len(call_graph.nodes),
                'total_edges': len(call_graph.edges),
                'graph_density': nx.density(call_graph),
                'graph_diameter': diameter,
                'central_functions': centrality,
                'bottlenecks': bottlenecks,
                'hot_paths': self.call_graph_analyzer.identify_hot_paths()
            }
        except Exception as e:
            return {"error": f"Graph analysis failed: {str(e)}"}
    
    def simulate_architecture_changes(self, changes: List[Dict]) -> Dict:
        """Simulate the impact of architectural changes"""
        impacts = {}
        
        for change in changes:
            change_type = change.get('type', 'modification')
            target = change.get('target')
            
            if change_type == 'delete_file':
                # Simulate file deletion impact
                impact = self.simulate_file_deletion(target)
            elif change_type == 'extract_function':
                # Simulate function extraction
                impact = self.simulate_function_extraction(target, change.get('new_function'))
            else:
                # Generic modification impact
                impact = self.call_graph_analyzer.simulate_impact(target, change_type)
            
            impacts[target] = impact
        
        return impacts
    
    def simulate_file_deletion(self, file_path: str) -> Dict:
        """Simulate impact of deleting a file"""
        # Find all functions in the file
        file_functions = [
            node for node in self.call_graph_analyzer.call_graph.nodes 
            if self.call_graph_analyzer.call_graph.nodes[node].get('file') == file_path
        ]
        
        total_impact = {
            'affected_functions': set(),
            'affected_files': set(),
            'broken_callers': 0
        }
        
        for func in file_functions:
            impact = self.call_graph_analyzer.simulate_impact(func, 'deletion')
            total_impact['affected_functions'].update(impact['affected_functions'])
            total_impact['affected_files'].update(impact['affected_files'])
            total_impact['broken_callers'] += len(impact['affected_functions'])
        
        return total_impact
    
    def simulate_function_extraction(self, target_function: str, new_function: str) -> Dict:
        """Simulate impact of extracting a function"""
        # This would analyze the function's current callers and dependencies
        return {
            'complexity_reduction': 0.1,  # Placeholder
            'affected_callers': list(self.call_graph_analyzer.call_graph.predecessors(target_function)),
            'maintainability_improvement': 0.15
        }
    
    def generate_nextgen_report(self, basic_metrics: Dict, advanced_metrics: Dict, nextgen_metrics: Dict) -> str:
        """Generate comprehensive next-generation report"""
        report = []
        
        report.append("=" * 80)
        report.append(">>>> NEXT-GENERATION CODE INTELLIGENCE REPORT")
        report.append("=" * 80)
        report.append("")
        
        # >>>> Predictive Risk Analysis
        risk_data = nextgen_metrics.get('predictive_risk', {})
        report.append(">>>> PREDICTIVE RISK ANALYSIS")
        report.append("-" * 40)
        
        if risk_data.get('high_risk_files'):
            report.append("Top 5 High-Risk Files:")
            for file_path, risk_score in risk_data['high_risk_files'][:5]:
                report.append(f"  {file_path}: {risk_score:.1%} risk")
            report.append(f"Average Project Risk: {risk_data.get('average_risk', 0):.1%}")
        else:
            report.append("No risk analysis data available")
        report.append("")
        
        # >>>>>> Call Graph Analysis
        call_data = nextgen_metrics.get('call_graph', {})
        report.append(">>>>>> ARCHITECTURAL ANALYSIS")
        report.append("-" * 40)
        report.append(f"Call Graph Size: {call_data.get('total_nodes', 0)} functions, {call_data.get('total_edges', 0)} calls")
        report.append(f"Architecture Density: {call_data.get('graph_density', 0):.3f}")
        
        if call_data.get('bottlenecks'):
            report.append(f"Potential Bottlenecks: {len(call_data['bottlenecks'])} functions")
        report.append("")
        
        # >>>> Ecosystem Intelligence
        eco_data = nextgen_metrics.get('ecosystem', {})
        report.append(">>>> DEPENDENCY ECOSYSTEM")
        report.append("-" * 40)
        report.append(f"Total Dependencies: {len(eco_data)}")
        
        # Count by type
        py_deps = [d for d in eco_data.values() if d.get('type') == 'python']
        js_deps = [d for d in eco_data.values() if d.get('type') == 'nodejs']
        
        report.append(f"Python Dependencies: {len(py_deps)}")
        report.append(f"JavaScript Dependencies: {len(js_deps)}")
        
        # Unreachable dependencies
        unreachable = [pkg for pkg, info in eco_data.items() if not info.get('reachable', True)]
        if unreachable:
            report.append(f"Potentially Unreachable Dependencies: {len(unreachable)}")
        report.append("")
        
        # >>>> AI-Augmented Insights
        ai_data = nextgen_metrics.get('ai_understanding', {})
        report.append(">>>> AI-AUGMENTED INSIGHTS")
        report.append("-" * 40)
        report.append(f"Files with AI Summaries: {len(ai_data)}")
        
        if ai_data:
            sample_files = list(ai_data.keys())[:3]
            for file_path in sample_files:
                summary = ai_data[file_path]
                report.append(f"  {Path(file_path).name}: {summary[:100]}...")
        report.append("")
        
        # >>>> Code Evolution
        evolution_data = nextgen_metrics.get('code_evolution', {})
        report.append(">>>> CODE EVOLUTION DNA")
        report.append("-" * 40)
        report.append(f"Stable Files: {evolution_data.get('stable_files_count', 0)}")
        report.append(f"Volatile Files: {evolution_data.get('volatile_files_count', 0)}")
        report.append(f"Codebase Stability: {evolution_data.get('stability_ratio', 0):.1%}")
        report.append("")
        
        # >>>> Recommendations
        report.append(">>>> RECOMMENDATIONS & INSIGHTS")
        report.append("-" * 40)
        
        recommendations = self.generate_recommendations(basic_metrics, advanced_metrics, nextgen_metrics)
        for i, rec in enumerate(recommendations[:5], 1):
            report.append(f"{i}. {rec}")
        
        return '\n'.join(report)
    
    def generate_recommendations(self, basic_metrics: Dict, advanced_metrics: Dict, nextgen_metrics: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Risk-based recommendations
        risk_data = nextgen_metrics.get('predictive_risk', {})
        if risk_data.get('average_risk', 0) > 0.3:
            recommendations.append("High overall project risk detected. Consider increasing test coverage and code reviews.")
        
        high_risk_files = risk_data.get('high_risk_files', [])
        if len(high_risk_files) > 5:
            recommendations.append(f"Found {len(high_risk_files)} high-risk files. Prioritize refactoring and testing.")
        
        # Architecture recommendations
        call_data = nextgen_metrics.get('call_graph', {})
        if call_data.get('graph_density', 0) > 0.1:
            recommendations.append("High architectural density detected. Consider modularization to reduce coupling.")
        
        if call_data.get('bottlenecks'):
            recommendations.append(f"Found {len(call_data['bottlenecks'])} potential bottlenecks. Review these critical functions.")
        
        # Dependency recommendations
        eco_data = nextgen_metrics.get('ecosystem', {})
        unreachable = [pkg for pkg, info in eco_data.items() if not info.get('reachable', True)]
        if unreachable:
            recommendations.append(f"Found {len(unreachable)} potentially unused dependencies. Consider removing them.")
        
        return recommendations
    
    def analyze(self):
        """Comprehensive next-generation analysis"""
        print(">>>> Starting next-generation project analysis...")
        print(f"Project: {self.project_path}")
        
        # Run basic and advanced analysis
        basic_data, advanced_metrics = self.collect_project_data()
        basic_metrics = self.calculate_metrics(basic_data)
        
        # Run next-generation analysis
        nextgen_metrics = self.analyze_advanced_metrics(basic_data, advanced_metrics['git_analysis'])
        
        # Generate reports
        basic_report = self.generate_report(basic_metrics)
        advanced_report = self.generate_advanced_report(basic_metrics, advanced_metrics['git_analysis'], advanced_metrics)
        nextgen_report = self.generate_nextgen_report(basic_metrics, advanced_metrics, nextgen_metrics)
        
        full_report = basic_report + "\n\n" + advanced_report + "\n\n" + nextgen_report
        
        return full_report, basic_metrics, advanced_metrics, nextgen_metrics

# Real-time Dashboard Server
class CodebaseDashboard:
    """Real-time codebase health dashboard with Flask"""
    
    def __init__(self, analyzer: NextGenProjectAnalyzer):
        self.analyzer = analyzer
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'codebase-analyzer-secret'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.cached_data = None
        self.setup_routes()
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route("/")
        def index():
            return render_template('dashboard.html')
        
        @self.app.route("/health")
        def health():
            return jsonify({
                "status": "healthy", 
                "timestamp": datetime.datetime.now().isoformat()
            })
        
        @self.app.route("/api/analyze")
        def analyze():
            try:
                print(">>� Running analysis...")
                report, basic_metrics, advanced_metrics, nextgen_metrics = self.analyzer.analyze()
                
                self.cached_data = {
                    "basic_metrics": basic_metrics,
                    "advanced_metrics": self.serialize_metrics(advanced_metrics),
                    "nextgen_metrics": self.serialize_metrics(nextgen_metrics),
                    "report": report,
                    "timestamp": datetime.datetime.now().isoformat()
                }
                
                return jsonify(self.cached_data)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route("/api/metrics")
        def get_metrics():
            if self.cached_data:
                return jsonify(self.cached_data)
            return jsonify({"error": "No data available. Run analysis first."}), 404
        
        @self.app.route("/api/visualizations")
        def get_visualizations():
            if not self.cached_data:
                return jsonify({"error": "No data available"}), 404
            
            try:
                visualizations = self.generate_visualizations()
                return jsonify(visualizations)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.socketio.on('connect')
        def handle_connect():
            emit('connected', {'data': 'Connected to dashboard'})
        
        @self.socketio.on('request_update')
        def handle_update_request():
            if self.cached_data:
                emit('metrics_update', self.cached_data)
    
    def serialize_metrics(self, data):
        """Serialize complex data types for JSON"""
        if isinstance(data, dict):
            return {k: self.serialize_metrics(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return [self.serialize_metrics(item) for item in data]
        elif isinstance(data, set):
            return list(data)
        elif isinstance(data, (np.integer, np.floating)):
            return float(data)
        elif isinstance(data, np.ndarray):
            return data.tolist()
        elif isinstance(data, Path):
            return str(data)
        else:
            return data
    
    def generate_visualizations(self):
        """Generate Plotly visualizations"""
        visualizations = {}
        
        if not self.cached_data:
            return visualizations
        
        basic = self.cached_data.get('basic_metrics', {})
        nextgen = self.cached_data.get('nextgen_metrics', {})
        
        # Language distribution pie chart
        if 'language_distribution' in basic:
            lang_data = basic['language_distribution']
            fig = px.pie(
                values=[lang_data[lang]['percentage'] for lang in lang_data],
                names=list(lang_data.keys()),
                title='Language Distribution'
            )
            visualizations['language_distribution'] = fig.to_json()
        
        # Risk scores bar chart
        risk_data = nextgen.get('predictive_risk', {})
        if risk_data.get('high_risk_files'):
            files = [Path(f[0]).name for f in risk_data['high_risk_files'][:10]]
            scores = [f[1] * 100 for f in risk_data['high_risk_files'][:10]]
            
            fig = go.Figure(data=[
                go.Bar(x=files, y=scores, marker_color='indianred')
            ])
            fig.update_layout(
                title='Top 10 High-Risk Files',
                xaxis_title='File',
                yaxis_title='Risk Score (%)',
                xaxis_tickangle=-45
            )
            visualizations['risk_scores'] = fig.to_json()
        
        # Code metrics overview
        if basic:
            metrics_names = ['Total Files', 'Total Lines', 'Code Lines', 'Comment Lines']
            metrics_values = [
                basic.get('total_files', 0),
                basic.get('total_lines', 0),
                basic.get('code_lines', 0),
                basic.get('comment_lines', 0)
            ]
            
            fig = go.Figure(data=[
                go.Bar(x=metrics_names, y=metrics_values, marker_color='lightblue')
            ])
            fig.update_layout(title='Code Metrics Overview')
            visualizations['code_metrics'] = fig.to_json()
        
        return visualizations
    
    def open_browser(self, url):
        """Open browser after a short delay"""
        webbrowser.open(url)
    
    def run(self, host: str = "127.0.0.1", port: int = 5000):
        """Run the dashboard server"""
        url = f"http://{host}:{port}"
        print(f"\n{'='*60}")
        print(f">>>> Dashboard starting at: {url}")
        print(f"{'='*60}\n")
        
        # Open browser after 1.5 seconds
        Timer(1.5, self.open_browser, args=[url]).start()
        
        self.socketio.run(self.app, host=host, port=port, debug=False)

def main():
    """Main function with next-generation capabilities"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Next-generation project analysis with AI and predictive analytics')
    parser.add_argument('project_path', help='Path to the project directory to analyze')
    parser.add_argument('--dashboard', action='store_true', help='Start real-time dashboard')
    parser.add_argument('--port', type=int, default=5000, help='Dashboard port')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.project_path):
        print(f"Error: Path '{args.project_path}' does not exist")
        return
    
    if not os.path.isdir(args.project_path):
        print(f"Error: '{args.project_path}' is not a directory")
        return
    
    analyzer = NextGenProjectAnalyzer(args.project_path)
    
    if args.dashboard:
        print(f">>>> Starting real-time dashboard on port {args.port}...")
        dashboard = CodebaseDashboard(analyzer)
        dashboard.run(port=args.port)
    else:
        report, basic_metrics, advanced_metrics, nextgen_metrics = analyzer.analyze()
        
        # Save comprehensive report
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"nextgen_analysis_{timestamp}.txt"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n>> Full next-generation report saved to: {report_filename}")
        print("\n" + "="*80)
        print("Analysis completed successfully!")
        print(f"Total Files: {basic_metrics.get('total_files', 0)}")
        print(f"Total Lines: {basic_metrics.get('total_lines', 0)}")
        print(f"Languages: {len(basic_metrics.get('language_distribution', {}))}")
        print("="*80)

if __name__ == "__main__":
    main()

"""
Advanced code analyzer for project-wide intelligence and metrics.
Extracted and adapted from project-analyzer-main.
"""

import os
import re
import json
import ast
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Any, Set, Optional
import datetime

try:
    import numpy as np
    import pandas as pd
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    from git import Repo, GitCommandError
    HAS_GIT = True
except ImportError:
    HAS_GIT = False

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False


class CodeMetricsAnalyzer:
    """Analyze code complexity and quality metrics"""
    
    def __init__(self):
        self.metrics = {}
    
    def analyze_python_file(self, content: str) -> Dict:
        """Analyze Python file for complexity metrics"""
        try:
            tree = ast.parse(content)
            
            metrics = {
                'functions': 0,
                'classes': 0,
                'imports': 0,
                'complexity_score': 0,
                'max_nesting': 0,
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    metrics['functions'] += 1
                    metrics['complexity_score'] += self._calculate_function_complexity(node)
                elif isinstance(node, ast.ClassDef):
                    metrics['classes'] += 1
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    metrics['imports'] += 1
            
            return metrics
        except:
            return {'error': 'Failed to parse Python file'}
    
    def _calculate_function_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity for a function"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def analyze_javascript_file(self, content: str) -> Dict:
        """Analyze JavaScript/TypeScript file (basic regex-based)"""
        metrics = {
            'functions': len(re.findall(r'function\s+\w+|const\s+\w+\s*=\s*\(|=>\s*{', content)),
            'classes': len(re.findall(r'class\s+\w+', content)),
            'imports': len(re.findall(r'import\s+.*from|require\(', content)),
            'complexity_score': content.count('if') + content.count('for') + content.count('while'),
        }
        return metrics


class DependencyAnalyzer:
    """Analyze project dependencies and their usage"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.dependencies = {}
    
    def analyze_dependencies(self) -> Dict:
        """Analyze all project dependencies"""
        dependencies = {}
        
        # Python dependencies
        requirements_files = list(self.project_path.glob("**/requirements.txt"))
        for req_file in requirements_files:
            dependencies.update(self._analyze_python_dependencies(req_file))
        
        # Check pyproject.toml
        pyproject = self.project_path / "pyproject.toml"
        if pyproject.exists():
            dependencies.update(self._analyze_pyproject(pyproject))
        
        # Node.js dependencies
        package_files = list(self.project_path.glob("**/package.json"))
        for pkg_file in package_files:
            dependencies.update(self._analyze_node_dependencies(pkg_file))
        
        return dependencies
    
    def _analyze_python_dependencies(self, requirements_file: Path) -> Dict:
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
                            'file': str(requirements_file)
                        }
        except Exception as e:
            print(f"Error analyzing {requirements_file}: {e}")
        
        return dependencies
    
    def _analyze_pyproject(self, pyproject_file: Path) -> Dict:
        """Analyze dependencies from pyproject.toml"""
        dependencies = {}
        
        try:
            import tomli
        except ImportError:
            try:
                import tomllib as tomli
            except ImportError:
                return dependencies
        
        try:
            with open(pyproject_file, 'rb') as f:
                data = tomli.load(f)
            
            # Get dependencies from project section
            if 'project' in data and 'dependencies' in data['project']:
                for dep in data['project']['dependencies']:
                    pkg = dep.split('>=')[0].split('==')[0].split('<')[0].split('>')[0].strip()
                    version = dep.replace(pkg, '').strip()
                    dependencies[pkg] = {
                        'version': version or 'latest',
                        'type': 'python',
                        'file': str(pyproject_file)
                    }
        except Exception as e:
            print(f"Error analyzing pyproject.toml: {e}")
        
        return dependencies
    
    def _analyze_node_dependencies(self, package_file: Path) -> Dict:
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
                            'file': str(package_file)
                        }
        except Exception as e:
            print(f"Error analyzing {package_file}: {e}")
        
        return dependencies


class GitHistoryAnalyzer:
    """Analyze Git history for file churn and activity"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.has_git = HAS_GIT and (project_path / '.git').exists()
    
    def analyze_history(self, max_commits: int = 100) -> Dict:
        """Analyze git history"""
        if not self.has_git:
            return {}
        
        try:
            repo = Repo(self.project_path)
            
            file_churn = defaultdict(lambda: {'commits': 0, 'additions': 0, 'deletions': 0})
            file_ages = {}
            authors = set()
            
            commits = list(repo.iter_commits('HEAD', max_count=max_commits))
            
            for commit in commits:
                authors.add(commit.author.name)
                for item in commit.stats.files:
                    file_churn[item]['commits'] += 1
                    file_churn[item]['additions'] += commit.stats.files[item]['insertions']
                    file_churn[item]['deletions'] += commit.stats.files[item]['deletions']
                    
                    if item not in file_ages:
                        file_ages[item] = commit.committed_datetime
            
            return {
                'file_churn': dict(file_churn),
                'file_ages': file_ages,
                'total_commits': len(commits),
                'total_authors': len(authors),
                'authors': list(authors)
            }
        except Exception as e:
            print(f"Git analysis failed: {e}")
            return {}


class CallGraphBuilder:
    """Build static call graph from code"""
    
    def __init__(self):
        self.call_graph = {}
        if HAS_NETWORKX:
            self.graph = nx.DiGraph()
        else:
            self.graph = None
    
    def analyze_python_calls(self, content: str, file_path: str):
        """Extract Python function calls and definitions"""
        try:
            tree = ast.parse(content)
            
            functions = []
            calls = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        calls.append(node.func.id)
            
            self.call_graph[file_path] = {
                'functions': functions,
                'calls': calls
            }
            
            if self.graph is not None:
                for func in functions:
                    self.graph.add_node(f"{file_path}::{func}")
                for call in calls:
                    if call in functions:
                        self.graph.add_edge(f"{file_path}::caller", f"{file_path}::{call}")
        
        except:
            pass
    
    def get_complexity_metrics(self) -> Dict:
        """Get call graph complexity metrics"""
        if self.graph is None or len(self.graph.nodes) == 0:
            return {}
        
        try:
            return {
                'total_nodes': len(self.graph.nodes),
                'total_edges': len(self.graph.edges),
                'density': nx.density(self.graph),
                'is_connected': nx.is_weakly_connected(self.graph)
            }
        except:
            return {}


class ProjectAnalyzer:
    """Main project analyzer orchestrating all analysis types"""
    
    LANGUAGE_EXTENSIONS = {
        '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
        '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.h': 'C/C++ Header',
        '.cs': 'C#', '.go': 'Go', '.rs': 'Rust', '.rb': 'Ruby',
        '.php': 'PHP', '.swift': 'Swift', '.kt': 'Kotlin',
        '.jsx': 'React', '.tsx': 'TypeScript React', '.vue': 'Vue',
        '.html': 'HTML', '.css': 'CSS', '.json': 'JSON',
        '.yaml': 'YAML', '.yml': 'YAML', '.md': 'Markdown'
    }
    
    EXCLUDED_DIRS = {'.git', '__pycache__', 'node_modules', 'venv', '.env', 
                     'dist', 'build', '.pytest_cache', '.vscode', '.idea'}
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.metrics_analyzer = CodeMetricsAnalyzer()
        self.dependency_analyzer = DependencyAnalyzer(self.project_path)
        self.git_analyzer = GitHistoryAnalyzer(self.project_path)
        self.call_graph = CallGraphBuilder()
    
    def analyze_file(self, file_path: Path) -> Optional[Dict]:
        """Analyze a single file"""
        ext = file_path.suffix.lower()
        language = self.LANGUAGE_EXTENSIONS.get(ext, 'Unknown')
        
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
            
            # Get code metrics
            code_metrics = {}
            if language == 'Python' and content:
                code_metrics = self.metrics_analyzer.analyze_python_file(content)
                self.call_graph.analyze_python_calls(content, str(file_path))
            elif language in ['JavaScript', 'TypeScript'] and content:
                code_metrics = self.metrics_analyzer.analyze_javascript_file(content)
            
            return {
                'path': str(file_path.relative_to(self.project_path)),
                'absolute_path': str(file_path),
                'name': file_path.name,
                'extension': ext,
                'language': language,
                'size': size,
                'code_lines': code_lines,
                'comment_lines': comment_lines,
                'blank_lines': blank_lines,
                'total_lines': code_lines + comment_lines + blank_lines,
                'comment_ratio': comment_lines / max(code_lines + comment_lines, 1),
                **code_metrics
            }
        except Exception as e:
            return None
    
    def analyze_project(self) -> Dict:
        """Perform comprehensive project analysis"""
        print(f"Analyzing project: {self.project_path}")
        
        files_data = []
        
        # Walk through project directory
        for root, dirs, files in os.walk(self.project_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.EXCLUDED_DIRS]
            
            for file in files:
                file_path = Path(root) / file
                
                try:
                    file_info = self.analyze_file(file_path)
                    if file_info:
                        files_data.append(file_info)
                except Exception as e:
                    print(f"Error analyzing {file_path}: {e}")
        
        # Calculate metrics
        metrics = self._calculate_metrics(files_data)
        
        # Get dependency analysis
        print("Analyzing dependencies...")
        dependencies = self.dependency_analyzer.analyze_dependencies()
        
        # Get git history
        print("Analyzing git history...")
        git_analysis = self.git_analyzer.analyze_history()
        
        # Get call graph metrics
        print("Analyzing code structure...")
        call_graph_metrics = self.call_graph.get_complexity_metrics()
        
        return {
            'project_path': str(self.project_path),
            'analyzed_at': datetime.datetime.now().isoformat(),
            'files': files_data,
            'metrics': metrics,
            'dependencies': dependencies,
            'git_history': git_analysis,
            'call_graph': call_graph_metrics,
        }
    
    def _calculate_metrics(self, files: List[Dict]) -> Dict:
        """Calculate aggregate metrics"""
        metrics = {
            'total_files': len(files),
            'total_size': sum(f['size'] for f in files),
            'total_lines': sum(f['total_lines'] for f in files),
            'code_lines': sum(f['code_lines'] for f in files),
            'comment_lines': sum(f['comment_lines'] for f in files),
            'blank_lines': sum(f['blank_lines'] for f in files),
        }
        
        # Language distribution
        language_stats = defaultdict(lambda: {'count': 0, 'lines': 0, 'size': 0})
        for f in files:
            lang = f['language']
            language_stats[lang]['count'] += 1
            language_stats[lang]['lines'] += f['code_lines']
            language_stats[lang]['size'] += f['size']
        
        total_code_lines = max(metrics['code_lines'], 1)
        metrics['language_distribution'] = {
            lang: {
                'count': stats['count'],
                'lines': stats['lines'],
                'size': stats['size'],
                'percentage': (stats['lines'] / total_code_lines) * 100
            }
            for lang, stats in language_stats.items()
        }
        
        # Complexity metrics
        total_functions = sum(f.get('functions', 0) for f in files)
        total_classes = sum(f.get('classes', 0) for f in files)
        total_complexity = sum(f.get('complexity_score', 0) for f in files)
        
        metrics.update({
            'total_functions': total_functions,
            'total_classes': total_classes,
            'total_complexity': total_complexity,
            'avg_complexity': total_complexity / max(total_functions, 1)
        })
        
        return metrics
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate a text report from analysis"""
        report = []
        
        report.append("=" * 80)
        report.append("PROJECT ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"Project: {analysis['project_path']}")
        report.append(f"Analyzed: {analysis['analyzed_at']}")
        report.append("")
        
        metrics = analysis['metrics']
        
        report.append("FILE & DIRECTORY STRUCTURE")
        report.append("-" * 40)
        report.append(f"Total Files: {metrics['total_files']:,}")
        report.append(f"Total Size: {metrics['total_size']:,} bytes")
        report.append("")
        
        report.append("CODE METRICS")
        report.append("-" * 40)
        report.append(f"Total Lines: {metrics['total_lines']:,}")
        report.append(f"Code Lines: {metrics['code_lines']:,}")
        report.append(f"Comment Lines: {metrics['comment_lines']:,}")
        report.append(f"Blank Lines: {metrics['blank_lines']:,}")
        report.append(f"Comment Ratio: {(metrics['comment_lines'] / max(metrics['code_lines'], 1) * 100):.1f}%")
        report.append("")
        
        report.append("CODE STRUCTURE")
        report.append("-" * 40)
        report.append(f"Total Functions: {metrics.get('total_functions', 0):,}")
        report.append(f"Total Classes: {metrics.get('total_classes', 0):,}")
        report.append(f"Average Complexity: {metrics.get('avg_complexity', 0):.2f}")
        report.append("")
        
        report.append("PROGRAMMING LANGUAGES")
        report.append("-" * 40)
        for lang, stats in sorted(metrics['language_distribution'].items(), 
                                   key=lambda x: x[1]['percentage'], reverse=True)[:10]:
            report.append(f"{lang:20} {stats['percentage']:5.1f}% ({stats['count']:3} files, {stats['lines']:6,} lines)")
        report.append("")
        
        # Dependencies
        if analysis['dependencies']:
            report.append("DEPENDENCIES")
            report.append("-" * 40)
            py_deps = [d for d in analysis['dependencies'].values() if d['type'] == 'python']
            js_deps = [d for d in analysis['dependencies'].values() if d['type'] == 'nodejs']
            report.append(f"Python Packages: {len(py_deps)}")
            report.append(f"Node.js Packages: {len(js_deps)}")
            report.append("")
        
        # Git history
        git = analysis.get('git_history', {})
        if git:
            report.append("VERSION CONTROL")
            report.append("-" * 40)
            report.append(f"Total Commits Analyzed: {git.get('total_commits', 0)}")
            report.append(f"Contributors: {git.get('total_authors', 0)}")
            
            if git.get('file_churn'):
                most_changed = sorted(git['file_churn'].items(), 
                                    key=lambda x: x[1]['commits'], reverse=True)[:5]
                report.append("\nMost Modified Files:")
                for file_path, stats in most_changed:
                    report.append(f"  {Path(file_path).name}: {stats['commits']} commits")
            report.append("")
        
        # Call graph
        cg = analysis.get('call_graph', {})
        if cg:
            report.append("ARCHITECTURAL METRICS")
            report.append("-" * 40)
            report.append(f"Function Nodes: {cg.get('total_nodes', 0)}")
            report.append(f"Call Relationships: {cg.get('total_edges', 0)}")
            if 'density' in cg:
                report.append(f"Graph Density: {cg['density']:.4f}")
            report.append("")
        
        return '\n'.join(report)
    
    def generate_advanced_report(self, analysis: Dict) -> Dict:
        """Generate advanced analysis report with risk analysis and insights"""
        metrics = analysis['metrics']
        files = analysis['files']
        git = analysis.get('git_history', {})
        
        advanced_report = {
            'code_churn': {},
            'stability_analysis': {},
            'high_risk_files': []
        }
        
        # Code Churn & Stability
        if git and git.get('file_churn'):
            churn = git['file_churn']
            sorted_churn = sorted(churn.items(), key=lambda x: x[1]['commits'], reverse=True)[:10]
            
            advanced_report['code_churn'] = {
                'most_modified_files': [
                    {
                        'file': str(Path(file_path).name),
                        'full_path': file_path,
                        'commits': stats['commits'],
                        'additions': stats.get('additions', 0),
                        'deletions': stats.get('deletions', 0)
                    }
                    for file_path, stats in sorted_churn
                ]
            }
        
        # Calculate file risks
        file_risks = []
        for f in files:
            risk_score = self._calculate_file_risk(f, git)
            if risk_score > 0.3:  # Only include files with notable risk
                file_risks.append({
                    'file': f.get('path', ''),
                    'risk_score': risk_score,
                    'complexity': f.get('complexity_score', 0),
                    'lines': f.get('total_lines', 0),
                    'comment_ratio': f.get('comment_ratio', 0)
                })
        
        file_risks.sort(key=lambda x: x['risk_score'], reverse=True)
        advanced_report['high_risk_files'] = file_risks
        
        # Stability analysis
        stable_count, volatile_count = self._analyze_stability(files, git)
        advanced_report['stability_analysis'] = {
            'stable_files': stable_count,
            'volatile_files': volatile_count,
            'total_files': len(files),
            'stability_ratio': stable_count / len(files) if files else 0
        }
        
        return advanced_report
    
    def generate_nextgen_report(self, analysis: Dict) -> Dict:
        """Generate next-generation analysis with predictive insights"""
        files = analysis['files']
        metrics = analysis['metrics']
        git = analysis.get('git_history', {})
        call_graph = analysis.get('call_graph', {})
        dependencies = analysis.get('dependencies', {})
        
        nextgen_report = {}
        
        # Predictive Risk Analysis
        file_risks = []
        for f in files:
            risk_score = self._calculate_file_risk(f, git)
            file_risks.append((f['path'], risk_score))
        
        file_risks.sort(key=lambda x: x[1], reverse=True)
        top_risks = file_risks[:10]
        avg_risk = sum(r for _, r in file_risks) / len(file_risks) if file_risks else 0
        
        nextgen_report['predictive_risk_analysis'] = {
            'top_risk_files': [{'file': path, 'risk_score': risk} for path, risk in top_risks],
            'average_project_risk': avg_risk,
            'high_risk_count': sum(1 for _, r in file_risks if r > 0.5)
        }
        
        # Architectural Analysis
        total_funcs = metrics.get('total_functions', 0)
        complex_modules = []
        for f in files:
            funcs = f.get('functions', []) if isinstance(f.get('functions'), list) else []
            for func in funcs:
                if isinstance(func, dict) and func.get('complexity', 0) > 10:
                    complex_modules.append({
                        'file': f.get('path', ''),
                        'function': func.get('name', ''),
                        'complexity': func.get('complexity', 0)
                    })
        
        complex_modules.sort(key=lambda x: x['complexity'], reverse=True)
        
        nextgen_report['architectural_analysis'] = {
            'call_graph_nodes': call_graph.get('total_nodes', 0),
            'call_graph_edges': call_graph.get('total_edges', 0),
            'architecture_density': call_graph.get('density', 0),
            'high_complexity_modules': complex_modules[:15],
            'total_functions': total_funcs
        }
        
        # Dependency Ecosystem
        py_deps = [d for d in dependencies.values() if d.get('type') == 'python']
        js_deps = [d for d in dependencies.values() if d.get('type') == 'nodejs']
        
        nextgen_report['dependency_ecosystem'] = {
            'total_dependencies': len(dependencies),
            'python_dependencies': len(py_deps),
            'javascript_dependencies': len(js_deps),
            'dependency_breakdown': {
                'python': len(py_deps),
                'nodejs': len(js_deps),
                'other': len(dependencies) - len(py_deps) - len(js_deps)
            }
        }
        
        # AI-Augmented Insights
        nextgen_report['ai_insights'] = {
            'files_with_summaries': 0,
            'semantic_patterns': [],
            'suggested_refactorings': []
        }
        
        # Code Evolution DNA
        stable_count, volatile_count = self._analyze_stability(files, git)
        total_files = len(files)
        stability_ratio = stable_count / total_files if total_files > 0 else 0
        
        nextgen_report['code_evolution_dna'] = {
            'stable_files': stable_count,
            'volatile_files': volatile_count,
            'total_files': total_files,
            'stability_ratio': stability_ratio,
            'current_coverage_estimate': metrics.get('comment_ratio', 0)
        }
        
        # Recommendations
        recommendations = self._generate_recommendations(file_risks, metrics, dependencies, call_graph)
        
        nextgen_report['recommendations'] = {
            'high_priority': recommendations[:3],
            'medium_priority': recommendations[3:6] if len(recommendations) > 3 else [],
            'all_recommendations': recommendations
        }
        
        return nextgen_report
    
    def _calculate_file_risk(self, file_info: Dict, git_history: Dict) -> float:
        """Calculate risk score for a file (0.0 to 1.0)"""
        risk = 0.0
        
        # Complexity risk
        complexity = file_info.get('complexity_score', 0)
        if complexity > 50:
            risk += 0.3
        elif complexity > 20:
            risk += 0.15
        
        # Low comment ratio risk
        comment_ratio = file_info.get('comment_ratio', 0)
        if comment_ratio < 0.1:
            risk += 0.2
        
        # Git churn risk
        if git_history and git_history.get('file_churn'):
            file_path = file_info.get('absolute_path', file_info.get('path', ''))
            churn = git_history['file_churn'].get(file_path, {})
            commits = churn.get('commits', 0)
            if commits > 10:
                risk += 0.2
            elif commits > 5:
                risk += 0.1
        
        # Large file risk
        lines = file_info.get('total_lines', 0)
        if lines > 1000:
            risk += 0.2
        elif lines > 500:
            risk += 0.1
        
        return min(risk, 1.0)  # Cap at 1.0
    
    def _analyze_stability(self, files: List[Dict], git_history: Dict) -> Tuple[int, int]:
        """Analyze file stability based on git history"""
        stable_count = 0
        volatile_count = 0
        
        if not git_history or not git_history.get('file_churn'):
            # If no git history, consider all files stable
            return len(files), 0
        
        file_churn = git_history['file_churn']
        
        for f in files:
            file_path = f.get('absolute_path', f.get('path', ''))
            churn = file_churn.get(file_path, {})
            commits = churn.get('commits', 0)
            
            if commits < 2:  # Less than 2 commits = stable
                stable_count += 1
            elif commits > 10:  # More than 10 commits = volatile
                volatile_count += 1
            else:
                stable_count += 1  # Default to stable
        
        return stable_count, volatile_count
    
    def _generate_recommendations(self, file_risks: List[Tuple[str, float]], 
                                 metrics: Dict, dependencies: Dict, 
                                 call_graph: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Risk-based recommendations
        high_risk_files = [f for f, r in file_risks if r > 0.5]
        if len(high_risk_files) > 5:
            recommendations.append(f"Found {len(high_risk_files)} high-risk files. Prioritize refactoring and testing.")
        
        # Complexity recommendations
        avg_complexity = metrics.get('avg_complexity', 0)
        if avg_complexity > 10:
            recommendations.append(f"High average complexity ({avg_complexity:.1f}). Consider breaking down complex functions.")
        
        # Comment ratio recommendations
        comment_ratio = metrics.get('comment_lines', 0) / max(metrics.get('code_lines', 1), 1)
        if comment_ratio < 0.1:
            recommendations.append(f"Low documentation ({comment_ratio*100:.1f}% comments). Improve code documentation.")
        
        # Architecture recommendations
        density = call_graph.get('density', 0)
        if density > 0.1:
            recommendations.append("High architectural density detected. Consider modularization to reduce coupling.")
        
        # Dependency recommendations
        if len(dependencies) > 50:
            recommendations.append(f"Large number of dependencies ({len(dependencies)}). Review and remove unused packages.")
        
        if not recommendations:
            recommendations.append("Code health looks good! Keep up the good practices.")
        
        return recommendations
        
        return '\n'.join(report)

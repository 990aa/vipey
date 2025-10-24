# Project Analyzer 🚀

A comprehensive, AI-powered codebase intelligence platform that analyzes project directories and provides deep insights into code quality, architecture, risk, and maintainability.

## 🌟 Features

### 📊 Basic Analytics
- **File & Directory Structure**: Counts, depth, distribution, sizes
- **Size & Storage Metrics**: Total size, code vs text, compression ratios
- **Code Content Analysis**: Lines of code, comments, blanks, ratios
- **Language Detection**: 25+ programming languages with percentages
- **Quality Metrics**: Complexity, duplication, dependency analysis

### 🔍 Advanced Analytics
- **Code Churn & Stability**: Git-based change frequency analysis
- **Cognitive Complexity**: Human-understandability scoring
- **Architecture Violations**: Layer breaches, circular dependencies
- **Team Knowledge**: Bus factor, ownership distribution
- **Dead Code Detection**: Unused functions, orphaned files

### 🧠 Next-Generation Intelligence
- **Predictive Risk Modeling**: ML-based bug prediction
- **Dynamic Call Graphs**: Impact analysis, hot path identification
- **AI-Augmented Understanding**: Documentation quality, intent mismatch detection
- **Ecosystem Intelligence**: Dependency reachability, vulnerability analysis
- **Real-Time Dashboard**: Live metrics and WebSocket updates
- **Code Evolution DNA**: Lineage tracking, refactoring detection

## 🛠 Installation

### Prerequisites
- Python 3.8+
- Git (for historical analysis)

### Quick Start
```bash
# Clone or download project-analyzer.py
# Install dependencies
pip install -r requirements.txt

# Run basic analysis
python project-analyzer.py /path/to/your/project
```

### Full Requirements
Create `requirements.txt`:
```txt
# Core analysis
pathlib>=1.0.1
humanize>=4.6.0
gitpython>=3.1.40
pydriller>=2.1
networkx>=3.1
matplotlib>=3.7.0
seaborn>=0.12.2
numpy>=1.24.0
scipy>=1.10.0
scikit-learn>=1.3.0

# Code analysis
radon>=5.1.0
vulture>=2.7
bandit>=1.7.5
lizard>=1.17.10
javalang>=0.13.0
tree-sitter>=0.20.1
tree-sitter-python>=0.20.0
tree-sitter-javascript>=0.20.0
tree-sitter-java>=0.20.0
tree-sitter-go>=0.19.0
tree-sitter-rust>=0.20.0

# Dependency analysis
pipdeptree>=2.7.1
safety>=2.3.5
packageurl-python>=0.11.1

# AI/ML capabilities
openai>=1.3.0
transformers>=4.35.0
torch>=2.0.0
sentence-transformers>=2.2.2
nltk>=3.8.1
textstat>=0.7.3

# Visualization & APIs
plotly>=5.15.0
fastapi>=0.104.0
uvicorn>=0.24.0
websockets>=12.0
aiofiles>=23.2.0

# Security & crypto
pycryptodome>=3.18.0
cryptography>=41.0.0

# Utilities
pydantic>=2.4.0
pandas>=2.0.0
tqdm>=4.65.0
python-dotenv>=1.0.0
click>=8.1.0
rich>=13.0.0
```

## 🚀 Usage Examples

### Basic Analysis
```bash
# Quick project overview
python project-analyzer.py /path/to/project

# Analyze current directory
python project-analyzer.py .

# Save report to specific file
python project-analyzer.py /path/to/project > analysis_report.txt
```

### Advanced Git Analysis
```bash
# Full analysis with Git history (requires git repository)
python project-analyzer.py /path/to/git/project

# Limit Git history depth for performance
python project-analyzer.py /path/to/project --git-depth 100
```

### Real-Time Dashboard
```bash
# Start interactive dashboard on port 8000
python project-analyzer.py /path/to/project --dashboard

# Custom port
python project-analyzer.py /path/to/project --dashboard --port 8080

# Access dashboard at http://localhost:8000
```

### Risk-Focused Analysis
```bash
# Focus on predictive risk metrics
python project-analyzer.py /path/to/project --risk-only

# Generate risk visualization
python project-analyzer.py /path/to/project --visualize-risk
```

### Architecture Analysis
```bash
# Deep architecture and dependency analysis
python project-analyzer.py /path/to/project --architecture

# Export dependency graph
python project-analyzer.py /path/to/project --export-graph
```

### AI-Powered Insights
```bash
# Enable AI code understanding (requires OpenAI API key)
python project-analyzer.py /path/to/project --ai-analysis

# Set custom AI model
python project-analyzer.py /path/to/project --ai-model gpt-4
```

## 📋 Output Examples

### Basic Metrics Section
```
📁 FILE & DIRECTORY STRUCTURE
----------------------------------------
Total Files: 1,234
Total Directories: 89
Maximum Directory Depth: 7
Average Files per Directory: 13.9

💾 SIZE & STORAGE METRICS
----------------------------------------
Total Size: 45.2 MB
Code Files Size: 32.1 MB
Text Files Size: 2.3 MB

🔤 PROGRAMMING LANGUAGES
----------------------------------------
Python         45.2% ( 70 files, 30456 lines)
JavaScript     32.1% ( 50 files, 21678 lines)
HTML           12.3% ( 19 files,  8912 lines)
```

### Advanced Analytics Section
```
🔍 CODE CHURN & STABILITY ANALYSIS
----------------------------------------
High Churn Files (most frequently modified):
  src/auth/service.py: 23 commits
  src/api/endpoints.py: 18 commits

🧠 COGNITIVE COMPLEXITY HOTSPOTS
----------------------------------------
src/utils/helpers.py: complexity score 47
src/core/processing.py: complexity score 38
```

### Next-Generation Intelligence
```
🧠 PREDICTIVE RISK ANALYSIS
----------------------------------------
Top 5 High-Risk Files:
  src/auth/service.py: 87% risk
  src/database/migrations.py: 76% risk
Average Project Risk: 34.2%

🕸️ ARCHITECTURAL ANALYSIS
----------------------------------------
Call Graph Size: 245 functions, 1892 calls
Potential Bottlenecks: 3 functions
```

## 🎯 Use Cases

### For Development Teams
```bash
# Monitor codebase health
python project-analyzer.py . --dashboard

# Identify technical debt hotspots
python project-analyzer.py . --risk-only

# Onboarding new developers
python project-analyzer.py . --architecture --ai-analysis
```

### For Project Managers
```bash
# Track project metrics over time
python project-analyzer.py . --basic --export-json

# Assess maintenance burden
python project-analyzer.py . --advanced --focus-maintainability
```

### For Security Teams
```bash
# Security-focused analysis
python project-analyzer.py . --security --dependency-check

# Compliance auditing
python project-analyzer.py . --license-check --export-report
```

### For Open Source Maintainers
```bash
# Community health assessment
python project-analyzer.py . --git-analysis --team-metrics

# Contribution guidance
python project-analyzer.py . --onboarding-path --beginner-issues
```

## ⚙️ Configuration

### Environment Variables
```bash
# OpenAI API for AI features (optional)
export OPENAI_API_KEY="your-api-key"

# Custom analysis thresholds
export RISK_THRESHOLD="0.7"
export COMPLEXITY_THRESHOLD="50"

# Dashboard configuration
export DASHBOARD_PORT="8000"
export DASHBOARD_HOST="localhost"
```

### Configuration File
Create `.project-analyzer.json`:
```json
{
  "exclude_patterns": ["*_test.py", "temp/", "build/"],
  "risk_model": "conservative",
  "ai_enabled": true,
  "dashboard": {
    "port": 8080,
    "refresh_interval": 30
  },
  "languages": {
    "priority": ["python", "javascript", "typescript"],
    "ignore": ["json", "yaml"]
  }
}
```

## 📈 Output Formats

### Text Report (Default)
```bash
python project-analyzer.py /path/to/project
```

### JSON Export
```bash
python project-analyzer.py /path/to/project --json > analysis.json
```

### HTML Dashboard
```bash
python project-analyzer.py /path/to/project --html --output report.html
```

### CSV Metrics
```bash
python project-analyzer.py /path/to/project --csv --output metrics.csv
```

## 🚨 Performance Tips

### For Large Codebases
```bash
# Limit analysis depth
python project-analyzer.py /path/to/large-project --max-depth 3

# Exclude non-essential directories
python project-analyzer.py /path/to/project --exclude "node_modules,dist,build"

# Sample analysis (random file sampling)
python project-analyzer.py /path/to/project --sample 0.1  # 10% of files
```

### Memory Optimization
```bash
# Disable memory-intensive features
python project-analyzer.py /path/to/project --no-call-graph --no-ai

# Stream processing for very large projects
python project-analyzer.py /path/to/project --streaming
```

## 🔧 Troubleshooting

### Common Issues

**Git History Not Available**
```bash
# Run without Git analysis
python project-analyzer.py /path/to/project --no-git
```

**Memory Errors**
```bash
# Reduce memory usage
python project-analyzer.py /path/to/project --lightweight
```

**AI Features Not Working**
```bash
# Disable AI or use local models
python project-analyzer.py /path/to/project --no-ai
# or
python project-analyzer.py /path/to/project --local-ai
```

### Debug Mode
```bash
# Enable verbose logging
python project-analyzer.py /path/to/project --debug

# Profile performance
python project-analyzer.py /path/to/project --profile
```

## 📊 Sample Integration

### CI/CD Pipeline
```yaml
# GitHub Actions example
- name: Codebase Analysis
  run: |
    python project-analyzer.py . --json > analysis.json
    python project-analyzer.py . --risk-only --fail-on-risk 0.8
```

### Pre-commit Hook
```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: project-analysis
      name: Analyze Codebase Changes
      entry: python project-analyzer.py
      args: [".", "--changed-files", "--fail-on-risk", "0.9"]
      language: system
```

## 🤝 Contributing

This analyzer is designed to be extensible. Key extension points:

1. **New Language Support**: Add to `language_extensions` mapping
2. **Custom Metrics**: Implement new analyzer classes
3. **Export Formats**: Add new output formatters
4. **Integration Plugins**: Connect to other tools and APIs

## 📄 License

This project is open source. See LICENSE file for details.

## 🆘 Support

- **Documentation**: Run `python project-analyzer.py --help`
- **Issues**: Check the --debug output for troubleshooting
- **Features**: Use command-line flags to enable/disable specific analyses

---

**Ready to analyze your codebase?** 🎉

```bash
# Get started with a basic analysis
python project-analyzer.py /path/to/your/project

# Or launch the interactive dashboard
python project-analyzer.py /path/to/your/project --dashboard
```

The analyzer will automatically detect your project type, apply appropriate analysis techniques, and deliver comprehensive insights about your codebase health and structure!
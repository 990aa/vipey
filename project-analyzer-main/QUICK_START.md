# Quick Start Guide - Project Analyzer Dashboard

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
# Navigate to project directory
cd project-analyzer

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install required packages (already done)
pip install -r requirements.txt
```

### Step 2: Launch Dashboard
```bash
# Run with default settings (port 5000)
python project-analyzer.py <your-project-path> --dashboard

# Or specify custom port
python project-analyzer.py <your-project-path> --dashboard --port 8080
```

### Step 3: Analyze Your Code
1. Browser opens automatically to http://127.0.0.1:5000
2. Click the **"🔍 Run Analysis"** button
3. Wait for analysis to complete (~5-10 seconds)
4. Explore interactive charts and metrics!

---

## 📊 Dashboard Features

### Main Sections

#### 1. **Status Bar** (Top)
- **Total Files**: Number of files analyzed
- **Lines of Code**: Total code lines
- **Risk Score**: Overall project risk (0-100%)
- **Languages**: Number of programming languages detected

#### 2. **Project Metrics Card**
- Code Lines
- Comment Lines
- Total Size (in KB/MB)
- Average Complexity

#### 3. **Language Distribution Card**
- Top 8 languages used
- Percentage breakdown
- Visual progress bars

#### 4. **Predictive Risk Analysis Card**
- Average risk score
- Number of high-risk files
- Top 5 risky files with badges:
  - 🔴 Critical (>80%)
  - 🟠 High (60-80%)
  - 🟡 Medium (40-60%)
  - 🟢 Low (<40%)

#### 5. **Architecture Metrics Card**
- Total functions detected
- Function calls mapped
- Architecture density
- Bottlenecks identified

#### 6. **Interactive Charts**
- **Language Distribution Pie Chart**: Visual language breakdown
- **High-Risk Files Bar Chart**: Top 10 files by risk score
- **Code Metrics Bar Chart**: Key statistics visualization

---

## 🎯 Use Cases & Examples

### Example 1: Analyze Any Project
```bash
# Analyze a Python project
python project-analyzer.py C:\Projects\my-python-app --dashboard

# Analyze a JavaScript project
python project-analyzer.py C:\Projects\my-react-app --dashboard

# Analyze a mixed codebase
python project-analyzer.py C:\Projects\full-stack-app --dashboard
```

### Example 2: Generate Report Only (No Dashboard)
```bash
# Just generate text report
python project-analyzer.py <project-path>

# Report saved to: nextgen_analysis_YYYYMMDD_HHMMSS.txt
```

### Example 3: Multiple Analyses
```bash
# Analyze test project
python project-analyzer.py test_project --dashboard --port 5000

# In another terminal, analyze another project
python project-analyzer.py another_project --dashboard --port 5001
```

---

## 🎨 Dashboard Actions

### Button Controls

1. **🔍 Run Analysis**
   - Starts code analysis
   - Shows loading spinner
   - Populates all metrics and charts
   - Enables other buttons

2. **📄 Show/Hide Full Report**
   - Toggles detailed text report
   - Shows complete analysis in monospace font
   - Easy to read format

3. **💾 Download Report**
   - Downloads analysis as .txt file
   - Filename: `codebase_analysis_YYYY-MM-DD.txt`
   - Contains full report content

---

## 📈 Understanding the Results

### Risk Levels Explained
- **0-20% (Very Low)**: Well-maintained, low complexity
- **20-40% (Low)**: Good code quality, minor issues
- **40-60% (Medium)**: Needs attention, refactoring recommended
- **60-80% (High)**: Significant issues, high priority
- **80-100% (Critical)**: Urgent attention required

### Architecture Density
- **< 0.05**: Loosely coupled (Good!)
- **0.05-0.15**: Moderate coupling
- **> 0.15**: Tightly coupled (Consider refactoring)

### Code Stability
- **> 90%**: Very stable codebase
- **70-90%**: Moderately stable
- **< 70%**: High churn, potential issues

---

## 🔧 Troubleshooting

### Dashboard Won't Start
```bash
# Check if port is in use
netstat -ano | findstr :5000

# Try different port
python project-analyzer.py <path> --dashboard --port 5001
```

### Analysis Fails
```bash
# Check if path is correct
ls <your-project-path>

# Ensure git repository exists (optional)
cd <your-project-path>
git status
```

### Charts Not Showing
- Wait for analysis to complete
- Check browser console (F12) for errors
- Refresh page (F5)
- Clear browser cache

---

## 💡 Tips & Tricks

### 1. **Compare Projects**
Analyze multiple projects and compare metrics side-by-side

### 2. **Track Progress**
Run analysis before and after refactoring to see improvements

### 3. **Team Reviews**
Share dashboard URL during code reviews

### 4. **CI/CD Integration**
Generate reports automatically in your build pipeline

### 5. **Large Projects**
For very large codebases (>100k lines), analysis may take 30-60 seconds

---

## 📋 Supported Languages

✅ **Fully Supported:**
- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- Java (.java)
- C/C++ (.c, .cpp, .h)
- C# (.cs)
- Go (.go)
- Rust (.rs)
- Ruby (.rb)
- PHP (.php)

✅ **Detected:**
- HTML, CSS
- JSON, XML, YAML
- SQL, Shell scripts
- React (.jsx, .tsx)
- Vue (.vue)
- And more...

---

## 🎓 Advanced Features

### Real-Time Updates
- Dashboard supports WebSocket connections
- Metrics update automatically
- No need to refresh browser

### Dependency Analysis
- Detects Python packages (requirements.txt)
- Detects Node.js packages (package.json)
- Identifies unused dependencies

### Git Integration
- Analyzes commit history
- Identifies frequently changed files
- Calculates code stability metrics

---

## 🏆 Best Practices

1. **Regular Analysis**: Run weekly to track code health
2. **Before Releases**: Verify risk levels before deploying
3. **After Refactoring**: Confirm improvements with metrics
4. **Team Meetings**: Use dashboard for technical discussions
5. **Documentation**: Export reports for project documentation

---

## 📞 Need Help?

- Check `TEST_RESULTS_SUMMARY.md` for detailed verification
- Review `README.md` for full documentation
- Examine `test_project/` for usage examples

---

**Happy Analyzing! 🎉**

Your code health is just one command away!

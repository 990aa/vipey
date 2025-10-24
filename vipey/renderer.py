# renderer.py
import json
import os
import re
from pathlib import Path
import webbrowser
import threading
import time

try:
    import markdown
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

try:
    from flask import Flask, render_template_string
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False


def save_visualization(storyboard_data: dict, output_path: str):
    """Save visualization as a self-contained HTML file."""
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    template_path = os.path.join(template_dir, 'index.html')
    
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find and inline CSS files
    css_pattern = r'<link rel="stylesheet" href="(/assets/[^"]+)">'
    css_matches = re.findall(css_pattern, html_content)
    
    for css_path in css_matches:
        css_file = os.path.join(template_dir, css_path.lstrip('/'))
        if os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
            # Replace link tag with inline style
            html_content = html_content.replace(
                f'<link rel="stylesheet" href="{css_path}">',
                f'<style>{css_content}</style>'
            )
    
    # Find and inline JS files
    js_pattern = r'<script type="module" crossorigin src="(/assets/[^"]+)"></script>'
    js_matches = re.findall(js_pattern, html_content)
    
    for js_path in js_matches:
        js_file = os.path.join(template_dir, js_path.lstrip('/'))
        if os.path.exists(js_file):
            with open(js_file, 'r', encoding='utf-8') as f:
                js_content = f.read()
            # Replace script tag with inline script
            html_content = html_content.replace(
                f'<script type="module" crossorigin src="{js_path}"></script>',
                f'<script type="module">{js_content}</script>'
            )
    
    # Inject the storyboard data
    json_data = json.dumps(storyboard_data, indent=2)
    final_html = html_content.replace('%%VIPEY_STORYBOARD_DATA%%', json_data)
    
    # Write the final HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Visualization saved to: {output_path}")


def save_multi_tab_visualization(storyboard_data: dict = None, 
                                 project_data: dict = None,
                                 file_data: dict = None,
                                 output_path: str = "visualization.html",
                                 interactive: bool = False):
    """
    Save multi-tab visualization with function trace, project analysis, and documentation.
    
    Args:
        storyboard_data: Function execution trace data
        project_data: Project analysis data
        file_data: Single file analysis data
        output_path: Path to save the HTML file
        interactive: If True, start a local server; if False, create static HTML
    """
    if interactive and HAS_FLASK:
        # Start interactive server
        _start_interactive_server(storyboard_data, project_data, file_data)
    else:
        # Create static HTML file
        _create_static_multi_tab_html(storyboard_data, project_data, file_data, output_path)


def _create_static_multi_tab_html(storyboard_data, project_data, file_data, output_path):
    """Create a static multi-tab HTML visualization"""
    
    # Read documentation
    doc_path = Path(__file__).parent.parent / "DOCUMENTATION.md"
    documentation_html = ""
    if doc_path.exists():
        with open(doc_path, 'r', encoding='utf-8') as f:
            doc_content = f.read()
        if HAS_MARKDOWN:
            documentation_html = markdown.markdown(doc_content, extensions=['fenced_code', 'tables', 'toc'])
        else:
            # Fallback to plain text in pre tag
            documentation_html = f"<pre>{doc_content}</pre>"
    else:
        documentation_html = "<p>Documentation not found.</p>"
    
    # Generate project analysis HTML
    project_html = _generate_project_analysis_html(project_data, file_data)
    
    # Build the multi-tab HTML
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vipey - Code Analysis & Visualization</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #0d1117;
            color: #c9d1d9;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: #161b22;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            border: 1px solid #30363d;
        }
        
        h1 {
            color: #58a6ff;
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #30363d;
        }
        
        .tab {
            padding: 12px 24px;
            background: #161b22;
            border: 1px solid #30363d;
            border-bottom: none;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            color: #8b949e;
            transition: all 0.3s;
        }
        
        .tab:hover {
            background: #1c2128;
            color: #c9d1d9;
        }
        
        .tab.active {
            background: #0d1117;
            color: #58a6ff;
            border-color: #58a6ff;
        }
        
        .tab-content {
            display: none;
            background: #161b22;
            padding: 30px;
            border-radius: 8px;
            border: 1px solid #30363d;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .metric-card {
            background: #0d1117;
            padding: 20px;
            margin: 15px 0;
            border-radius: 6px;
            border: 1px solid #30363d;
        }
        
        .metric-card h3 {
            color: #58a6ff;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .metric-item {
            background: #0d1117;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #30363d;
        }
        
        .metric-label {
            color: #8b949e;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        
        .metric-value {
            color: #58a6ff;
            font-size: 1.8em;
            font-weight: bold;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #30363d;
        }
        
        th {
            background: #0d1117;
            color: #58a6ff;
            font-weight: 600;
        }
        
        tr:hover {
            background: #1c2128;
        }
        
        code {
            background: #0d1117;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
            color: #79c0ff;
        }
        
        pre {
            background: #0d1117;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
            border: 1px solid #30363d;
        }
        
        .doc-content {
            max-width: 900px;
        }
        
        .doc-content h2 {
            color: #58a6ff;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 1.8em;
        }
        
        .doc-content h3 {
            color: #79c0ff;
            margin-top: 25px;
            margin-bottom: 12px;
            font-size: 1.4em;
        }
        
        .doc-content p {
            margin: 12px 0;
            line-height: 1.8;
        }
        
        .doc-content ul, .doc-content ol {
            margin: 12px 0 12px 30px;
        }
        
        .doc-content li {
            margin: 8px 0;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 500;
        }
        
        .badge-success {
            background: #238636;
            color: #fff;
        }
        
        .badge-warning {
            background: #9e6a03;
            color: #fff;
        }
        
        .badge-info {
            background: #1f6feb;
            color: #fff;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎯 Vipey - Code Analysis & Visualization</h1>
            <p>Comprehensive code intelligence and execution tracing</p>
        </header>
        
        <div class="tabs">
            {TAB_HEADERS}
        </div>
        
        {TAB_CONTENTS}
    </div>
    
    <script>
        // Tab switching logic
        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName + '-content').classList.add('active');
            document.querySelector('[data-tab="' + tabName + '"]').classList.add('active');
        }
        
        // Initialize - show first available tab
        document.addEventListener('DOMContentLoaded', () => {
            const firstTab = document.querySelector('.tab');
            if (firstTab) {
                firstTab.click();
            }
        });
    </script>
</body>
</html>
"""
    
    # Build tabs
    tab_headers = []
    tab_contents = []
    
    if storyboard_data:
        tab_headers.append('<div class="tab" data-tab="trace" onclick="switchTab(\'trace\')">Function Trace</div>')
        tab_contents.append(f'''
        <div id="trace-content" class="tab-content">
            <h2>Function Execution Trace</h2>
            <p>Interactive execution trace not available in static mode. Use <code>interactive=True</code> for full trace visualization.</p>
            <div class="metric-card">
                <h3>Execution Summary</h3>
                <p>Total frames captured: {len(storyboard_data.get('frames', []))}</p>
                <p>Return value: <code>{storyboard_data.get('return_value', 'N/A')}</code></p>
            </div>
        </div>
        ''')
    
    if project_data or file_data:
        tab_headers.append('<div class="tab active" data-tab="analysis" onclick="switchTab(\'analysis\')">Project Analysis</div>')
        tab_contents.append(f'<div id="analysis-content" class="tab-content active">{project_html}</div>')
    
    tab_headers.append('<div class="tab" data-tab="docs" onclick="switchTab(\'docs\')">Documentation</div>')
    tab_contents.append(f'<div id="docs-content" class="tab-content"><div class="doc-content">{documentation_html}</div></div>')
    
    final_html = html_template.replace('{TAB_HEADERS}', '\n'.join(tab_headers))
    final_html = final_html.replace('{TAB_CONTENTS}', '\n'.join(tab_contents))
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Multi-tab visualization saved to: {output_path}")


def _generate_project_analysis_html(project_data, file_data):
    """Generate HTML for project analysis tab"""
    if not project_data and not file_data:
        return "<p>No analysis data available.</p>"
    
    data = project_data or {'metrics': {}, 'files': [file_data] if file_data else []}
    metrics = data.get('metrics', {})
    
    html = f"""
    <h2>Project Analysis Results</h2>
    
    <div class="metric-grid">
        <div class="metric-item">
            <div class="metric-label">Total Files</div>
            <div class="metric-value">{metrics.get('total_files', 0):,}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Total Lines</div>
            <div class="metric-value">{metrics.get('total_lines', 0):,}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Code Lines</div>
            <div class="metric-value">{metrics.get('code_lines', 0):,}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Functions</div>
            <div class="metric-value">{metrics.get('total_functions', 0):,}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Classes</div>
            <div class="metric-value">{metrics.get('total_classes', 0):,}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Avg Complexity</div>
            <div class="metric-value">{metrics.get('avg_complexity', 0):.1f}</div>
        </div>
    </div>
    
    <div class="metric-card">
        <h3>Language Distribution</h3>
        <table>
            <thead>
                <tr>
                    <th>Language</th>
                    <th>Files</th>
                    <th>Lines</th>
                    <th>Percentage</th>
                </tr>
            </thead>
            <tbody>
    """
    
    lang_dist = metrics.get('language_distribution', {})
    for lang, stats in sorted(lang_dist.items(), key=lambda x: x[1]['percentage'], reverse=True)[:10]:
        html += f"""
                <tr>
                    <td><span class="badge badge-info">{lang}</span></td>
                    <td>{stats['count']}</td>
                    <td>{stats['lines']:,}</td>
                    <td>{stats['percentage']:.1f}%</td>
                </tr>
        """
    
    html += """
            </tbody>
        </table>
    </div>
    """
    
    # Dependencies
    dependencies = data.get('dependencies', {})
    if dependencies:
        html += """
        <div class="metric-card">
            <h3>Dependencies</h3>
            <table>
                <thead>
                    <tr>
                        <th>Package</th>
                        <th>Version</th>
                        <th>Type</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for pkg, info in list(dependencies.items())[:20]:  # Show first 20
            html += f"""
                    <tr>
                        <td><code>{pkg}</code></td>
                        <td>{info.get('version', 'N/A')}</td>
                        <td><span class="badge badge-success">{info.get('type', 'unknown')}</span></td>
                    </tr>
            """
        
        html += """
                </tbody>
            </table>
        </div>
        """
    
    # Git history
    git = data.get('git_history', {})
    if git and git.get('file_churn'):
        html += """
        <div class="metric-card">
            <h3>Most Modified Files (Git History)</h3>
            <table>
                <thead>
                    <tr>
                        <th>File</th>
                        <th>Commits</th>
                        <th>Additions</th>
                        <th>Deletions</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        most_changed = sorted(git['file_churn'].items(), key=lambda x: x[1]['commits'], reverse=True)[:10]
        for file_path, stats in most_changed:
            html += f"""
                    <tr>
                        <td><code>{Path(file_path).name}</code></td>
                        <td>{stats['commits']}</td>
                        <td><span class="badge badge-success">+{stats['additions']}</span></td>
                        <td><span class="badge badge-warning">-{stats['deletions']}</span></td>
                    </tr>
            """
        
        html += """
                </tbody>
            </table>
        </div>
        """
    
    return html


def _start_interactive_server(storyboard_data, project_data, file_data):
    """Start Flask server for interactive visualization"""
    if not HAS_FLASK:
        print("Flask not available. Install it for interactive mode: pip install flask")
        return
    
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        # TODO: Implement interactive multi-tab interface with real-time updates
        return "<h1>Interactive mode - Under construction</h1>"
    
    def open_browser():
        time.sleep(1.5)
        webbrowser.open('http://127.0.0.1:5000')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    print("\n" + "="*60)
    print("Starting interactive server at: http://127.0.0.1:5000")
    print("="*60 + "\n")
    
    app.run(debug=False, port=5000)

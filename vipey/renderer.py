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
        # Get time complexity if available
        complexity = storyboard_data.get('time_complexity', {})
        complexity_html = ""
        if complexity:
            big_o = complexity.get('big_o', 'Unknown')
            explanation = complexity.get('explanation', '')
            patterns = complexity.get('patterns', [])
            confidence = complexity.get('confidence', 'unknown')
            
            pattern_badges = ' '.join([f'<span class="badge badge-info">{p}</span>' for p in patterns])
            confidence_color = {'high': 'success', 'medium': 'warning', 'low': 'danger'}.get(confidence, 'info')
            
            complexity_html = f'''
            <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; margin-top: 20px;">
                <h3 style="color: white;">⏱️ Time Complexity Analysis</h3>
                <div style="font-size: 2em; font-weight: bold; margin: 15px 0;">{big_o}</div>
                <p style="opacity: 0.9;">{explanation}</p>
                {f'<div style="margin-top: 10px;">Patterns detected: {pattern_badges}</div>' if patterns else ''}
                <div style="margin-top: 10px; opacity: 0.8;">
                    <span class="badge badge-{confidence_color}">Confidence: {confidence}</span>
                </div>
            </div>
            '''
        
        tab_headers.append('<div class="tab" data-tab="trace" onclick="switchTab(\'trace\')">Function Trace</div>')
        tab_contents.append(f'''
        <div id="trace-content" class="tab-content">
            <h2>Function Execution Trace</h2>
            <p>Interactive execution trace not available in static mode. Use <code>interactive=True</code> for full trace visualization.</p>
            {complexity_html}
            <div class="metric-card">
                <h3>Execution Summary</h3>
                <p><strong>Function:</strong> <code>{storyboard_data.get('function_name', 'unknown')}</code></p>
                <p><strong>Total frames captured:</strong> {len(storyboard_data.get('frames', []))}</p>
                <p><strong>Return value:</strong> <code>{storyboard_data.get('return_value', 'N/A')}</code></p>
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


def _generate_plotly_charts(project_data):
    """Generate interactive Plotly charts for project analysis"""
    if not HAS_PLOTLY:
        return {}
    
    charts = {}
    metrics = project_data.get('metrics', {})
    
    # 1. Language Distribution Pie Chart
    lang_dist = metrics.get('language_distribution', {})
    if lang_dist:
        langs = []
        percentages = []
        for lang, stats in sorted(lang_dist.items(), key=lambda x: x[1]['percentage'], reverse=True)[:10]:
            langs.append(lang)
            percentages.append(stats['percentage'])
        
        fig = go.Figure(data=[go.Pie(
            labels=langs,
            values=percentages,
            hole=0.3,
            marker=dict(colors=px.colors.qualitative.Set3)
        )])
        fig.update_layout(
            title="Language Distribution",
            height=400,
            showlegend=True
        )
        charts['language_distribution'] = fig.to_html(include_plotlyjs='cdn', div_id='lang-dist-chart')
    
    # 2. File Risk Scores Bar Chart
    advanced_report = project_data.get('advanced_report', {})
    if advanced_report and 'high_risk_files' in advanced_report:
        risk_files = advanced_report['high_risk_files'][:15]
        if risk_files:
            files = [Path(f['file']).name for f in risk_files]
            scores = [f['risk_score'] for f in risk_files]
            
            fig = go.Figure(data=[go.Bar(
                x=files,
                y=scores,
                marker=dict(
                    color=scores,
                    colorscale='Reds',
                    showscale=True,
                    colorbar=dict(title="Risk Score")
                )
            )])
            fig.update_layout(
                title="Top 15 High-Risk Files",
                xaxis_title="File",
                yaxis_title="Risk Score",
                height=400,
                xaxis_tickangle=-45
            )
            charts['risk_scores'] = fig.to_html(include_plotlyjs='cdn', div_id='risk-chart')
    
    # 3. Complexity Distribution Bar Chart
    nextgen_report = project_data.get('nextgen_report', {})
    if nextgen_report and 'architectural_analysis' in nextgen_report:
        arch = nextgen_report['architectural_analysis']
        if 'high_complexity_modules' in arch:
            modules = arch['high_complexity_modules'][:15]
            if modules:
                mod_names = [Path(m['file']).name for m in modules]
                complexities = [m['complexity'] for m in modules]
                
                fig = go.Figure(data=[go.Bar(
                    x=mod_names,
                    y=complexities,
                    marker=dict(color='indianred')
                )])
                fig.update_layout(
                    title="Top 15 Complex Modules",
                    xaxis_title="Module",
                    yaxis_title="Cyclomatic Complexity",
                    height=400,
                    xaxis_tickangle=-45
                )
                charts['complexity'] = fig.to_html(include_plotlyjs='cdn', div_id='complexity-chart')
    
    # 4. File Churn Over Time (Git History)
    git = project_data.get('git_history', {})
    if git and git.get('file_churn'):
        file_churn = sorted(git['file_churn'].items(), key=lambda x: x[1]['commits'], reverse=True)[:15]
        if file_churn:
            files = [Path(f[0]).name for f in file_churn]
            commits = [f[1]['commits'] for f in file_churn]
            additions = [f[1]['additions'] for f in file_churn]
            deletions = [f[1]['deletions'] for f in file_churn]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Commits', x=files, y=commits, marker_color='lightblue'))
            fig.add_trace(go.Bar(name='Additions', x=files, y=additions, marker_color='lightgreen'))
            fig.add_trace(go.Bar(name='Deletions', x=files, y=deletions, marker_color='salmon'))
            
            fig.update_layout(
                title="File Churn (Top 15 Files)",
                xaxis_title="File",
                yaxis_title="Count",
                barmode='group',
                height=400,
                xaxis_tickangle=-45
            )
            charts['file_churn'] = fig.to_html(include_plotlyjs='cdn', div_id='churn-chart')
    
    # 5. Dependency Type Distribution Pie Chart
    dependencies = project_data.get('dependencies', {})
    if dependencies:
        dep_types = {}
        for pkg, info in dependencies.items():
            dep_type = info.get('type', 'unknown')
            dep_types[dep_type] = dep_types.get(dep_type, 0) + 1
        
        if dep_types:
            fig = go.Figure(data=[go.Pie(
                labels=list(dep_types.keys()),
                values=list(dep_types.values()),
                marker=dict(colors=px.colors.qualitative.Pastel)
            )])
            fig.update_layout(
                title="Dependency Types",
                height=400
            )
            charts['dependency_types'] = fig.to_html(include_plotlyjs='cdn', div_id='dep-types-chart')
    
    # 6. Code Quality Metrics Radar Chart
    if nextgen_report and 'code_evolution_dna' in nextgen_report:
        evolution = nextgen_report['code_evolution_dna']
        categories = []
        values = []
        
        if 'test_coverage_trend' in evolution:
            categories.append('Test Coverage')
            values.append(evolution.get('current_coverage_estimate', 0) * 100)
        
        avg_complexity = metrics.get('avg_complexity', 0)
        categories.append('Code Quality<br>(100-complexity)')
        values.append(max(0, 100 - avg_complexity * 2))
        
        comment_ratio = metrics.get('comment_ratio', 0)
        categories.append('Documentation')
        values.append(comment_ratio * 100)
        
        maintainability = 100 - (len(advanced_report.get('high_risk_files', [])) * 5)
        categories.append('Maintainability')
        values.append(max(0, maintainability))
        
        if categories and values:
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Project Metrics'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                title="Code Quality Overview",
                height=400
            )
            charts['quality_radar'] = fig.to_html(include_plotlyjs='cdn', div_id='quality-radar-chart')
    
    return charts


def _generate_project_analysis_html(project_data, file_data):
    """Generate HTML for project analysis tab"""
    if not project_data and not file_data:
        return "<p>No analysis data available.</p>"
    
    data = project_data or {'metrics': {}, 'files': [file_data] if file_data else []}
    metrics = data.get('metrics', {})
    
    # Generate Plotly charts
    charts = _generate_plotly_charts(data) if project_data else {}
    
    html = f"""
    <h2>Project Analysis Results</h2>
    """
    
    # Add interactive charts if available
    if charts:
        html += """
        <div class="metric-card">
            <h3>📊 Interactive Visualizations</h3>
            <p style="color: #666; margin-bottom: 20px;">Hover over charts for detailed information. Click and drag to zoom.</p>
        """
        
        # Add charts in a grid layout
        if 'quality_radar' in charts:
            html += f'<div style="margin-bottom: 30px;">{charts["quality_radar"]}</div>'
        
        # Row 1: Language distribution and dependency types
        html += '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px;">'
        if 'language_distribution' in charts:
            html += f'<div>{charts["language_distribution"]}</div>'
        if 'dependency_types' in charts:
            html += f'<div>{charts["dependency_types"]}</div>'
        html += '</div>'
        
        # Row 2: Risk scores and complexity
        html += '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px;">'
        if 'risk_scores' in charts:
            html += f'<div>{charts["risk_scores"]}</div>'
        if 'complexity' in charts:
            html += f'<div>{charts["complexity"]}</div>'
        html += '</div>'
        
        # Row 3: File churn (full width)
        if 'file_churn' in charts:
            html += f'<div style="margin-bottom: 30px;">{charts["file_churn"]}</div>'
        
        html += """
        </div>
        """
    
    html += """
    <div class="metric-grid">
        <div class="metric-item">
            <div class="metric-label">Total Files</div>
            <div class="metric-value">{:,}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Total Lines</div>
            <div class="metric-value">{:,}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Code Lines</div>
            <div class="metric-value">{:,}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Functions</div>
            <div class="metric-value">{:,}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Classes</div>
            <div class="metric-value">{:,}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Avg Complexity</div>
            <div class="metric-value">{:.1f}</div>
        </div>
    </div>
    """.format(
        metrics.get('total_files', 0),
        metrics.get('total_lines', 0),
        metrics.get('code_lines', 0),
        metrics.get('total_functions', 0),
        metrics.get('total_classes', 0),
        metrics.get('avg_complexity', 0)
    )
    
    html += """
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
    """Start Flask server for interactive React visualization"""
    if not HAS_FLASK:
        print("Flask not available. Install it for interactive mode: pip install flask")
        return
    
    from flask import Flask, send_from_directory, jsonify
    
    app = Flask(__name__, static_folder=None)
    app.config['SECRET_KEY'] = 'vipey-secret-key'
    
    # Get template directory
    template_dir = Path(__file__).parent / 'templates'
    dist_dir = template_dir / 'dist'
    
    # Store data globally for API endpoints
    app.config['STORYBOARD_DATA'] = storyboard_data
    app.config['PROJECT_DATA'] = project_data
    app.config['FILE_DATA'] = file_data
    
    @app.route('/')
    def index():
        """Serve the React app"""
        return send_from_directory(dist_dir, 'index.html')
    
    @app.route('/assets/<path:path>')
    def assets(path):
        """Serve static assets"""
        return send_from_directory(dist_dir / 'assets', path)
    
    @app.route('/api/storyboard')
    def get_storyboard():
        """API endpoint for storyboard data"""
        data = app.config.get('STORYBOARD_DATA', {})
        if not data:
            return jsonify({
                'frames': [],
                'return_value': None,
                'source_code': '# No storyboard data available',
                'function_name': 'N/A'
            })
        return jsonify(data)
    
    @app.route('/api/project')
    def get_project():
        """API endpoint for project analysis data"""
        from flask import Response
        
        project = app.config.get('PROJECT_DATA')
        file_info = app.config.get('FILE_DATA')
        
        if not project and not file_info:
            return Response('<p>No analysis data available.</p>', mimetype='text/html')
        
        # Generate HTML for project analysis
        html = _generate_project_analysis_html(project, file_info)
        return Response(html, mimetype='text/html')
    
    @app.route('/api/documentation')
    def get_documentation():
        """API endpoint for documentation"""
        doc_path = Path(__file__).parent.parent / "DOCUMENTATION.md"
        if not doc_path.exists():
            return '<p>Documentation not found.</p>'
        
        with open(doc_path, 'r', encoding='utf-8') as f:
            doc_content = f.read()
        
        if HAS_MARKDOWN:
            html = markdown.markdown(doc_content, extensions=['fenced_code', 'tables', 'toc'])
        else:
            html = f"<pre>{doc_content}</pre>"
        
        return html
    
    # Track if browser has been opened
    browser_opened = False
    
    def open_browser():
        nonlocal browser_opened
        if not browser_opened:
            time.sleep(1.5)
            webbrowser.open('http://127.0.0.1:5000')
            browser_opened = True
    
    # Start browser in separate thread (only once)
    threading.Thread(target=open_browser, daemon=True).start()
    
    print("\n" + "="*70)
    print("🚀 Vipey Interactive Server")
    print("="*70)
    print()
    print("  ➜  Local:   \033[1;36mhttp://127.0.0.1:5000\033[0m")
    print()
    print("  Press \033[1;31mCtrl+C\033[0m to stop the server")
    print("="*70 + "\n")
    
    try:
        app.run(debug=False, port=5000, use_reloader=False, threaded=True)
    except KeyboardInterrupt:
        print("\n" + "="*70)
        print("✋ Server stopped by user")
        print("="*70)


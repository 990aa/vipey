# renderer.py
import json
import os
import re

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

// CodePane.tsx
import React, { useEffect, useRef } from 'react';

interface CodePaneProps {
  code: string;
  highlightLine: number;
}

export const CodePane: React.FC<CodePaneProps> = ({ code, highlightLine }) => {
  const codeRef = useRef<HTMLPreElement>(null);

  useEffect(() => {
    // Simple syntax highlighting for Python
    if (codeRef.current) {
      const lines = code.split('\n');
      const highlighted = lines.map((line, index) => {
        const lineNumber = index + 1;
        const isHighlighted = lineNumber === highlightLine;
        
        // Basic Python syntax highlighting
        let coloredLine = line
          .replace(/\b(def|class|if|else|elif|for|while|return|import|from|as|try|except|finally|with|pass|break|continue|yield|async|await)\b/g, '<span style="color: #C678DD">$1</span>')
          .replace(/\b(True|False|None|self)\b/g, '<span style="color: #D19A66">$1</span>')
          .replace(/(#.*$)/g, '<span style="color: #5C6370">$1</span>')
          .replace(/"([^"]*)"/g, '<span style="color: #98C379">"$1"</span>')
          .replace(/'([^']*)'/g, '<span style="color: #98C379">\'$1\'</span>')
          .replace(/\b(\d+)\b/g, '<span style="color: #D19A66">$1</span>');

        return `
          <div style="
            display: flex;
            ${isHighlighted ? 'background: rgba(255, 215, 0, 0.15); border-left: 3px solid #ffd700;' : ''}
            padding: 0 10px;
          ">
            <span style="
              color: #5C6370;
              min-width: 40px;
              text-align: right;
              padding-right: 20px;
              user-select: none;
            ">${lineNumber}</span>
            <span style="flex: 1; white-space: pre;">${coloredLine || ' '}</span>
          </div>
        `;
      }).join('');
      
      codeRef.current.innerHTML = highlighted;
    }
  }, [code, highlightLine]);

  return (
    <div style={{ 
      borderRadius: '6px', 
      overflow: 'auto',
      border: '1px solid #30363d',
      background: '#1e2127',
      maxHeight: '600px'
    }}>
      <pre 
        ref={codeRef}
        style={{
          margin: 0,
          padding: '15px 0',
          fontSize: '14px',
          lineHeight: '1.6',
          fontFamily: "'Consolas', 'Monaco', 'Courier New', monospace",
          color: '#ABB2BF'
        }}
      />
    </div>
  );
};

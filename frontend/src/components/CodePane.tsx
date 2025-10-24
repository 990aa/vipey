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
          .replace(/\b(def|class|if|else|elif|for|while|return|import|from|as|try|except|finally|with|pass|break|continue|yield|async|await)\b/g, '<span style="color: #1565c0">$1</span>')
          .replace(/\b(True|False|None|self)\b/g, '<span style="color: #1976d2">$1</span>')
          .replace(/(#.*$)/g, '<span style="color: #5c6bc0">$1</span>')
          .replace(/"([^"]*)"/g, '<span style="color: #388e3c">"$1"</span>')
          .replace(/'([^']*)'/g, '<span style="color: #388e3c">\'$1\'</span>')
          .replace(/\b(\d+)\b/g, '<span style="color: #1976d2">$1</span>');

        return `
          <div style="
            display: flex;
            ${isHighlighted ? 'background: rgba(30, 136, 229, 0.3); border-left: 4px solid #1e88e5; transform: translateX(2px);' : ''}
            padding: 4px 10px;
            transition: all 0.3s ease;
            margin: 2px 0;
          ">
            <span style="
              color: #5c6bc0;
              min-width: 40px;
              text-align: right;
              padding-right: 20px;
              user-select: none;
              font-weight: ${isHighlighted ? 'bold' : 'normal'};
            ">${lineNumber}</span>
            <span style="flex: 1; white-space: pre;">${coloredLine || ' '}</span>
          </div>
        `;
      }).join('');
      
      codeRef.current.innerHTML = highlighted;
      
      // Smooth scroll to highlighted line
      if (highlightLine > 0) {
        const highlightedElement = codeRef.current.children[highlightLine - 1] as HTMLElement;
        if (highlightedElement) {
          highlightedElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }
    }
  }, [code, highlightLine]);

  return (
    <div style={{ 
      borderRadius: '8px', 
      overflow: 'auto',
      border: '1px solid #64b5f6',
      background: '#e3f2fd',
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
          color: '#1a237e'
        }}
      />
    </div>
  );
};

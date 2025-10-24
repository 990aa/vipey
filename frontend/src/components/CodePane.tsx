// CodePane.tsx
import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface CodePaneProps {
  code: string;
  highlightLine: number;
}

export const CodePane: React.FC<CodePaneProps> = ({ code, highlightLine }) => {
  const lineProps = (lineNumber: number) => {
    const style: React.CSSProperties = { display: 'block', padding: '0 10px' };
    if (lineNumber === highlightLine) {
      style.backgroundColor = 'rgba(255, 215, 0, 0.15)';
      style.borderLeft = '3px solid #ffd700';
    }
    return { style };
  };

  return (
    <div style={{ 
      borderRadius: '6px', 
      overflow: 'hidden',
      border: '1px solid #30363d' 
    }}>
      <SyntaxHighlighter
        language="python"
        style={vscDarkPlus}
        showLineNumbers={true}
        wrapLines={true}
        lineProps={lineProps}
        customStyle={{
          margin: 0,
          padding: '15px',
          fontSize: '14px',
          lineHeight: '1.6'
        }}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
};

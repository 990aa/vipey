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
    const style: React.CSSProperties = { display: 'block' };
    if (lineNumber === highlightLine) {
      style.backgroundColor = 'rgba(255, 255, 0, 0.2)';
    }
    return { style };
  };

  return (
    <SyntaxHighlighter
      language="python"
      style={vscDarkPlus}
      showLineNumbers={true}
      wrapLines={true}
      lineProps={lineProps}
    >
      {code}
    </SyntaxHighlighter>
  );
};

// VisualizationPane.tsx
import React from 'react';
import { ArrayVisualizer } from './ArrayVisualizer';

interface VisualizationPaneProps {
  variable: any;
}

export const VisualizationPane: React.FC<VisualizationPaneProps> = ({ variable }) => {
  if (!variable) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: '40px', 
        color: '#8b949e',
        fontSize: '1.1em'
      }}>
        No variables to display
      </div>
    );
  }

  // Display all local variables
  return (
    <div style={{ padding: '15px' }}>
      {Object.entries(variable).map(([key, value]) => {
        const varType = Array.isArray(value) ? 'list' : typeof value;
        
        return (
          <div 
            key={key} 
            style={{ 
              marginBottom: '25px', 
              background: '#161b22',
              borderRadius: '8px',
              padding: '15px',
              border: '1px solid #30363d'
            }}
          >
            <h3 style={{ 
              margin: '0 0 15px 0',
              color: '#58a6ff',
              fontSize: '1.1em',
              display: 'flex',
              alignItems: 'center',
              gap: '10px'
            }}>
              <span>{key}</span>
              <span style={{ 
                fontSize: '0.75em', 
                color: '#8b949e',
                background: '#0d1117',
                padding: '4px 10px',
                borderRadius: '12px',
                fontWeight: 'normal'
              }}>
                {varType}
              </span>
            </h3>
            {Array.isArray(value) ? (
              <ArrayVisualizer data={value} />
            ) : (
              <pre style={{ 
                backgroundColor: '#0d1117', 
                color: '#79c0ff',
                padding: '15px', 
                borderRadius: '6px',
                overflow: 'auto',
                margin: 0,
                border: '1px solid #30363d',
                fontSize: '0.95em',
                lineHeight: '1.6'
              }}>
                {JSON.stringify(value, null, 2)}
              </pre>
            )}
          </div>
        );
      })}
    </div>
  );
};

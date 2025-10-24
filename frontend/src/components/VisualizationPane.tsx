// VisualizationPane.tsx
import React from 'react';
import { ArrayVisualizer } from './ArrayVisualizer';
import { LinkedListVisualizer } from './LinkedListVisualizer';
import { TreeVisualizer } from './TreeVisualizer';
import { GraphVisualizer } from './GraphVisualizer';
import { HashMapVisualizer } from './HashMapVisualizer';

interface VisualizationPaneProps {
  variable: any;
}

export const VisualizationPane: React.FC<VisualizationPaneProps> = ({ variable }) => {
  if (!variable) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: '40px', 
        color: '#1565c0',
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
              background: '#bbdefb',
              borderRadius: '8px',
              padding: '15px',
              border: '1px solid #64b5f6',
              animation: 'fadeIn 0.3s ease',
              transition: 'all 0.3s ease'
            }}
          >
            <h3 style={{ 
              margin: '0 0 15px 0',
              color: '#0d47a1',
              fontSize: '1.1em',
              display: 'flex',
              alignItems: 'center',
              gap: '10px'
            }}>
              <span>{key}</span>
              <span style={{ 
                fontSize: '0.75em', 
                color: '#1565c0',
                background: '#e3f2fd',
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
                backgroundColor: '#e3f2fd', 
                color: '#0d47a1',
                padding: '15px', 
                borderRadius: '6px',
                overflow: 'auto',
                margin: 0,
                border: '1px solid #64b5f6',
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

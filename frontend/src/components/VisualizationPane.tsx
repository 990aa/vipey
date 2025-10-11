// VisualizationPane.tsx
import React from 'react';
import { ArrayVisualizer } from './ArrayVisualizer';

interface VisualizationPaneProps {
  variable: any;
}

export const VisualizationPane: React.FC<VisualizationPaneProps> = ({ variable }) => {
  if (!variable) {
    return <div>No variables to display</div>;
  }

  // Display all local variables
  return (
    <div style={{ padding: '10px' }}>
      {Object.entries(variable).map(([key, value]) => {
        const varType = Array.isArray(value) ? 'list' : typeof value;
        
        return (
          <div key={key} style={{ marginBottom: '20px', borderBottom: '1px solid #eee', paddingBottom: '10px' }}>
            <h3 style={{ margin: '5px 0' }}>
              {key} <span style={{ fontSize: '12px', color: '#666' }}>({varType})</span>
            </h3>
            {Array.isArray(value) ? (
              <ArrayVisualizer data={value} />
            ) : (
              <pre style={{ 
                backgroundColor: '#f5f5f5', 
                padding: '10px', 
                borderRadius: '4px',
                overflow: 'auto'
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

// ArrayVisualizer.tsx
import React from 'react';

interface ArrayVisualizerProps {
  data: any[];
}

export const ArrayVisualizer: React.FC<ArrayVisualizerProps> = ({ data }) => {
  if (!Array.isArray(data)) {
    return <div>Invalid array data</div>;
  }

  return (
    <div style={{ 
      display: 'flex', 
      gap: '5px', 
      padding: '10px',
      flexWrap: 'wrap'
    }}>
      {data.map((item, index) => (
        <div
          key={index}
          style={{
            padding: '10px 15px',
            border: '2px solid #333',
            borderRadius: '4px',
            backgroundColor: '#f0f0f0',
            minWidth: '40px',
            textAlign: 'center',
            fontFamily: 'monospace',
          }}
        >
          <div style={{ fontSize: '10px', color: '#666' }}>[{index}]</div>
          <div style={{ fontSize: '16px', fontWeight: 'bold' }}>
            {JSON.stringify(item)}
          </div>
        </div>
      ))}
    </div>
  );
};

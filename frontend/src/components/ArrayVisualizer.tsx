// ArrayVisualizer.tsx
import React from 'react';

interface ArrayVisualizerProps {
  data: any[];
}

export const ArrayVisualizer: React.FC<ArrayVisualizerProps> = ({ data }) => {
  if (!Array.isArray(data)) {
    return <div style={{ color: '#da3633' }}>Invalid array data</div>;
  }

  return (
    <div style={{ 
      display: 'flex', 
      gap: '10px', 
      padding: '15px',
      flexWrap: 'wrap',
      background: '#0d1117',
      borderRadius: '6px',
      border: '1px solid #30363d'
    }}>
      {data.map((item, index) => (
        <div
          key={index}
          style={{
            padding: '12px 18px',
            border: '2px solid #58a6ff',
            borderRadius: '8px',
            background: 'linear-gradient(135deg, #161b22 0%, #1c2128 100%)',
            minWidth: '50px',
            textAlign: 'center',
            fontFamily: 'monospace',
            transition: 'all 0.3s ease',
            cursor: 'default',
            boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-4px)';
            e.currentTarget.style.boxShadow = '0 6px 12px rgba(88, 166, 255, 0.3)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 2px 4px rgba(0,0,0,0.2)';
          }}
        >
          <div style={{ fontSize: '11px', color: '#8b949e', marginBottom: '4px' }}>
            [{index}]
          </div>
          <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#79c0ff' }}>
            {JSON.stringify(item)}
          </div>
        </div>
      ))}
    </div>
  );
};

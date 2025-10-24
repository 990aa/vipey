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
      background: '#e3f2fd',
      borderRadius: '6px',
      border: '1px solid #64b5f6'
    }}>
      {data.map((item, index) => (
        <div
          key={index}
          style={{
            padding: '12px 18px',
            border: '2px solid #1e88e5',
            borderRadius: '8px',
            background: 'linear-gradient(135deg, #bbdefb 0%, #90caf9 100%)',
            minWidth: '50px',
            textAlign: 'center',
            fontFamily: 'monospace',
            transition: 'all 0.3s ease',
            cursor: 'default',
            boxShadow: '0 2px 4px rgba(21, 101, 192, 0.2)',
            animation: 'slideIn 0.3s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-4px) scale(1.05)';
            e.currentTarget.style.boxShadow = '0 6px 12px rgba(30, 136, 229, 0.4)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0) scale(1)';
            e.currentTarget.style.boxShadow = '0 2px 4px rgba(21, 101, 192, 0.2)';
          }}
        >
          <div style={{ fontSize: '11px', color: '#1565c0', marginBottom: '4px', fontWeight: 600 }}>
            [{index}]
          </div>
          <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#0d47a1' }}>
            {JSON.stringify(item)}
          </div>
        </div>
      ))}
    </div>
  );
};

// HashMapVisualizer.tsx
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

interface HashMapData {
  type: 'HashMap' | 'LRUCache';
  buckets?: Array<Array<[any, any]>>;
  entries?: Array<[any, any]>;
  capacity?: number;
  size?: number;
  display?: string;
  recentlyAccessed?: any;
  evicted?: any;
}

interface HashMapVisualizerProps {
  data: HashMapData;
  currentStep?: number;
}

export const HashMapVisualizer: React.FC<HashMapVisualizerProps> = ({ data, currentStep = 0 }) => {
  const [displayMode, setDisplayMode] = useState<'buckets' | 'list'>('list');

  useEffect(() => {
    // Auto-detect display mode
    if (data.buckets && data.buckets.length > 0) {
      setDisplayMode('buckets');
    } else {
      setDisplayMode('list');
    }
  }, [data]);

  if (!data) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: '40px',
        color: '#1565c0',
        fontSize: '1.1em'
      }}>
        Empty hash map
      </div>
    );
  }

  // LRU Cache visualization (Doubly Linked List + Hash Map)
  if (data.type === 'LRUCache' && data.entries) {
    return (
      <div style={{ 
        padding: '20px',
        background: '#e3f2fd',
        borderRadius: '8px',
        border: '2px solid #64b5f6',
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px',
        }}>
          <h3 style={{ margin: 0, color: '#0d47a1', fontSize: '1.2em' }}>
            💾 LRU Cache
          </h3>
          <div style={{ 
            background: '#bbdefb', 
            padding: '6px 12px', 
            borderRadius: '8px',
            fontSize: '13px',
            fontWeight: 600,
            color: '#0d47a1',
          }}>
            {data.size ?? data.entries.length} / {data.capacity ?? '∞'}
          </div>
        </div>

        <div style={{ 
          display: 'flex', 
          flexDirection: 'column',
          gap: '12px',
        }}>
          <div style={{
            fontSize: '12px',
            color: '#1565c0',
            fontWeight: 600,
            marginBottom: '5px',
          }}>
            Most Recent → Least Recent
          </div>
          
          <div style={{ 
            display: 'flex', 
            gap: '15px',
            overflowX: 'auto',
            padding: '10px',
          }}>
            {data.entries.map(([key, value], index) => {
              const isRecent = data.recentlyAccessed === key;
              const isEvicted = data.evicted === key;

              return (
                <motion.div
                  key={`${key}-${index}`}
                  initial={{ scale: 0.8, opacity: 0, x: -20 }}
                  animate={{ 
                    scale: isRecent ? 1.1 : 1, 
                    opacity: isEvicted ? 0.3 : 1,
                    x: 0,
                  }}
                  transition={{ delay: index * 0.05, duration: 0.3 }}
                  style={{
                    minWidth: '100px',
                    padding: '15px',
                    background: isRecent
                      ? 'linear-gradient(135deg, #66bb6a 0%, #43a047 100%)'
                      : isEvicted
                      ? 'linear-gradient(135deg, #ef5350 0%, #e53935 100%)'
                      : 'linear-gradient(135deg, #bbdefb 0%, #90caf9 100%)',
                    border: `3px solid ${isRecent ? '#2e7d32' : isEvicted ? '#c62828' : '#1e88e5'}`,
                    borderRadius: '12px',
                    textAlign: 'center',
                    boxShadow: isRecent 
                      ? '0 6px 16px rgba(67, 160, 71, 0.4)'
                      : '0 4px 8px rgba(30, 136, 229, 0.3)',
                    position: 'relative',
                  }}
                >
                  {isRecent && (
                    <div style={{
                      position: 'absolute',
                      top: -10,
                      right: -10,
                      background: '#4caf50',
                      color: 'white',
                      borderRadius: '50%',
                      width: '24px',
                      height: '24px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '14px',
                      fontWeight: 'bold',
                    }}>
                      ✓
                    </div>
                  )}
                  {isEvicted && (
                    <div style={{
                      position: 'absolute',
                      top: -10,
                      right: -10,
                      background: '#f44336',
                      color: 'white',
                      borderRadius: '50%',
                      width: '24px',
                      height: '24px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '14px',
                      fontWeight: 'bold',
                    }}>
                      ✗
                    </div>
                  )}
                  <div style={{ 
                    fontSize: '12px', 
                    color: isRecent || isEvicted ? 'white' : '#1565c0',
                    fontWeight: 600,
                    marginBottom: '8px',
                  }}>
                    key: {JSON.stringify(key)}
                  </div>
                  <div style={{ 
                    fontSize: '16px', 
                    fontWeight: 'bold',
                    color: isRecent || isEvicted ? 'white' : '#0d47a1',
                  }}>
                    {JSON.stringify(value)}
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  // Regular Hash Map visualization with buckets
  if (displayMode === 'buckets' && data.buckets) {
    return (
      <div style={{ 
        padding: '20px',
        background: '#e3f2fd',
        borderRadius: '8px',
        border: '2px solid #64b5f6',
        maxHeight: '400px',
        overflowY: 'auto',
      }}>
        <h3 style={{ margin: '0 0 20px 0', color: '#0d47a1', fontSize: '1.2em' }}>
          🗂️ Hash Map (Bucket View)
        </h3>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          {data.buckets.map((bucket, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05, duration: 0.3 }}
              style={{
                display: 'flex',
                gap: '10px',
                alignItems: 'center',
              }}
            >
              <div style={{
                minWidth: '60px',
                padding: '8px',
                background: '#bbdefb',
                border: '2px solid #64b5f6',
                borderRadius: '8px',
                textAlign: 'center',
                fontWeight: 600,
                color: '#0d47a1',
                fontSize: '13px',
              }}>
                [{index}]
              </div>
              
              <div style={{ 
                display: 'flex', 
                gap: '8px', 
                flexWrap: 'wrap',
                flex: 1,
              }}>
                {bucket.length === 0 ? (
                  <div style={{ 
                    color: '#5c6bc0', 
                    fontSize: '13px',
                    fontStyle: 'italic',
                  }}>
                    empty
                  </div>
                ) : (
                  bucket.map(([key, value], entryIndex) => (
                    <div
                      key={entryIndex}
                      style={{
                        padding: '10px 15px',
                        background: 'linear-gradient(135deg, #90caf9 0%, #64b5f6 100%)',
                        border: '2px solid #1e88e5',
                        borderRadius: '8px',
                        fontSize: '13px',
                        fontWeight: 600,
                        color: '#0d47a1',
                        boxShadow: '0 2px 4px rgba(30, 136, 229, 0.3)',
                      }}
                    >
                      {JSON.stringify(key)}: {JSON.stringify(value)}
                    </div>
                  ))
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    );
  }

  // Simple list view for hash map entries
  if (data.entries) {
    return (
      <div style={{ 
        padding: '20px',
        background: '#e3f2fd',
        borderRadius: '8px',
        border: '2px solid #64b5f6',
      }}>
        <h3 style={{ margin: '0 0 20px 0', color: '#0d47a1', fontSize: '1.2em' }}>
          🗂️ Hash Map
        </h3>
        
        <div style={{ 
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))',
          gap: '12px',
        }}>
          {data.entries.map(([key, value], index) => (
            <motion.div
              key={index}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: index * 0.05, duration: 0.3 }}
              style={{
                padding: '15px',
                background: 'linear-gradient(135deg, #bbdefb 0%, #90caf9 100%)',
                border: '2px solid #1e88e5',
                borderRadius: '12px',
                textAlign: 'center',
                boxShadow: '0 4px 8px rgba(30, 136, 229, 0.3)',
              }}
            >
              <div style={{ 
                fontSize: '12px', 
                color: '#1565c0',
                fontWeight: 600,
                marginBottom: '8px',
              }}>
                {JSON.stringify(key)}
              </div>
              <div style={{ 
                fontSize: '16px', 
                fontWeight: 'bold',
                color: '#0d47a1',
              }}>
                {JSON.stringify(value)}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div style={{ 
      textAlign: 'center', 
      padding: '40px',
      color: '#1565c0',
      fontSize: '1.1em'
    }}>
      No data to display
    </div>
  );
};

// LinkedListVisualizer.tsx
import React, { useEffect, useState } from 'react';
import { ReactFlow, Node, Edge, Position, MarkerType } from '@xyflow/react';
import { motion } from 'framer-motion';
import '@xyflow/react/dist/style.css';

interface LinkedListData {
  type: 'LinkedList';
  values: any[];
  display: string;
  pointers?: { from: number; to: number; label?: string }[];
}

interface LinkedListVisualizerProps {
  data: LinkedListData;
  currentStep?: number;
}

export const LinkedListVisualizer: React.FC<LinkedListVisualizerProps> = ({ data, currentStep = 0 }) => {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);

  useEffect(() => {
    if (!data || !data.values) return;

    // Create nodes for each value in the linked list
    const newNodes: Node[] = data.values.map((value, index) => ({
      id: `node-${index}`,
      data: { 
        label: (
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: index * 0.1, duration: 0.3 }}
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '8px',
              padding: '12px',
              background: 'linear-gradient(135deg, #bbdefb 0%, #90caf9 100%)',
              border: '3px solid #1e88e5',
              borderRadius: '12px',
              minWidth: '70px',
              boxShadow: '0 4px 8px rgba(30, 136, 229, 0.3)',
            }}
          >
            <div style={{ 
              fontSize: '11px', 
              color: '#1565c0', 
              fontWeight: 600,
              fontFamily: 'monospace'
            }}>
              [{index}]
            </div>
            <div style={{ 
              fontSize: '20px', 
              fontWeight: 'bold', 
              color: '#0d47a1',
              fontFamily: 'monospace'
            }}>
              {typeof value === 'string' && value === '...' ? value : JSON.stringify(value)}
            </div>
          </motion.div>
        )
      },
      position: { x: index * 150, y: 50 },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
      draggable: false,
      style: {
        background: 'transparent',
        border: 'none',
        padding: 0,
      }
    }));

    // Create edges between nodes (next pointers)
    const newEdges: Edge[] = [];
    for (let i = 0; i < data.values.length - 1; i++) {
      // Don't create edge if next value is "..."
      if (data.values[i + 1] !== '...') {
        newEdges.push({
          id: `edge-${i}`,
          source: `node-${i}`,
          target: `node-${i + 1}`,
          animated: true,
          style: { 
            stroke: '#1e88e5', 
            strokeWidth: 3,
          },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            width: 20,
            height: 20,
            color: '#1e88e5',
          },
          label: 'next',
          labelStyle: {
            fill: '#0d47a1',
            fontWeight: 600,
            fontSize: '12px',
          },
          labelBgStyle: {
            fill: '#e3f2fd',
            fillOpacity: 0.9,
          },
        });
      }
    }

    // Add custom pointers if provided (e.g., for reversing operations)
    if (data.pointers) {
      data.pointers.forEach((pointer, idx) => {
        newEdges.push({
          id: `pointer-${idx}`,
          source: `node-${pointer.from}`,
          target: `node-${pointer.to}`,
          animated: true,
          style: { 
            stroke: '#f44336', 
            strokeWidth: 2,
            strokeDasharray: '5,5',
          },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            width: 15,
            height: 15,
            color: '#f44336',
          },
          label: pointer.label || '',
          labelStyle: {
            fill: '#c62828',
            fontWeight: 700,
            fontSize: '11px',
          },
          labelBgStyle: {
            fill: '#ffebee',
            fillOpacity: 0.95,
          },
        });
      });
    }

    setNodes(newNodes);
    setEdges(newEdges);
  }, [data, currentStep]);

  if (!data || !data.values || data.values.length === 0) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: '40px',
        color: '#1565c0',
        fontSize: '1.1em'
      }}>
        Empty linked list
      </div>
    );
  }

  return (
    <div style={{ 
      height: '250px', 
      width: '100%',
      background: '#e3f2fd',
      borderRadius: '8px',
      border: '2px solid #64b5f6',
      overflow: 'hidden'
    }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        attributionPosition="bottom-left"
        proOptions={{ hideAttribution: true }}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
        zoomOnScroll={false}
        panOnDrag={false}
        preventScrolling={false}
      />
    </div>
  );
};

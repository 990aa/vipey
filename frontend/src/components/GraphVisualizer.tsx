// GraphVisualizer.tsx
import React, { useEffect, useState } from 'react';
import { ReactFlow, Node, Edge, Position, MarkerType } from '@xyflow/react';
import { motion } from 'framer-motion';
import '@xyflow/react/dist/style.css';

interface GraphData {
  type: 'Graph';
  nodes: number[];
  edges: Array<[number, number]>;
  directed?: boolean;
  weighted?: boolean;
  weights?: { [key: string]: number };
  display?: string;
  highlighted_nodes?: number[];
  highlighted_edges?: Array<[number, number]>;
}

interface GraphVisualizerProps {
  data: GraphData;
  currentStep?: number;
}

export const GraphVisualizer: React.FC<GraphVisualizerProps> = ({ data, currentStep = 0 }) => {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);

  useEffect(() => {
    if (!data || !data.nodes) return;

    // Circular layout for nodes
    const numNodes = data.nodes.length;
    const radius = Math.min(200, 50 + numNodes * 15);
    const centerX = 300;
    const centerY = 200;

    const newNodes: Node[] = data.nodes.map((nodeValue, index) => {
      const angle = (2 * Math.PI * index) / numNodes - Math.PI / 2;
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);

      const isHighlighted = data.highlighted_nodes?.includes(nodeValue);

      return {
        id: `node-${nodeValue}`,
        data: {
          label: (
            <motion.div
              initial={{ scale: 0, opacity: 0 }}
              animate={{ 
                scale: 1, 
                opacity: 1,
                boxShadow: isHighlighted 
                  ? '0 0 20px rgba(244, 67, 54, 0.8)' 
                  : '0 4px 12px rgba(30, 136, 229, 0.4)'
              }}
              transition={{ delay: index * 0.08, duration: 0.3 }}
              style={{
                width: '50px',
                height: '50px',
                borderRadius: '50%',
                background: isHighlighted
                  ? 'linear-gradient(135deg, #f44336 0%, #c62828 100%)'
                  : 'linear-gradient(135deg, #1e88e5 0%, #1565c0 100%)',
                border: isHighlighted ? '4px solid #b71c1c' : '3px solid #0d47a1',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                fontWeight: 'bold',
                fontSize: '18px',
                transition: 'all 0.3s ease',
              }}
            >
              {nodeValue}
            </motion.div>
          ),
        },
        position: { x, y },
        draggable: false,
        style: {
          background: 'transparent',
          border: 'none',
          padding: 0,
        },
      };
    });

    const newEdges: Edge[] = data.edges.map((edge, index) => {
      const [from, to] = edge;
      const edgeKey = `${from}-${to}`;
      const isHighlighted = data.highlighted_edges?.some(
        ([hFrom, hTo]) => (hFrom === from && hTo === to) || (!data.directed && hFrom === to && hTo === from)
      );

      let weight = null;
      if (data.weighted && data.weights) {
        weight = data.weights[edgeKey] ?? data.weights[`${to}-${from}`] ?? null;
      }

      return {
        id: `edge-${from}-${to}`,
        source: `node-${from}`,
        target: `node-${to}`,
        animated: isHighlighted,
        style: {
          stroke: isHighlighted ? '#f44336' : '#42a5f5',
          strokeWidth: isHighlighted ? 4 : 2,
        },
        markerEnd: data.directed ? {
          type: MarkerType.ArrowClosed,
          width: 20,
          height: 20,
          color: isHighlighted ? '#f44336' : '#42a5f5',
        } : undefined,
        label: weight !== null ? String(weight) : undefined,
        labelStyle: {
          fill: '#0d47a1',
          fontWeight: 700,
          fontSize: '13px',
        },
        labelBgStyle: {
          fill: '#e3f2fd',
          fillOpacity: 0.95,
          rx: 8,
          ry: 8,
        },
      };
    });

    setNodes(newNodes);
    setEdges(newEdges);
  }, [data, currentStep]);

  if (!data || !data.nodes || data.nodes.length === 0) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: '40px',
        color: '#1565c0',
        fontSize: '1.1em'
      }}>
        Empty graph
      </div>
    );
  }

  return (
    <div style={{ 
      height: '450px', 
      width: '100%',
      background: '#e3f2fd',
      borderRadius: '8px',
      border: '2px solid #64b5f6',
      overflow: 'hidden',
      position: 'relative'
    }}>
      <div style={{
        position: 'absolute',
        top: 10,
        right: 10,
        zIndex: 10,
        background: '#bbdefb',
        padding: '8px 12px',
        borderRadius: '8px',
        border: '2px solid #64b5f6',
        fontSize: '12px',
        fontWeight: 600,
        color: '#0d47a1',
      }}>
        {data.directed ? '🔀 Directed' : '🔗 Undirected'} | {data.nodes.length} nodes | {data.edges.length} edges
      </div>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        attributionPosition="bottom-left"
        proOptions={{ hideAttribution: true }}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
        zoomOnScroll={true}
        panOnDrag={true}
        minZoom={0.3}
        maxZoom={1.5}
      />
    </div>
  );
};

// TreeVisualizer.tsx
import React, { useEffect, useState } from 'react';
import { ReactFlow, Node, Edge, Position, MarkerType } from '@xyflow/react';
import { motion } from 'framer-motion';
import '@xyflow/react/dist/style.css';

interface TreeNode {
  value: any;
  left?: TreeNode;
  right?: TreeNode;
  height?: number;
  balance?: number;
}

interface TreeData {
  type: 'Tree' | 'BST' | 'AVL';
  root: TreeNode;
  display?: string;
}

interface TreeVisualizerProps {
  data: TreeData;
  currentStep?: number;
}

export const TreeVisualizer: React.FC<TreeVisualizerProps> = ({ data, currentStep = 0 }) => {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);

  useEffect(() => {
    if (!data || !data.root) return;

    const newNodes: Node[] = [];
    const newEdges: Edge[] = [];
    let nodeId = 0;

    // Calculate tree layout using level-order traversal
    const calculateLayout = (root: TreeNode | undefined, x: number, y: number, level: number, offset: number): string | null => {
      if (!root || root.value === null || root.value === undefined) return null;

      const currentId = `node-${nodeId++}`;
      
      // Create node with animation
      newNodes.push({
        id: currentId,
        data: {
          label: (
            <motion.div
              initial={{ scale: 0, opacity: 0, y: -20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              transition={{ delay: level * 0.15, duration: 0.4, type: 'spring' }}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                width: '60px',
                height: '60px',
                background: 'linear-gradient(135deg, #1e88e5 0%, #1565c0 100%)',
                border: '3px solid #0d47a1',
                borderRadius: '50%',
                color: 'white',
                fontWeight: 'bold',
                fontSize: '18px',
                boxShadow: '0 4px 12px rgba(30, 136, 229, 0.4)',
                position: 'relative',
              }}
            >
              <span>{JSON.stringify(root.value)}</span>
              {(root.height !== undefined || root.balance !== undefined) && (
                <div style={{
                  position: 'absolute',
                  bottom: '-22px',
                  fontSize: '10px',
                  color: '#0d47a1',
                  fontWeight: 600,
                  background: '#e3f2fd',
                  padding: '2px 6px',
                  borderRadius: '8px',
                  border: '1px solid #64b5f6',
                }}>
                  {root.height !== undefined && `h:${root.height}`}
                  {root.balance !== undefined && ` b:${root.balance}`}
                </div>
              )}
            </motion.div>
          ),
        },
        position: { x, y },
        sourcePosition: Position.Bottom,
        targetPosition: Position.Top,
        draggable: false,
        style: {
          background: 'transparent',
          border: 'none',
          padding: 0,
        },
      });

      // Recursively add children
      const verticalSpacing = 120;
      const horizontalOffset = offset / 2;

      if (root.left) {
        const leftId = calculateLayout(root.left, x - horizontalOffset, y + verticalSpacing, level + 1, horizontalOffset);
        if (leftId) {
          newEdges.push({
            id: `edge-${currentId}-left`,
            source: currentId,
            target: leftId,
            animated: false,
            style: {
              stroke: '#42a5f5',
              strokeWidth: 2,
            },
            markerEnd: {
              type: MarkerType.ArrowClosed,
              width: 15,
              height: 15,
              color: '#42a5f5',
            },
          });
        }
      }

      if (root.right) {
        const rightId = calculateLayout(root.right, x + horizontalOffset, y + verticalSpacing, level + 1, horizontalOffset);
        if (rightId) {
          newEdges.push({
            id: `edge-${currentId}-right`,
            source: currentId,
            target: rightId,
            animated: false,
            style: {
              stroke: '#42a5f5',
              strokeWidth: 2,
            },
            markerEnd: {
              type: MarkerType.ArrowClosed,
              width: 15,
              height: 15,
              color: '#42a5f5',
            },
          });
        }
      }

      return currentId;
    };

    // Calculate tree depth to determine initial offset
    const getDepth = (node: TreeNode | undefined): number => {
      if (!node || node.value === null || node.value === undefined) return 0;
      return 1 + Math.max(getDepth(node.left), getDepth(node.right));
    };

    const depth = getDepth(data.root);
    const initialOffset = Math.pow(2, depth) * 25;

    calculateLayout(data.root, 400, 30, 0, initialOffset);

    setNodes(newNodes);
    setEdges(newEdges);
  }, [data, currentStep]);

  if (!data || !data.root) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: '40px',
        color: '#1565c0',
        fontSize: '1.1em'
      }}>
        Empty tree
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
        zoomOnScroll={true}
        panOnDrag={true}
        minZoom={0.3}
        maxZoom={1.5}
      />
    </div>
  );
};

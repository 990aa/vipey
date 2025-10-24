"""Problem Statement:
Given an integer $n$ representing the number of nodes (labeled from $0$ to $n-1$) and a list of connections, where connections[i] = [a, b] represents an undirected edge between node $a$ and node $b$.Return a list of all critical connections in any order.

Example:
Input: 
$n = 4$, connections = [[0, 1], [1, 2], [2, 0], [1, 3]]Output: [[1, 3]]Explanation:The nodes 0, 1, and 2 form a cycle. Removing any edge between them ([0, 1], [1, 2], or [2, 0]) will not disconnect the graph.The edge [1, 3] is the only connection to node 3. If it is removed, node 3 becomes isolated, increasing the number of connected components from 1 to 2. Therefore, [1, 3] is a critical connection.

Output: [[1, 3]]

Explanation:The nodes 0, 1, and 2 form a cycle. Removing any edge between them ([0, 1], [1, 2], or [2, 0]) will not disconnect the graph.The edge [1, 3] is the only connection to node 3. If it is removed, node 3 becomes isolated, increasing the number of connected components from 1 to 2. Therefore, [1, 3] is a critical connection.

"""

from collections import defaultdict

class Solution:
    def criticalConnections(self, n: int, connections: list[list[int]]) -> list[list[int]]:
        # 1. Build the adjacency list
        graph = defaultdict(list)
        for u, v in connections:
            graph[u].append(v)
            graph[v].append(u)
            
        # 2. Initialize data structures for the algorithm
        # discovery_times: Stores the time a node is first visited
        # low_links: Stores the lowest discovery time reachable from this node
        # -1 indicates the node hasn't been visited yet.
        discovery_times = [-1] * n
        low_links = [-1] * n
        
        # We use a global timer to assign discovery times
        self.time = 0
        
        # List to store the bridges (critical connections)
        bridges = []

        # 3. Define the recursive DFS function
        def dfs(node: int, parent: int):
            # Mark the current node as visited by setting its times
            discovery_times[node] = self.time
            low_links[node] = self.time
            self.time += 1
            
            for neighbor in graph[node]:
                # Ignore the edge back to the parent
                if neighbor == parent:
                    continue
                    
                if discovery_times[neighbor] != -1:
                    # This is a "back-edge" to an already visited ancestor
                    # Update the low-link of the current node
                    low_links[node] = min(low_links[node], discovery_times[neighbor])
                else:
                    # This is a new node (part of the DFS tree)
                    # Recursively call DFS on the neighbor
                    dfs(neighbor, node)
                    
                    # After the DFS call returns, update the low-link of the
                    # current node based on the low-link of its child.
                    # This propagates the lowest reachable time up the tree.
                    low_links[node] = min(low_links[node], low_links[neighbor])
                    
                    # --- THIS IS THE CRITICAL CHECK ---
                    # If the lowest time the neighbor can reach is *after*
                    # this node's discovery, it means the *only* path
                    # from the neighbor back up the tree is through this
                    # (node, neighbor) edge. Thus, it's a bridge.
                    if low_links[neighbor] > discovery_times[node]:
                        bridges.append([node, neighbor])

        # 4. Start the DFS
        # We iterate in case the graph is disconnected, although
        # for this problem, we can assume it's connected (or start from 0).
        for i in range(n):
            if discovery_times[i] == -1:
                dfs(i, -1)  # -1 represents a null parent for the root
                
        return bridges

# --- Example Usage ---
sol = Solution()

# Example 1:
n1 = 4
connections1 = [[0, 1], [1, 2], [2, 0], [1, 3]]
print(f"Graph 1 (n={n1}, connections={connections1})")
bridges1 = sol.criticalConnections(n1, connections1)
print(f"Critical Connections: {bridges1}")  # Output: [[1, 3]]

print("-" * 20)

# Example 2: More complex
n2 = 6
connections2 = [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4], [4, 5], [5, 3]]
# 
# This graph has two cycles: (0, 1, 2) and (3, 4, 5). 
# The only edge connecting them is (1, 3).
print(f"Graph 2 (n={n2}, connections={connections2})")
bridges2 = sol.criticalConnections(n2, connections2)
print(f"Critical Connections: {bridges2}")  # Output: [[1, 3]]
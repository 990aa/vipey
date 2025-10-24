"""
Problem Statement:
Given an integer $n$ representing the number of nodes (labeled from $0$ to $n-1$) and a list of connections, where connections[i] = [a, b] represents a directed edge from node $a$ to node $b$.Return a list of all strongly connected components. Each component should be a list of the nodes it contains.

Example:
Input: $n = 5$, connections = [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]

Output: [[0, 1, 2], [3], [4]] (The order of components or nodes within them doesn't matter)

Explanation:
Nodes 0, 1, and 2 form a cycle ($0 \rightarrow 1 \rightarrow 2 \rightarrow 0$). You can get from any of them to any other. They form one SCC: [0, 1, 2].Node 3 can be reached from the cycle (via $1 \rightarrow 3$), but you cannot get back from 3 to the cycle. Node 3 can reach node 4.Node 4 can be reached from 3, but it cannot get back to 3 or to the main cycle.Therefore, [3] and [4] are "maximal" components of size 1. They are strongly connected only with themselves.
"""


from collections import defaultdict

class Solution:
    def findSCCs(self, n: int, connections: list[list[int]]) -> list[list[int]]:
        # 1. Build the adjacency list for the directed graph
        graph = defaultdict(list)
        for u, v in connections:
            graph[u].append(v)
            
        # 2. Initialize data structures
        # -1 indicates the node hasn't been visited
        discovery_times = [-1] * n
        # low_links stores the lowest discovery time reachable
        low_links = [-1] * n
        
        # 'on_stack' tracks nodes currently in the recursion stack
        # This is crucial to distinguish back-edges from cross-edges
        # to already processed components.
        stack = []
        on_stack = [False] * n
        
        # 'sccs' will store our final list of components
        sccs = []
        
        # Global timer for discovery times
        self.time = 0

        # 3. Define the recursive DFS function
        def dfs(node: int):
            # Set discovery time and low-link for the new node
            discovery_times[node] = self.time
            low_links[node] = self.time
            self.time += 1
            
            # Add to the stack and mark as "on stack"
            stack.append(node)
            on_stack[node] = True
            
            for neighbor in graph[node]:
                if discovery_times[neighbor] == -1:
                    # Neighbor hasn't been visited, so recurse
                    dfs(neighbor)
                    
                    # After recursion, update this node's low-link
                    # based on its child's low-link
                    low_links[node] = min(low_links[node], low_links[neighbor])
                    
                elif on_stack[neighbor]:
                    # Neighbor *is* visited AND *is* still on the stack
                    # This means we found a back-edge to an ancestor
                    # in the current SCC. Update low-link.
                    low_links[node] = min(low_links[node], discovery_times[neighbor])
            
            # --- THIS IS THE CRITICAL CHECK ---
            # If the low-link value is still this node's discovery time,
            # it means this node is the "root" of an SCC.
            if low_links[node] == discovery_times[node]:
                component = []
                while True:
                    # Pop nodes from the stack until we pop this
                    # 'node'. All popped nodes form the SCC.
                    popped_node = stack.pop()
                    on_stack[popped_node] = False
                    component.append(popped_node)
                    
                    if popped_node == node:
                        break
                sccs.append(component)

        # 4. Start DFS from each unvisited node
        for i in range(n):
            if discovery_times[i] == -1:
                dfs(i)
                
        return sccs

# --- Example Usage ---
sol = Solution()

# Example 1:
n1 = 5
connections1 = [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]
print(f"Graph 1 (n={n1}, connections={connections1})")
sccs1 = sol.findSCCs(n1, connections1)
print(f"Strongly Connected Components: {sccs1}") 
# Output: [[4], [3], [0, 1, 2]] (order may vary)

print("-" * 20)

# Example 2: More complex, multiple cycles
n2 = 8
connections2 = [
    [0, 1], [1, 2], [2, 0],  # SCC 1: {0, 1, 2}
    [1, 3], [3, 4], [4, 5],  # Path
    [5, 3],                 # SCC 2: {3, 4, 5}
    [2, 6], [6, 7], [7, 6]   # SCC 3: {6, 7}
]
print(f"Graph 2 (n={n2}, connections={connections2})")
sccs2 = sol.findSCCs(n2, connections2)
print(f"Strongly Connected Components: {sccs2}")
# Output: [[6, 7], [3, 4, 5], [0, 1, 2]] (order may vary)
from math import log, exp
"""
The Grash class with methods to process graph operations 

"""

class Graph(object):
    def __init__(self) -> None:
        """
        Initialize Graph class

        :return: None
        """
        self.v = 0 # No of vertices
        self.graph = {} # Store Graph relations with weights
        """
        e.g { USD: { CAD: 10, HKD: 5 }}
        """
        self.nodes = [] # Store all currency codes
        """
        e.g [USD, CAD, HKD]
        """
    def add_edge(self, s, d, w) -> None:
        """
        Add edge between nodes and assign weight

        :param str s: Source currency
        :param str d: Destination/Target currency
        :param str s: Conversion rate => after negate 
        :return: None
        """
        if s not in self.graph:
            self.graph[s] = {}
        self.graph[s][d] = w        
    
    def addNode(self, value) -> None:
        """
        Add node in the graph and increase nodes count

        :param str value: Set node value
        :return: None
        """
        self.nodes.append(value)
        self.v += 1

    def negate_logarithm_converter(self) -> None:
        """
        Negate logarithm converer for finding negative cycle in the graph

        :return: None
        """
        for s in self.graph:
            for d in self.graph[s]:
                self.graph[s][d] = -log(self.graph[s][d])   

    def getProfitCycle(self, src, predecessors):
        """
        Add node in the graph and increase nodes count

        :param str src: source currency
        :param list predecessors: List of predecessors to travarse back
        :return: list profit_cycle: List of profittable nodes
                 float profit_percentage: Profit percentage if we perform this trade
        """
        V, res = set(), []
        while src not in V:
            V.add(src)
            res.append(src)
            src = predecessors[src]
        res.append(src)
        path =  res[res.index(src):][::-1]
        result_amount = 0
        trade_sequence = [] 
        for i in range (1, len(path)):
            start = path[i-1]
            end = path[i]
            trade_sequence.append(start)
            result_amount += self.graph[start][end]	
        trade_sequence.append(end)
        result_amount = exp(-result_amount)		
        profit_percent = result_amount - 1
        if profit_percent > 0: # Here we can check certain criteria for profit percentage like above 2% only etc
            return trade_sequence, profit_percent
        return None, None
    
    def bfs(self, start, end) -> list:
        """
        Find shortest path between two nodes

        :param str start: Starting node
        :param str end: Target node
        :return: list: Shortest path nodes
        """
        queue = []
        queue.append([start])
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node == end:
                return path
            for adjecent in self.graph[node]:
                new_path = list(path)
                new_path.append(adjecent)
                queue.append(new_path)

    def dfs(self, node, visited) -> None:
        """
        Visit all the nodes nearby until last node in the path

        :param str node: Starting node
        :param dict visited: Dictionary of each node and status of visit
        :return: None
        """
        visited[node] = True
        stack = [node]
        while stack:
            node = stack.pop()
            for adj in self.graph[node]:
                if visited[adj] is None:
                    visited[adj] = True
                    stack.append(adj)

    def findNonReachableNodes(self, source):
        """
        Find shortest path between two nodes

        :param str source: Starting node
        :return: list: List of non reachable nodes from source node
        """
        visited = {i: None for i in self.nodes}
        self.dfs(source, visited)
        nonReachable = []
        for node in visited:
            if visited[node] is None:
                nonReachable.append(node)
        return nonReachable

    def getAmount(self, start, end, allCurrenciesSSP, profitablePath):
        """
        Prepare paths and calculate the profit amount 

        :param str start: Starting node
        :param str end: Target node
        :param list allCurrenciesSSP: All single source shortest paths from start node to end node
        :param list profitablePath: Most profitable node list
        :return: list: Final profitable trade sequence
                 float: Final amount 
        """
        path = allCurrenciesSSP[end]
        if start in profitablePath and end in profitablePath:
            startCycle = profitablePath
            endCycle = self.bfs(startCycle[-1], end)
            path = startCycle + endCycle            
        elif start in profitablePath:
            path = profitablePath[profitablePath.index(start):] + profitablePath[:profitablePath.index(start)]
            end_path = self.bfs(start, end)
            path = path + end_path
        elif end in profitablePath:
            commonNodes = list(set(profitablePath).intersection(path))
            nodesCount = float('Inf')
            startChain = []
            for i in commonNodes:
                if len(allCurrenciesSSP[i]) < nodesCount:
                    startChain = allCurrenciesSSP[i]
                    nodesCount = len(allCurrenciesSSP[i])
            node = startChain[-1]
            initialCycle = profitablePath[profitablePath.index(node):]            
            remainingCycle = []
            if len(initialCycle) != len(profitablePath):
                remainingCycle = profitablePath[:profitablePath.index(node)]    
            initialCycle.pop(0)            
            endCycle = profitablePath[:profitablePath.index(end)]
            endCycle.append(end)
            path =  startChain + initialCycle + remainingCycle + endCycle            
        else:
            startNodeCount = float('Inf')
            endNodeCount = float('Inf')
            startPath = []
            endPath = []
            for i in profitablePath:
                startPart = self.bfs(start, i)
                endPart = self.bfs(i, end)
                if len(startPart) < startNodeCount:
                    startPath = startPart
                    startNodeCount = len(startPart)
                if len(endPart) < endNodeCount:
                    endPath = endPart
                    endNodeCount = len(endPart)            
            path = startPath + profitablePath + endPath

        finalAmount = 0
        for i in range(1, len(path)):
            if path[i-1] == path[i]:
                continue
            if path[i-1] in self.graph:
                if path[i] in self.graph[path[i-1]]:
                    finalAmount += self.graph[path[i-1]][path[i]]
        return path, exp(-finalAmount)

    def bellmanFord(self, src):
        """
        Bellman ford algorithm to find profit opprtunity and return most profitable sequence 

        :param str src: Starting node
        :return: list: List of most profitable trade nodes
        """
        distance = {i: float('Inf') for i in self.nodes}
        predecessors = {i: None for i in self.nodes}
        distance[src] = 0
        max_profit_sequence = []
        max_profit_percent = 0
        for _ in range(self.v - 1):
            for s in self.graph:
                for d in self.graph[s]:
                    if distance[s] !=float("Inf") and distance[d] > distance[s] + self.graph[s][d]:
                        distance[d] = distance[s] + self.graph[s][d]
                        predecessors[d] = s
                        if d == src:
                            path, profit_percent = self.getProfitCycle(src, predecessors)
                            if path is not None and profit_percent > max_profit_percent:
                                max_profit_sequence = path
                                max_profit_percent = profit_percent
                            
        for s in self.graph:
            for d in self.graph[s]:
                if d == src:
                    if distance[s] !=float("Inf") and distance[d] > distance[s] + self.graph[s][d]:   
                        path, profit_percent = self.getProfitCycle(src, predecessors)
                        if profit_percent is not None and profit_percent > max_profit_percent:
                            max_profit_sequence = path
                            max_profit_percent = profit_percent                       
        return max_profit_sequence
       
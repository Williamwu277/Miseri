import random


class Tree:

    def __init__(self, params):
        self.nodes = params[0]
        self.weight = params[1]
        self.key = params[2]
        self.alt = params[3]

        if self.nodes > 100:
            raise TimeoutError

        self.edge_graph = []
        self.adj = [[] for _ in range(self.nodes+1)]
        self.distances = [0 for _ in range(self.nodes+1)]

        if self.key == "RANDOM":
            for vert in range(2, self.nodes+1):
                start = random.randint(1, vert-1)
                length = random.randint(1, self.weight)
                self.adj[start].append((vert, length))
                self.adj[vert].append((start, length))
                if self.weight > 1:
                    self.edge_graph.append((start, vert, length))
                else:
                    self.edge_graph.append((start, vert))
        elif self.key == "LINE":
            for vert in range(2, self.nodes+1):
                if random.randint(1, self.alt) == 1:
                    start = random.randint(1, vert-1)
                else:
                    start = vert-1
                length = random.randint(1, self.weight)
                self.adj[start].append((vert, length))
                self.adj[vert].append((start, length))
                if self.weight > 1:
                    self.edge_graph.append((start, vert, length))
                else:
                    self.edge_graph.append((start, vert))
        elif self.key == "STAR":
            for vert in range(2, self.nodes+1):
                if random.randint(1, self.alt) == 1:
                    start = random.randint(1, vert-1)
                else:
                    start = 1
                length = random.randint(1, self.weight)
                self.adj[vert].append((start, length))
                self.adj[start].append((vert, length))
                if self.weight > 1:
                    self.edge_graph.append((start, vert, length))
                else:
                    self.edge_graph.append((start, vert))

    def __str__(self):
        tree = str(self.nodes)+"\n"
        for nxt in range(self.nodes-1):
            line = ""
            for val in self.edge_graph[nxt]:
                line += str(val)+" "
            line.rstrip()
            tree += line+"\n"
        return tree.rstrip()

    def DFS(self, cur, parent, dist):
        self.distances[cur] = dist
        for nxt in self.adj[cur]:
            if nxt[0] != parent:
                self.DFS(nxt[0], cur, dist + nxt[1])

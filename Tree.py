import random
from PIL import Image, ImageDraw

# tree class
class Tree:

    def __init__(self, params):
        # parameters
        self.nodes = params[0]
        self.weight = params[1]
        self.key = params[2]
        self.alt = params[3]

        if self.nodes > 200:
            raise TimeoutError

        # edge graph, adjacency list, distances list, image
        self.edge_graph = []
        self.adj = [[] for _ in range(self.nodes+1)]
        self.distances = [0 for _ in range(self.nodes+1)]
        self.image = None

        # generate tree based on method
        if self.key == "RANDOM":
            # random tree generation, average depth of log(N)
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
            # generate a line graph
            for vert in range(2, self.nodes+1):
                if random.randint(1, max(self.alt, 1)) == 1:
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
            # generate a star graph
            for vert in range(2, self.nodes+1):
                if random.randint(1, max(self.alt, 1)) == 1:
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

    # output the tree in text
    def __str__(self):
        tree = str(self.nodes)+"\n"
        for nxt in range(self.nodes-1):
            line = ""
            for val in self.edge_graph[nxt]:
                line += str(val)+" "
            line.rstrip()
            tree += line+"\n"
        return tree.rstrip()

    # run depth first search to find distances
    def DFS(self, cur, parent, dist):
        self.distances[cur] = dist
        for nxt in self.adj[cur]:
            if nxt[0] != parent:
                self.DFS(nxt[0], cur, dist + nxt[1])

    # draw the tree out
    def DRAW(self):
        self.image = Image.new("RGB", (400, 400))

        # find the depths of each node
        depth = [0 for _ in range(self.nodes+1)]
        def dfs(cur, par):
            for nxt in self.adj[cur]:
                if nxt[0] != par:
                    depth[nxt[0]] = depth[cur] + 1
                    dfs(nxt[0], cur)
        
        dfs(1, -1)
        mp = dict()
        other = 0
        # count number of nodes per depth
        for i in range(1, self.nodes+1):
            if depth[i] in mp.keys():
                mp[depth[i]] += 1
            else:
                mp[depth[i]] = 1
        cnt = dict()
        for key in mp.keys():
            cnt[key] = mp[key]

        # calculate scale
        high = max(depth)+1
        other = max(mp.values())
        size = 400 // max(high*2+1, other*2+1, 1)
        other = 400 // (other*2+1)
        high = 400 // (high*2+1)

        # draw the tree
        def dfs_draw(cur, par, linexy, wei):

            val = 400 // (cnt[depth[cur]]+1)
            cx, cy = val*mp[depth[cur]], 2*high*depth[cur]+size

            if linexy != None:
                edge = ImageDraw.Draw(self.image)
                edge.line((linexy[0], linexy[1], cx, cy))

                weight = ImageDraw.Draw(self.image)
                weight.text(((linexy[0]+cx)//2, (linexy[1]+cy)//2), str(wei))

            li = len(self.adj[cur])
            if li > 0:
                for i in range(-(li//2), (li+1)//2):
                    if self.adj[cur][i+li//2][0] != par:
                        dfs_draw(self.adj[cur][i+li//2][0], cur, (cx,cy), self.adj[cur][i+li//2][1])
            
            draw = ImageDraw.Draw(self.image)
            draw.ellipse((cx-size//2, cy-size//2,cx+size//2, cy+size//2), "blue", "blue")

            text = ImageDraw.Draw(self.image)
            text.text((cx-5, cy-5), str(cur), (255,255,0))

            mp[depth[cur]] -= 1

        dfs_draw(1, -1, None, -1)

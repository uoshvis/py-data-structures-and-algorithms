from copy import deepcopy
from priority_queues.adaptable_heap_priority_queue import AdaptableHeapPriorityQueue
from priority_queues.heap_priority_queue import HeapPriorityQueue
from partition import Partition


class Graph:
    # ------------------------- nested Vertex class -------------------------
    class Vertex:
        """Lightweight vertex structure for a graph."""
        __slots__ = '_element'

        def __init__(self, x):
            """Do not call constructor directly. Use Graph s insert vertex(x)."""
            self._element = x

        def element(self):
            """Return element associated with this vertex."""
            return self._element

        def __hash__(self):  # will allow vertex to be a map/set key
            return hash(id(self))

    # ------------------------- nested Edge class -------------------------
    class Edge:
        """Lightweight edge structure for a graph."""
        __slots__ = '_origin', '_destination', '_element'

        def __init__(self, u, v, x):
            """Do not call constructor directly. Use Graph s insert edge(u,v,x)."""
            self._origin = u
            self._destination = v
            self._element = x

        def endpoints(self):
            """Return (u,v) tuple for vertices u and v"""
            return self._origin, self._destination

        def opposite(self, v):
            """Return the vertex that is opposite v on this edge."""
            return self._destination if v is self._origin else self._origin

        def element(self):
            return self._element

        def __hash__(self):  # will allow edge to be a map/set key
            return hash((self._origin, self._destination))

    """Representation of a simple graph using an adjacency map."""
    def __init__(self, directed=False):
        """
            Create an empty graph (undirected, by default).
            Graph is directed if optional parameter is set to True.
        """
        self._outgoing = {}
        # only create second map for directed graph; use alias for undirected
        self._incoming = {} if directed else self._outgoing

    def is_directed(self):
        return self._incoming is not self._outgoing # directed if maps are distinct

    def vertex_count(self):
        return len(self._outgoing)

    def vertices(self):
        """Return an iteration of all vertices of the graph."""
        return self._outgoing.keys()

    def edge_count(self):
        """Return the number of edges in the graph."""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        # for undirected graphs, make sure not to double-count edges
        return total if self.is_directed() else total //2

    def edges(self):
        """Return a set of all edges of the graph."""
        result = set()  # avoid double-reporting edges of undirected graph
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())           # add edges to resulting set
        return result

    def get_edge(self, u, v):
        """Return the edge from u to v, or None if not adjacent."""
        return self._outgoing[u].get(v)         # returns None if v not adjacent

    def degree(self, v, outgoing=True):
        """Return number of (outgoing) edges incident to vertex v in the graph.
        If graph is directed, optional parameter used to count incoming edges.
        """
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        """
        Return all (outgoing) edges incident to vertex v in the graph
        If graph is directed, optional parameter used to request incoming edges.
        """
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, x=None):
        """Insert and return a new Vertex with element x."""
        v = self.Vertex(x)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}
        return v

    def insert_edge(self, u, v, x = None):
        """Insert and return a new Edge from u to v with auxiliary element x."""
        e = self.Edge(u, v, x)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e


# --------------------- Graph Traversals ---------------------------------

# Basic depth-first search on a graph, starting at a designated vertex u
def DFS(g, u, discovered):
    """
        Perform DFS of the undiscovered portion of Graph g starting at Vertex u.
        discovered is a dictionary mapping each vertex to the edge that was used to
        discover it during the DFS. (u should be ”discovered” prior to the call.)
        Newly discovered vertices will be added to the dictionary as a result.
    """
    for e in g.incident_edges(u):
        v = e.opposite(u)
        if v not in discovered:    # discovered is dict
            discovered[v] = e
            DFS(g, v, discovered)


def run_DFS():
    g = Graph()
    u = g.insert_vertex()
    # Python dictionary that maps a vertex of the graph to the tree edge
    # that was used to discover that vertex.
    # source vertex u occurs as a key of the dictionary
    # with None as its value.
    result = {u: None}
    DFS(g, u, result)


# Function to reconstruct a directed path from u to
# The function returns an ordered list of vertices on the path.
def construct_path(u, v, discovered):
    path = []
    if v is discovered:
        # we build list from v to u and then reverse it at the end
        path.append(v)
        walk = v
        while walk is not u:
            e = discovered[walk]                # find edge leading to walk
            parent = e.opposite(walk)
            path.append(parent)
            walk = parent
        path.reverse()                          # reorient path from u to v
    return path


# Top-level function that returns a DFS forest for an entire graph
def DFS_complete(g):
    """Perform DFS for entire graph and return forest as a dictionary.
    Result maps each vertex v to the edge that was used to discover it.
    (Vertices that are roots of a DFS tree are mapped to None.)
    """
    forest = {}
    for u in g.vertices():
        if u not in forest:
            forest[u] = None            # u will be the root of a tree
            DFS(g, u, forest)
    return forest


# Breadth-first search
def BFS(g, s, discovered):
    """Perform BFS of the undiscovered portion of Graph g starting at Vertex s.

    discovered is a dictionary mapping each vertex to the edge that was used to
    discover it during the BFS (s should be mapped to None prior to the call).
    Newly discovered vertices will be added to the dictionary as a result.
    """
    level = [s]                                 # first level includes only s
    while len(level) > 0:
        next_level = []                         # prepare to gather newly found vertices
        for u in level:
            for e in g.incident_edges(u):       # for every outgoing edge from u
                v = e.opposite(u)
                if v not in discovered:         # v is an unvisited vertex
                    discovered[v] = e           # e is the tree edge that discovered v
                    next_level.append(v)        # v will be further considered in next pass
        level = next_level                      # relabel ’next’ level to become current


# -------------------------- Transitive Closure --------------------------------------

# Floyd-Warshall
def floyd_warshall(g):
    """Return a new graph that is the transitive closure of g.
    """
    closure = deepcopy(g)
    verts = list(closure.vertices())            # make indexable list
    n = len(verts)
    for k in range(n):
        for i in range(n):
            # verify that edge (i,k) exists in the partial closure
            if i !=k and closure.get_edge(verts[i], verts[k]) is not None:
                for j in range(n):
                    # verify that edge (k,j) exists in the partial closure
                    if i !=j !=k and closure.get_edge(verts[k], verts[j]) is not None:
                        # if (i,j) not yet included, add it to the closure
                        if closure.get_edge(verts[i], verts[j]) is None:
                            closure.insert_edge(verts[i], verts[j])


# ------------------------ Directed Acyclic Graphs ---------------------------

# Topological sorting algorithm
def topological_sort(g):
    """Return a list of verticies of directed acyclic graph g in topological order.
    If graph g has a cycle, the result will be incomplete.
    """
    topo = []                   # a list of vertices placed in topological order
    ready = []                  # list of vertices that have no remaining constraints
    incount = []                # keep track of in-degree for each vertex
    for u in g.vertices():
        incount[u] = g.degree(u, False)     # parameter requests incoming degree
        if incount[u] == 0:                 # if u has no incoming edges,
            ready.append(u)                 # it is free of constraints
    while len(ready) > 0:
        u = ready.pop()                     # u is free of constraints
        topo.append(u)                      # add u to the topological order
        for e in g.incident_edges(u):       # consider all outgoing neighbors of u
            v = e.opposite(u)
            incount[v] -= 1                 # v has one less constraint without u
            if incount[v] == 0:
                ready.append(v)
    return topo


# ------------------------- Shortest Paths ----------------------------------------

# Dijkstra's algorithm
def shortest_path_lengths(g, src):
    """Compute shortest-path distances from src to reachable vertices of g.
    Graph g can be undirected or directed, but must be weighted such that
    e.element() returns a numeric weight for each edge e.

    Return dictionary mapping each reachable vertex to its distance from src.
    """
    d = {}                              # d[v] is upper bound from s to v
    cloud = {}                          # map reachable v to its d[v] value
    pq = AdaptableHeapPriorityQueue()   # vertex v will have key d[v]
    pqlocator = {}                      # map from vertex to its pq locator

    # for each vertex v of the graph, add an entry to the priority queue, with
    # the source having distance 0 and all others having infinite distance
    for v in g.vertices():
        if v is src:
            d[v] = 0
        else:
            d[v] = float('inf')             # syntax for positive infinity
        pqlocator[v] = pq.add(d[v], v)      # save locator for future updates

    while not pq.is_empty():
        key, u = pq.remove_min()
        cloud[u] = key                      # its correct d[u] value
        del pqlocator[u]                    # u is no longer in pq
        for e in g.incident_edges(u):       # outgoing edges (u,v)
            v = e.opposite(u)
            if v not in cloud:
                wgt = e.elemet()
                if d[u] + wgt < d[v]:                   # better path to v?
                    d[v] = d[u] + wgt                   # update the distance
                    pq.update(pqlocator[v], d[v], v)    # update the pq entry
    return cloud                                        # only includes reachable vertices


# reconstruct the shortest path
def shortest_path_tree(g, s, d):
    """Reconstruct shortest-path tree rooted at vertex s, given distance map d.

    Return tree as a map from each reachable vertex v (other than s) to the
    edge e=(u,v) that is used to reach v from its parent u in the tree.
    """
    tree = {}
    for v in d:
        if v is not s:
            for e in g.incident_edges(v, False):            # consider INCOMING edges
                u = e.opposite(v)
                wgt = e.elemet()
                if d[v] == d[u] + wgt:
                    tree[v] = e                             # edge e is used to reach v
    return tree


# -----------------------------Minimum Spanning Trees-----------------------------------

# Prim-Jarnik algorithm
# O((n+m) log n) with heap based priority queue, or O(m log n) for a connected graph
# O(n^2) using unsorted list as priority queue
def MST_PrimJarnik(g):
    """Compute a minimum spanning tree of weighted graph g.

    Return a list of edges that comprise the MST (in arbitrary order).
    """
    d = {}                              # d[v] is bound on distance to tree
    tree = []                           # list of edges in spanning tree
    pq = AdaptableHeapPriorityQueue()   # d[v] maps to value (v, e=(u,v))
    pqlocator = {}                      # map from vertex to its pq locator

    # for each vertex v of the graph, add an entry to the priority queue, with
    # the source having distance 0 and all others having infinite distance

    for v in g.vertices():
        if len(d) == 0:                         # this is the first node
            d[v] = 0                            # make it the root
        else:
            d[v] = float('inf')                 # positive infinity
        pqlocator[v] = pq.add(d[v], (v, None))

    while not pq.is_empty():
        key, value = pq.remove_min()
        u, edge = value                         # unpack tuple from pq
        del pqlocator[u]                        # u is no longer in pq
        if edge is not None:
            tree.append(edge)                   # add edge to tree
        for link in g.incident_edges(u):
            v = link.opposite(u)
            if v in pqlocator:                  # thus v not yet in tree
                # see if edge (u,v) better connects v to the growing tree
                wgt = link.element()
                if wgt < d[v]:                  # better edge to v?
                    d[v] = wgt                  # update the distance
                    pq.update(pqlocator[v], d[v], (v, link))    # update the pq entry


#  Kruskal’s algorithm
#  Running time O(m log n)

def MST_Kruskal(g):
    """Compute a minimum spanning tree of a graph using Kruskal s algorithm.

    Return a list of edges that comprise the MST.
    The elements of the graph s edges are assumed to be weights.
    """
    tree = []                   # list of edges in spanning tree
    pq = HeapPriorityQueue()    # entries are edges in G, with weights as key
    forest = Partition()        # keeps track of forest clusters
    position = {}               # map each node to its Partition entry

    for v in g.vertices():
        position[v] = forest.make_group(v)

    for e in g.edges():
        pq.add(e.elemet(), e)               # edge’s element is assumed to be its weight

    size = g.vertex_count()
    while len(tree) != size - 1 and not pq.is_empty():
        # tree not spanning and unprocessed edges remain
        weight, edge = pq.remove_min()
        u, v = edge.endpoints()
        a = forest.find(position[u])
        b = forest.find(position[v])
        if a != b:
            tree.append(edge)
            forest.union(a, b)

    return tree

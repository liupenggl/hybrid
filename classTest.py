import networkx as nx
import matplotlib.pyplot as plt


class arrc:
    def __init__(self, start=0,step=1):
        self.start=start
        self.step=step
        self.changed={}
    def __getitem__(self,key):

        try:
            return self.changed[key]
        except KeyError:
            return self.start+key*self.step

    def __setitem__(self,key,value):
        self.changed[key]=value

def dfs_edges(G, source=None):
    """Produce edges in a depth-first-search (DFS).

    Parameters
    ----------
    G : NetworkX graph

    source : node, optional
       Specify starting node for depth-first search and return edges in
       the component reachable from source.

    Returns
    -------
    edges: generator
       A generator of edges in the depth-first-search.

    Examples
    --------
    >>> G = nx.Graph()
    >>> G.add_path([0,1,2])
    >>> print(list(nx.dfs_edges(G,0)))
    [(0, 1), (1, 2)]

    Notes
    -----
    Based on http://www.ics.uci.edu/~eppstein/PADS/DFS.py
    by D. Eppstein, July 2004.

    If a source is not specified then a source is chosen arbitrarily and
    repeatedly until all components in the graph are searched.
    """
    if source is None:
        # produce edges for all components
        nodes = G
    else:
        # produce edges for components with source
        nodes = [source]
    visited=set()
    for start in nodes:
        if start in visited:
            continue
        visited.add(start)
        stack = [(start,iter(G[start]))]
        while stack:
            parent,children = stack[-1]
            try:
                child = next(children)
                if child not in visited:
                    yield parent,child
                    visited.add(child)
                    stack.append((child,iter(G[child])))
            except StopIteration:
                stack.pop()


if __name__=="__main__":
    print "main"
    g=nx.generators.small.krackhardt_kite_graph()
    for x,y in dfs_edges(g,9):
        print (x,y)
 
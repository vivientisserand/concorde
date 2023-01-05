import networkx as nx

class Graph():
  
  def __init__(self, edges, directed=False):
        """
        A graph - or network - is a useful data stucture to store relational datasets.
        Actually any matrix can be seen as a graph, think a correlation structure between
        assets for instance. It is thus important being able to leverage such an ubiquitous
        object.
        
        Parameters:
            edges: a list of tuples indicating between which pair of nodes there is a link.
            directed: a boolean stating whether the network is directed or not. Default: False.
        """
        self.edges=edges
        self.directed=directed
        
    


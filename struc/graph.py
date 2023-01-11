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
        self.nodes = list(set([x[0] for x in edges] + [x[1] for x in edges]))
        
  @classmethod
  def from_dataframe(cls, graph_as_df, source=None, target=None, directed=False):
      """
      """
      cols = graph_as_df.columns
      source, target = source if not None else cols[0], target if not None else cols[1]
      assert source in cols and target in cols, "Provide valid source and target names (should be in column names)."
        
      if not directed:
          graph_as_df = graph_as_df[graph_as_df[source] < graph_as_df[target]]
      edges = list(zip(graph_as_df[source], graph_as_df[target]))
      graph = cls(edges, directed)
      return graph
    


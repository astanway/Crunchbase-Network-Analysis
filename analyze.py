import json
import sys
import build
from networkx import *

s = build.founder()
# i = build.investor()

nG = nx.number_of_nodes(nx.connected_component_subgraphs(s)[0])
nodes = nx.number_of_nodes(s)
edges = nx.number_of_edges(s)
print nG
print nodes
print edges
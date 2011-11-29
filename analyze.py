import json
from networkx import *

# NOTE: After building, you MUST add a newline to the gml files for networkx to read them again. Bizarre, I know. 
#       BUT! it's actually MUCH faster to build the graph inline than load it from a gml file, so that's what we'll be doing.

# shared founder graph
def founder():
  f = open("shared_companies.js")
  shared_companies = json.load(f)
  f = open("shared_edges.js")
  shared_edges = json.load(f)

  s = nx.Graph()
  for node in shared_companies.itervalues():
    s.add_node(node['id'], {'startup': node['startup'], 'label': node['label'], 'total': node['total']})

  for edge, item in enumerate(shared_edges):
    s.add_edge(shared_edges[edge]['target'], shared_edges[edge]['source'])

  return s

# directed investments graph
def investor():
  f = open("investment_companies.js")
  investment_companies = json.load(f)
  f = open("investment_edges.js")
  investment_edges = json.load(f)

  i = nx.DiGraph()
  for node in investment_companies.itervalues():
    i.add_node(node['id'], {'startup': node['startup'], 'label': node['label'], 'total': node['total']})

  for edge, item in enumerate(investment_edges):
    i.add_edge(investment_edges[edge]['source'], investment_edges[edge]['target'], value=investment_edges[edge]['value'])
  return i
  
s = founder()

nG = nx.number_of_nodes(nx.connected_component_subgraphs(s)[0])
nodes = nx.number_of_nodes(s)
edges = nx.number_of_edges(s)
print nG
print nodes
print edges


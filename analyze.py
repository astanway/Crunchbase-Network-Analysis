import json
from networkx import *

# shared founder graph
def founder():
  f = open("graphs/shared_companies.js")
  shared_companies = json.load(f)
  f = open("graphs/shared_edges.js")
  shared_edges = json.load(f)

  s = nx.Graph()
  for node in shared_companies.itervalues():
    s.add_node(node['id'], {'startup': node['startup'], 'label': node['label'], 'total': node['total']})

  for edge, item in enumerate(shared_edges):
    s.add_edge(shared_edges[edge]['target'], shared_edges[edge]['source'])

  # Uncomment to write graph to file
  # nx.write_gml(s, "graphs/shared_founders.gml")
  return s

# directed investments graph
def investor():
  f = open("graphs/investment_companies.js")
  investment_companies = json.load(f)
  f = open("graphs/investment_edges.js")
  investment_edges = json.load(f)

  i = nx.DiGraph()
  for node in investment_companies.itervalues():
    i.add_node(node['id'], {'startup': node['startup'], 'label': node['label'], 'total': node['total']})

  for edge, item in enumerate(investment_edges):
    i.add_edge(investment_edges[edge]['source'], investment_edges[edge]['target'], value=investment_edges[edge]['value'])
  
  # Uncomment to write graph to file
  # nx.write_gml(i, "graphs/investments.gml")
  return i
  
s = founder()
i = investor()

nG = nx.number_of_nodes(nx.connected_component_subgraphs(s)[0])
nodes = nx.number_of_nodes(s)
edges = nx.number_of_edges(s)
print nG
print nodes
print edges
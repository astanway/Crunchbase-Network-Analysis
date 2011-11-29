import json
from networkx import *

# json files built by scrape.py
f = open("shared_companies.js")
shared_companies = json.load(f)
f = open("shared_edges.js")
shared_edges = json.load(f)
f = open("investment_companies.js")
investment_companies = json.load(f)
f = open("investment_edges.js")
investment_edges = json.load(f)

# shared founder graph
s = nx.Graph()
for node in shared_companies.itervalues():
  s.add_node(node['id'], {'permalink': node['permalink'], 'label': node['label'], 'total': node['total']})

for edge, item in enumerate(shared_edges):
  s.add_edge(shared_edges[edge]['source'], shared_edges[edge]['target'])

nx.write_gml(s, "shared_founders.gml")

# investments graph
i = nx.Graph()
for node in investment_companies.itervalues():
  i.add_node(node['id'], {'permalink': node['permalink'], 'label': node['label'], 'total': node['total']})

for edge, item in enumerate(investment_edges):
  i.add_edge(investment_edges[edge]['source'], investment_edges[edge]['target'], value=investment_edges[edge]['value'])

nx.write_gml(i, "investments.gml")
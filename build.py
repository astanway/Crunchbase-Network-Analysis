import json
from networkx import *

# NOTE: After building, you MUST add a newline to the gml files for networkx to read them again. Bizarre, I know.

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
  s.add_node(node['id'], {'startup': node['startup'], 'label': node['label'], 'total': node['total']})

for edge, item in enumerate(shared_edges):
  s.add_edge(shared_edges[edge]['target'], shared_edges[edge]['source'])

nx.write_gml(s, "shared_founders.gml")

# directed investments graph
i = nx.DiGraph()
for node in investment_companies.itervalues():
  i.add_node(node['id'], {'startup': node['startup'], 'label': node['label'], 'total': node['total']})

for edge, item in enumerate(investment_edges):
  i.add_edge(investment_edges[edge]['source'], investment_edges[edge]['target'], value=investment_edges[edge]['value'])

nx.write_gml(i, "investments.gml")
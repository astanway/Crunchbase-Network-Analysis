import json
import sys
from networkx import *

#shared founder graph - SHOULD BE NO FIRMS IN THIS ONE.
f = open("shared_companies.js")
shared_companies = json.load(f)
f = open("shared_edges.js")
shared_edges = json.load(f)

s = nx.Graph()
counter = 0
for node, item in shared_companies.items():
  try:
    name=node.encode('latin-1')
    s.add_node(shared_companies[node]['id']) #ADDING ID AS LABEL
  except UnicodeEncodeError:
    counter += 1

    # edge [
    #   source 74527
    #   target 74527
    # ] THE FUCK
for edge, item in enumerate(shared_edges):
  s.add_edge(shared_edges[edge]['source'], shared_edges[edge]['target'])

print counter
print nx.number_of_nodes(s)
print nx.number_of_edges(s)

nx.write_gml(s, "shared_founders.gml")

#investments graph
f = open("investment_companies.js")
investment_companies = json.load(f)
f = open("investment_edges.js")
investment_edges = json.load(f)

counter = 0
i = nx.Graph()
for node, item in investment_companies.items():
  try:
    name=node.encode('latin-1')
    i.add_node(investment_companies[node]['id'])
  except UnicodeEncodeError:
    counter += 1

for edge, item in enumerate(investment_edges):
  i.add_edge(investment_edges[edge]['source'], investment_edges[edge]['target'], value=investment_edges[edge]['value'])

print counter
print nx.number_of_nodes(i)
print nx.number_of_edges(i)


nx.write_gml(i, "investments.gml")
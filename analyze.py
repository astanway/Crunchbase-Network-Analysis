from networkx import *
from numpy import *
import json
import sys
import build
import operator
import matplotlib.pyplot as plt
import matplotlib
import simplejson
import pickle
from decimal import *

G = build.investor()
H = weakly_connected_component_subgraphs(G)[0]
pr = pagerank_numpy(H)
hub,auth = hits_numpy(H)

p = sorted(pr.iteritems(), key=operator.itemgetter(1), reverse=True)
h = sorted(hub.iteritems(), key=operator.itemgetter(1), reverse=True)
a = sorted(auth.iteritems(), key=operator.itemgetter(1), reverse=True)

# p = pickle.load(open('p.p', 'rb'))
# a = pickle.load(open('a.p', 'rb'))
# h = pickle.load(open('h.p', 'rb'))

names = get_node_attributes(G, 'label')
status = get_node_attributes(G, 'startup')
total = get_node_attributes(G, 'total')

# Pagerank vs. Total Raised
prtotal = []
prscore = []
for node in p:
  prtotal.append(total[node[0]])
  prscore.append(node[1])

plt.plot(prscore, prtotal, "go")
plt.title("Pagerank vs. Total Raised")
plt.ylabel("Total Raised")
plt.xlabel("Page Rank")
plt.savefig('pr.png')
plt.clf()

# Authority Score vs. Total Raised Top 100
atotal = []
ascore = []
counter = 0
for node in a:
  print counter
  if counter == 100:
    break
  atotal.append(total[node[0]])
  ascore.append(node[1])
  counter += 1

plt.plot(ascore, atotal, "go")
plt.title("Authority Score vs. Total Raised Top 100")
plt.ylabel("Total Raised")
plt.xlabel("Authority Score")
plt.savefig('realauthtop100.png')
plt.clf()

# founder graph centrality
G = build.founder()
status = get_node_attributes(G, 'startup')
total = get_node_attributes(G, 'total')
label = get_node_attributes(G, 'label')
dc = nx.degree_centrality(G)
dc = sorted(dc.iteritems(), key=operator.itemgetter(1))
total_raised = []
dc_measure = []
for node, value in dc:
  if value > 0:
    total_raised.append(total[node])
    dc_measure.append(value)

plt.plot(dc_measure, total_raised, "go")
plt.title("Degree Centrality vs. Total Raised")
plt.ylabel("Total Raised")
plt.xlabel("Degree Centrality")
plt.savefig('deg_centrality.png')
plt.clf()

# Nodes in Component vs. Max Raised per Component
size = []
avg = []
for component in nx.connected_component_subgraphs(G):
  comp_total = 0
  if len(component) > 1:
    for node in component.nodes():
      try:
        if comp_total < total[node]:
          comp_total = total[node]
        avg.append(comp_total)
        size.append(len(component))
      except KeyError:
        pass

plt.plot(size, avg, "go")
plt.title("Nodes in Component vs. Max Raised per Component")
plt.ylabel("Max Raised")
plt.xlabel("Nodes")
plt.savefig('component_max.png')
plt.clf()

# Nodes in Component vs. Avg Raised per Node
size = []
avg = []
for component in nx.connected_component_subgraphs(G):
  comp_total = 0
  nodes_in_component = len(component)
  if nodes_in_component > 1:
    for node in component.nodes():
      try:
        comp_total += total[node]
      except KeyError:
        pass
    size.append(nodes_in_component)
    avg.append(comp_total / nodes_in_component)
        

plt.plot(size, avg, "go")
plt.title("Nodes in Component vs. Avg Raised per Node")
plt.ylabel("Avg Raised")
plt.xlabel("Nodes")
plt.savefig('component_total.png')
plt.clf()

# total investor birds eye graph
graph = build.investor()
G = weakly_connected_component_subgraphs(graph)[0]
status = get_node_attributes(G, 'startup')
label = get_node_attributes(G, 'label')
for node, degree in G.out_degree_iter():
  if 0 < degree < 40 and status[node] == 0:
    G.remove_node(node)
  try:
    if status[node] == 1 and len(G.out_edges(node)) > 10:
      G.node[node]['startup'] = 0
      print G.node[node]
  except NetworkXError:
    pass

for node, degree in G.in_degree_iter():
  if 1 <= degree < 5:
    G.remove_node(node) 


#Proximity to Node with High Centrality
G = build.founder() 
G = connected_component_subgraphs(G)[0]
cl = closeness_centrality(G)
cl = sorted(cl.iteritems(), key=operator.itemgetter(1), reverse=True)
names = get_node_attributes(G, 'label')
total = get_node_attributes(G, 'total')
sort = {}
for node in cl:
  try:
    sort[names[node[0]]] = total[node[0]]
  except IndexError:
    pass

sort = sorted(sort.iteritems(), key=operator.itemgetter(1), reverse=True)

for node in sort:
  print node[0] + " " + repr(node[1] / 4671750000 * 2)
  
for component in nx.connected_component_subgraphs(G):
  comp_total = 0
  nodes_in_component = len(component)
  if nodes_in_component > 1:
    for node in component.nodes():
      try:
        comp_total += total[node]
      except KeyError:
        pass
    size.append(nodes_in_component)
    avg.append(comp_total / nodes_in_component)
        

plt.plot(size, avg, "go")
plt.ylabel("Total Raised")
plt.xlabel("Proximity to Node with High Centrality")
plt.savefig('centrality_graph_totals.png')
plt.clf()


#Percentage of nodes with well-funded neighbors
graph = build.founder()
x = connected_component_subgraphs(graph)
x.reverse()
allnum = []
size = []

for G in x:
  if len(G) == 1:
    continue
  nodes = G.nodes()
  names = get_node_attributes(G, 'label')
  total = get_node_attributes(G, 'total')
  sort = {}
  for node in G:
    try:
      sort[node] = G.node[node]['total']
    except KeyError:
      pass

  sort = sorted(sort.iteritems(), key=operator.itemgetter(0), reverse=True)

  denom = 0
  numb = 0
  for node in sort:
    if node[1] > 0:
      denom += 1
      for neighbor in G.neighbors(node[0]):
        if G.node[neighbor]['total'] > 0:
          numb += 1
    G.remove_node(node[0])
  if denom > 0:
    print repr(numb) +  "/" + repr(denom)
    final = Decimal(numb) / Decimal(denom)
    print final
    print len(nodes)
    allnum.append(final)
    size.append(len(nodes))

plt.plot(size, allnum, "go")
plt.xlabel("Size of Component")
plt.ylabel("Percentage of nodes with well-funded neighbors")
plt.savefig('size_vs_percentage.png')
plt.clf()
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

G = build.investor()
H = weakly_connected_component_subgraphs(G)[0]
pr = pagerank_numpy(H)
hub,auth = hits_numpy(H)

p = sorted(pr.iteritems(), key=operator.itemgetter(1), reverse=True)
h = sorted(hub.iteritems(), key=operator.itemgetter(1), reverse=True)
a = sorted(auth.iteritems(), key=operator.itemgetter(1), reverse=True)

p = pickle.load(open('p.p', 'rb'))
a = pickle.load(open('a.p', 'rb'))
h = pickle.load(open('h.p', 'rb'))

names = get_node_attributes(G, 'label')
status = get_node_attributes(G, 'startup')
total = get_node_attributes(G, 'total')

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
plt.savefig('badassauthtop100.png')
plt.clf()

# G = build.founder()

# http://www.cs.cmu.edu/~christos/PUBLICATIONS/kdd04-cross-assoc.pdf
# http://web.cs.dal.ca/~zyu/research/presentation/presentation.pdf
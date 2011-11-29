from networkx import *
import matplotlib
import matplotlib.pyplot as plt
from operator import itemgetter

f = open('investments.gml', 'r')
gml = f.read()
gml = gml.split('\n')[1:]
G = parse_gml(gml)
print "parsed"
 
nG = nx.number_of_nodes(nx.connected_component_subgraphs(G)[0])
nodes = nx.number_of_nodes(G)
edges = nx.number_of_edges(G)
print nodes
print edges

f = open('shared_founders.gml', 'r')
gml = f.read()
gml = gml.split('\n')[1:]
G = parse_gml(gml)
print "parsed"
 
nG = nx.number_of_nodes(nx.connected_component_subgraphs(G)[0])
nodes = nx.number_of_nodes(G)
edges = nx.number_of_edges(G)
print nodes
print edges
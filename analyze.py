from networkx import *
from numpy import *
import json
import sys
import build
import heapq
import operator

G = build.investor()
H = weakly_connected_component_subgraphs(G)[0]
pr = pagerank_numpy(H) # PageRank
hub,auth = hits_numpy(H) # Hits

p = heapq.nlargest(10, pr.iteritems(), operator.itemgetter(1))
h = heapq.nlargest(10, hub.iteritems(), operator.itemgetter(1))
a = heapq.nlargest(10, auth.iteritems(), operator.itemgetter(1))
print("\nTop-10 PageRank: (ID, PR-Value)")
print p
print("\n Top-10 Hubs: (ID, H-Value)")
print h
print("\n Top-10 Authorities: (ID, A-Value)")
print a

# Top-10 PageRank: (ID, PR-Value)
# [(19344, 0.00091745215190350369), (48255, 0.00068959315651957135), (48113, 0.00063096717351094787), (65542, 0.00062847024624734392), (62905, 0.00056682535022918319), (62385, 0.00055949909908265298), (21338, 0.00048970894830228885), (9369, 0.00047580070922522831), (25375, 0.00046691356677469934), (35458, 0.00045219752661437059)]
# 
#  Top-10 Hubs: (ID, H-Value)
# [(32088, (0.032286959138363006-0j)), (80093, (0.025158279497257179-0j)), (78912, (0.021449937886884162-0j)), (74913, (0.020467325996906455-0j)), (78149, (0.018560215849025657-0j)), (76606, (0.016771872201963241-0j)), (76434, (0.013088010172606796-0j)), (7057, (0.01118987006949849-0j)), (77000, (0.010053582952540026-0j)), (77378, (0.0078236718060255925-0j))]
# 
#  Top-10 Authorities: (ID, A-Value)
# [(73161, (0.0016245528145705367+0j)), (18571, (0.0014238830573720476+0j)), (27551, (0.0014188239949129327+0j)), (17518, (0.001417857886138381+0j)), (47570, (0.0013414336558649942+0j)), (10919, (0.0013166006500739662+0j)), (60631, (0.0013148324838315971+0j)), (74011, (0.0013111226468559153+0j)), (10753, (0.001259643285298924+0j)), (51334, (0.0012427092116801687+0j))]
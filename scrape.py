import json
import sys
import simplejson
import os
from pprint import pprint
from copy import deepcopy

investment_edges = []
investment_companies = {}
shared_edges = []
shared_companies = {}

id = 1

# companies
path = 'companies/'
listing = os.listdir(path)
for infile in listing:
  try:
    json_data=open(path + infile)
    data = json.load(json_data)
    node = {}
    node['label'] = 1
    node['id'] = id
    shared_companies[data['name']] = node
    investment_companies[data['name']] = node
    json_data.close()
    id += 1

  except ValueError:
    print infile + " is a douche company"
    
filename = "shared_companies.js"
data = simplejson.dumps(shared_companies)
FILE = open(filename,"w")
FILE.writelines(data)
FILE.close()

  
#connect shared founders
path = 'people/'
listing = os.listdir(path)
for infile in listing:
  try:
    json_data=open(path + infile)
    data = json.load(json_data)
    shared = []
    for x, item in enumerate(data['relationships']):
      if data['relationships'][x]['title'].lower().rfind("ceo") != -1 or data['relationships'][x]['title'].lower().rfind("founder") != 1:
        try:
          company = shared_companies[data['relationships'][x]['firm']['name']]
          shared.append(company)        
        except KeyError:
          print data['relationships'][x]['firm']['name'] + " is a douche company"
              
    for x, item in enumerate(shared):
      for i, item in enumerate(shared):
        if shared[i]['id'] == id or x == i:
          continue
        edge = {}
        edge['type'] = 'edge'
        edge['source'] = shared[x]['id']
        edge['target'] = shared[i]['id']
        shared_edges.append(edge)
  except ValueError:
    print "Company does not exist"


#investors
path = 'financial-organizations/'
listing = os.listdir(path)
for infile in listing:
  try:
    json_data=open(path + infile)
    data = json.load(json_data)
    try:
      firm = {}
      firm['label'] = 0
      firm['id'] = id
      investment_companies[data['name']] = firm
    
      id += 1

      if len(data['relationships']) == 0:
        continue
      
      #connect firm to startup
      for z, item in enumerate(data['investments']):
        try:
          company = investment_companies[data['investments'][z]['funding_round']['company']['name']]
          amount = data['investments'][z]['funding_round']['raised_amount']
        
          if amount == None:
            continue
      
          edge = {}
          edge['source'] = firm['id']
          edge['target'] = company['id']
          edge['value'] = amount
          investment_edges.append(edge)
        except KeyError:
          data['investments'][z]['funding_round']['company']['name'] + "is a shitty investment"
      
      json_data.close()
    except ValueError:
      print infile + " is a douche firm"
  except ValueError:
    print infile + " is really a douche firm"


filename = "investment_edges.js"
data = simplejson.dumps(investment_edges)
FILE = open(filename,"w")
FILE.writelines(data)
FILE.close()

filename = "shared_edges.js"
data = simplejson.dumps(shared_edges)
FILE = open(filename,"w")
FILE.writelines(data)
FILE.close()

filename = "investment_companies.js"
data = simplejson.dumps(investment_companies)
FILE = open(filename,"w")
FILE.writelines(data)
FILE.close()







 
# # filename = "founderEdges.js"
# # data = simplejson.dumps(founderEdges)
# # FILE = open(filename,"w")
# # FILE.writelines(data)
# # FILE.close()
# 
# # filename = "allpeople.js"
# # data = simplejson.dumps(people)
# # FILE = open(filename,"w")
# # FILE.writelines(data)
# # FILE.close()
# 
# 
# # companies
# # json_people = open("allpeople.js")
# # people = json.load(json_people)
# 
# # for x in data['relationships']:
# #   name = x['person']['first_name'] + " " + x['person']['last_name']
# #   try:
# #     node = people[name]
# #     node['investor'] = True
# #     if node.has_key('firms'):
# #        node['firms'] += " " + data['name']
# #     else:
# #        node['firms'] = data['name']
# #     members.append(node)
# #   except KeyError:
# #     print name + " is a douche investor"
# 
# # for x, item in enumerate(members):
# 
#   #connect investor to partners
#   # for i, item in enumerate(members):
#   #   if members[i]['id'] == id or x == i:
#   #     continue
#   #   edge = {}
#   #   edge['type'] = 'edge'
#   #   edge['source'] = members[x]['id']
#   #   edge['target'] = members[i]['id']
#   #   edges.append(edge)
# 
# 
#   #verify that we're cookin!
# 
#   #angel investments
# 
# 
# 
# 
# 
# 
# 
#     # graph = open("graph.gml","w")
#     # 
#     # graph.write("node[\n")
#     # graph.write(email)
#     # graph.write("\n]")
#     #   
#     # graph.close()
# 
# 
#   # filename = "edges.js"
#   # data = simplejson.dumps(edges)
#   # FILE = open(filename,"w")
#   # FILE.writelines(data)
#   # FILE.close()
#   # 
#   # filename = "people.js"
#   # data = simplejson.dumps(people)
#   # FILE = open(filename,"w")
#   # FILE.writelines(data)
#   # FILE.close()


# f = open("shared_companies.js")
# shared_companies = json.load(f)
# f = open("shared_edges.js")
# shared_edges = json.load(f)
# f = open("investment_companies.js")
# investment_companies = json.load(f)
# f = open("investment_edges.js")
# investment_edges = json.load(f)
# 
# #shared founder graph
# gml = "graph [\n"
# gml += "  directed 0\n"
# 
# for node, item in (shared_companies.items()):
#   gml += "  node [\n"
#   gml += "    id " + str(shared_companies[node]['id']) + "\n"
#   gml += "  ]\n"
# 
# 
# for edge, item in enumerate(shared_edges):
#   gml += "  edge [\n"
#   gml += "    source " + str(shared_edges[edge]['source']) + "\n"
#   gml += "    target " + str(shared_edges[edge]['target']) + "\n"
#   # if people[edge]['value']:
#   #   gml += "    value " + str(people[edge]['value']) + "\n"
#   gml += "  ]\n"
# 
# gml += "]\n"
# 
# filename = "graph.gml"
# FILE = open(filename,"w")
# FILE.writelines(gml)
# FILE.close()

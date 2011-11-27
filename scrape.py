import json
import sys
import simplejson
import os
from pprint import pprint

# edges = []
# people = {}
# companies = {}
# id = 1
# 
# #people
# # path = 'people/'
# # listing = os.listdir(path)
# # for infile in listing:
# #   try:
# #     json_data=open(path + infile)
# #     data = json.load(json_data)  
# #     name = data['first_name'] + " " + data['last_name']
# #     node = {}
# #     node['type'] = 'node'
# #     node['id'] = id
# #     node['name'] = name
# #     if len(data['investments']) > 0:
# #       node['investor'] = True
# #     people[name] = node
# #     id += 1
# #     json_data.close()
# #   except ValueError:
# #     print infile + " is a douche"
# 
# json_people = open("allpeople.js")
# people = json.load(json_people)
# 
# #founders
# path = 'companies/'
# listing = os.listdir(path)
# for infile in listing:
#   try:
#     json_data=open(path + infile)
#     data = json.load(json_data)
#     members = []
# 
#     if len(data['relationships']) == 0:
#       continue
# 
#     for x in data['relationships']:
#       name = x['person']['first_name'] + " " + x['person']['last_name']
#       try:
#         node = people[name]
#         node['founder'] = True #they aren't actually all founders, but that's okay
#         if node.has_key('companies'):
#            node['companies'] += " " + data['name']
#         else:
#            node['companies'] = data['name']
#         members.append(node)
#       except KeyError:
#         print name + " is a douche founder"
# 
#     #network dilution
#     company = {}
#     company['dilution'] = len(members)
#     company['members'] = members
#     companies[data['name']] = company
#   
#     #connect the founders to each other
#     # for x, item in enumerate(members):
#     #   for i, item in enumerate(members):
#     #     if members[i]['id'] == id or x == i:
#     #       continue
#     #     edge = {}
#     #     edge['type'] = 'edge'
#     #     edge['source'] = members[x]['id']
#     #     edge['target'] = members[i]['id']
#     #     edges.append(edge)
# 
#     json_data.close()
#   except ValueError:
#     print infile + " is a douche company"
# 
# filename = "foundercompanies.js"
# data = simplejson.dumps(companies)
# FILE = open(filename,"w")
# FILE.writelines(data)
# FILE.close()
# 
# json_people = open("foundercompanies.js")
# companies = json.load(json_people)

#investors
path = 'financial-organizations/'
listing = os.listdir(path)
for infile in listing:
  try:
    json_data=open(path + infile)
    data = json.load(json_data)
    members = []

    if len(data['relationships']) == 0:
      continue

    for x in data['relationships']:
      name = x['person']['first_name'] + " " + x['person']['last_name']
      try:
        node = people[name]
        node['investor'] = True
        if node.has_key('firms'):
           node['firms'] += " " + data['name']
        else:
           node['firms'] = data['name']
        members.append(node)
      except KeyError:
        print name + " is a douche investor"
  
    # for x, item in enumerate(members):

      #connect investor to partners
      # for i, item in enumerate(members):
      #   if members[i]['id'] == id or x == i:
      #     continue
      #   edge = {}
      #   edge['type'] = 'edge'
      #   edge['source'] = members[x]['id']
      #   edge['target'] = members[i]['id']
      #   edges.append(edge)
      
    #connect firm to founders
    for z, item in enumerate(data['investments']):
      try:
        company = companies[data['investments'][z]['funding_round']['company']['name']]
        amount = data['investments'][z]['funding_round']['raised_amount']
        num_founders = company['dilution']
        num_investors = len(members)
        
        if amount == None:
          continue
      
        for i, item in enumerate(company['members']):
          edge = {}
          edge['type'] = 'edge'
          edge['source'] = members[x]['id']
          edge['target'] = company['members'][i]['id']
          edge['value'] = amount / (num_founders * num_investors)
          edges.append(edge)
      except KeyError:
        data['investments'][z]['funding_round']['company']['name'] + "is a shitty investment"
      
    json_data.close()
  except ValueError:
    print infile + " is a douche firm"

#verify that we're cookin!

#angel investments







  # graph = open("graph.gml","w")
  # 
  # graph.write("node[\n")
  # graph.write(email)
  # graph.write("\n]")
  #   
  # graph.close()


# filename = "edges.js"
# data = simplejson.dumps(edges)
# FILE = open(filename,"w")
# FILE.writelines(data)
# FILE.close()
# 
# filename = "people.js"
# data = simplejson.dumps(people)
# FILE = open(filename,"w")
# FILE.writelines(data)
# FILE.close()

json_people = open("edges.js")
people = json.load(json_people)
gml = ""

for edge, item in enumerate(people):
  gml += "\n  edge ["
  gml += "\n    source " + str(people[edge]['source'])
  gml += "\n    target " + str(people[edge]['target'])
  if people[edge]['value']:
    gml += "\n    value " + str(people[edge]['value'])
  gml += "\n  ]"

filename = "edges.gml"
FILE = open(filename,"w")
FILE.writelines(gml)
FILE.close()

# filename = "founderEdges.js"
# data = simplejson.dumps(founderEdges)
# FILE = open(filename,"w")
# FILE.writelines(data)
# FILE.close()

# filename = "allpeople.js"
# data = simplejson.dumps(people)
# FILE = open(filename,"w")
# FILE.writelines(data)
# FILE.close()


# companies
# json_people = open("allpeople.js")
# people = json.load(json_people)
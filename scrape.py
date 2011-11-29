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

id = 0 # get rid of this

# add company nodes first so the ids match across the two graphs
path = 'companies/'
listing = os.listdir(path)
for infile in listing:
  try:
    json_data=open(path + infile)
    data = json.load(json_data)
    node = {}
    node['label'] = 1
    node['id'] = id
    node['permalink'] = data['permalink']
    node['total'] = 0
    shared_companies[data['permalink']] = node
    investment_companies[data['permalink']] = node
    json_data.close()
    id += 1

  except ValueError:
    print infile

#add investor nodes
path = 'financial-organizations/'
listing = os.listdir(path)
for infile in listing:
  json_data=open(path + infile)
  data = json.load(json_data)

  firm = {}
  firm['label'] = 0
  firm['id'] = id
  firm['permalink'] = data['permalink']
  firm['total'] = 0
  investment_companies[data['permalink']] = firm
  id += 1
  
# add angel investors to firm list
path = 'people/'
listing = os.listdir(path)
for infile in listing:
  try:
    json_data=open(path + infile)
    data = json.load(json_data)

    if len(data['investments']) == 0:
      continue

    angel = {}
    angel['label'] = 0
    angel['id'] = id
    angel['permalink'] = data['permalink']
    angel['total'] = 0
    investment_companies[data['permalink']] = angel
    id += 1
    
    print angel['name']

  except KeyError:
    print infile


# connect companies with investors
for data in shared_companies:
  if len(data['funding_rounds']) == 0:
    continue
  
  for z, item in enumerate(data['funding_rounds']):
    try:
      company = investment_companies[data['investments'][z]['funding_round']['company']['name']]
      amount = data['investments'][z]['funding_round']['raised_amount']
  
      if amount == None:
        continue
  
      edge = {}
      edge['source'] = firm['id']
      edge['target'] = company['id']
      edge['value'] = amount
  
      #add to the respective funding totals
      company['total'] += amount
      firm['total'] += amount
  
      investment_edges.append(edge)
  
      json_data.close()
  
    except KeyError:
      print data['investments'][z]['funding_round']['company']['name']

  
# connect shared founders
path = 'people/'
listing = os.listdir(path)
for infile in listing:
  try:
    json_data=open(path + infile)
    data = json.load(json_data)
    shared = []
    for x, item in enumerate(data['relationships']):
      if data['relationships'][x]['title'].lower().rfind("ceo") != -1 or data['relationships'][x]['title'].lower().rfind("founder") != -1 or data['relationships'][x]['title'].lower().rfind("creator") != -1:
        try:
          company = shared_companies[data['relationships'][x]['firm']['name']]
          shared.append(company)        
        except KeyError:
          continue # catches all the investment firms
            
    for x, item in enumerate(shared):
      for i, item2 in enumerate(shared):
        if shared[i]['id'] == shared[x]['id'] or x == i:
          continue
        edge = {}
        edge['type'] = 'edge'
        edge['source'] = shared[x]['id']
        edge['target'] = shared[i]['id']
        shared_edges.append(edge)
  except ValueError:
    print infile


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

filename = "shared_companies.js"
data = simplejson.dumps(shared_companies)
FILE = open(filename,"w")
FILE.writelines(data)
FILE.close()
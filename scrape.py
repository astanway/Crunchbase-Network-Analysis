import sys
import os
import json
import simplejson

investment_edges = []
investment_companies = {}
shared_edges = []
shared_companies = {}

id = 0 # get rid of this

json_data=open('shared_companies.js')
investment_companies = json.load(json_data)

json_data=open('shared_companies.js')
shared_companies = json.load(json_data)


# add company nodes first so the ids match across the two graphs
path = 'companies/'
listing = os.listdir(path)
for infile in listing:
  try:
    json_data = open(path + infile)
    data = json.load(json_data)
    company = {}
    company['label'] = 1
    company['id'] = id
    company['permalink'] = data['permalink']
    company['total'] = 0
    shared_companies[data['permalink']] = company
    investment_companies[data['permalink']] = company
    json_data.close()
    id += 1

  except ValueError:
    pass

#add investor nodes
path = 'financial-organizations/'
listing = os.listdir(path)
for infile in listing:
  try:
    json_data = open(path + infile)
    data = json.load(json_data)
    
    #make sure it isn't a company investing in another company
    if not data['permalink'] in shared_companies:    
      firm = {}
      firm['label'] = 0
      firm['id'] = id
      firm['permalink'] = data['permalink']
      firm['total'] = 0
      investment_companies[data['permalink']] = firm
      json_data.close()
      id += 1

  except ValueError:
    pass
  
# add angel investors to firm list
path = 'people/'
listing = os.listdir(path)
for infile in listing:
  try:
    json_data = open(path + infile)
    data = json.load(json_data)

    if len(data['investments']) == 0:
      continue

    angel = {}
    angel['label'] = 0
    angel['id'] = id
    angel['permalink'] = data['permalink']
    angel['total'] = 0
    investment_companies[data['permalink']] = angel
    json_data.close()
    id += 1

  except ValueError:
    pass

# connect companies with investors
path = 'companies/'
listing = os.listdir(path)
for infile in listing:
  try:
    json_data = open(path + infile)
    company = json.load(json_data)
    
    if not 'funding_rounds' in company:
      continue
  
    for funding_round in company['funding_rounds']:

      # dirty data yo
      if not funding_round['raised_amount'] or len(funding_round['investments']) == 0:
        continue

      # add the totals to the startups for each graph
      shared_companies[company['permalink']]['total'] += funding_round['raised_amount']
      investment_companies[company['permalink']]['total'] += funding_round['raised_amount']
      
      # make sure the ids are consistent
      if shared_companies[company['permalink']]['id'] != investment_companies[company['permalink']]['id']:
        print company['permalink']

      dilution = funding_round['raised_amount'] / len(funding_round['investments'])  

      for investor in funding_round['investments']:
        try:
          if investor['company'] != None:
            firm = investment_companies[investor['company']['permalink']]
          elif investor['financial_org'] != None:
            firm = investment_companies[investor['financial_org']['permalink']]
          elif investor['person'] != None:
            firm = investment_companies[investor['person']['permalink']]
        except KeyError:
          pass

        #add to the funding total for the firm
        firm['total'] += dilution

        edge = {}
        edge['source'] = firm['id']
        edge['target'] = shared_companies[company['permalink']]['id']
        edge['value'] = dilution
        investment_edges.append(edge)
  
  except ValueError:
    pass


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

        # catches people that have founded or ceo'd an investment firm, aot a startup
        except KeyError:
          continue
            
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
    pass


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
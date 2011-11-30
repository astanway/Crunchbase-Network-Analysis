###### What's going on?
This is the Crunchbase data dump, circa October 2011. Included are two graphs: investments.gml and shared_founders.gml. The former is a bipartite, directed graph connecting firms/angels to startups, where all edges represent the amount of money invested. The latter is an undirected graph where nodes are startups and edges represent a shared co-founder.

## Data
All data was scraped from Crunchbase using the
[crunchbase_search project](https://github.com/dbasch/crunchbase_search). It is then compiled into JSON graphs which are then fed into Networkx for super-sweet-analysis. Also, it turns out building to GML and then reading it back in is heinously slow. So, for all analysis, I don't actually use the GML files - I just use all my downloaded Crunchbase files and build the graph inline.

## Analysis
Stay tuned, fool.

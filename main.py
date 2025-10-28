import pandas as pd
import suggests
from time import gmtime, strftime
from time import sleep


def main():
    #queries = ['jobs near me', 'careers in', 'jobs hiring']


    city_list = pd.read_csv("USA City Locs.csv")
    loc_query_tails = city_list['City State Query'].to_list()

    ## Adding in a few test queries just to test a smaller sample
    loc_query_tails = ['Kirbyville Missouri', 'Warsaw Kentucky', 'Yakima Washington']

       
    ## Iterating through each seed query, assigning a variable to the seed
    for seed in loc_query_tails:
        print (f"🔍🐛🗺️ | Searching in {seed}")
        ## generating holder items:
        location_pulls = []
        location_suggests = []

        ## Structuring the Query
        base_query = "jobs in "
        query = base_query + seed.lower()
        
        ## generating the suggests item
        s = suggests.get_suggests(query, source='google')
        suggestion = {seed:s['suggests']}
        location_suggests.append(suggestion)
        ## generating the tree from the suggests item
        tree = suggests.get_suggests_tree(query,source='google')

        ## generating edges from the tree
        edges = suggests.to_edgelist(tree)

        ## generating the parents from the edges
        parents = suggests.add_parent_nodes(edges)
        location_pulls.append(parents)

        ## Saving the SEAPs
        df = pd.concat(location_pulls)
        df.to_csv(f'seap-data/{seed}-autocomplete.csv')
        ## sleeping
        sleep(1.5)




if __name__=="__main__":
    main()

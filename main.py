import pandas as pd
import suggests
import time


def main():
    #queries = ['jobs near me', 'careers in', 'jobs hiring']


    city_list = pd.read_csv("USA City Locs.csv")
    loc_query_tails = city_list['City State Query'].to_list()

    ''' CREATING A TIMER FOR GITHUB ACTIONS ''' 
    max_duration = 19800 ## 5.5 hours
    ##max_duration = 600 ## testing 10 minutes
    start_time = time.time()

       
    ## Iterating through each seed query, assigning a variable to the seed
    for seed in loc_query_tails[258:]:
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
        time.sleep(1.5)

        ## Checking time elapsed
        if time.time() - start_time > max_duration:
            print ("\n\n\n⏰ Time to Restart the Action")
            print (f"Stopped Location: {seed}")
            break




if __name__=="__main__":
    main()

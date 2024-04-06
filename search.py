import pprint as pp

def search_titleTxt(client, index_name, qtxt):
    query_bm25 = {
        'size': 5,
        '_source': ['title', 'description'],
        'query': {
            'multi_match': {
            'query': qtxt,
            'fields': ['title']  
            }
        }
    }
    client_search(client, index_name, query_bm25)


def search_titleTxt_terms(client, index_name, qtxt):
    query_bm25 = {
        'size': 5,
        '_source': ['title', 'description'],
        'query': {
            'term': {
                'description': qtxt
            }
        }
    }
    client_search(client, index_name, query_bm25)

def search_titleTotalTime(client, index_name, qtxt):
    query_bm25 = {
        'size': 5,
        '_source': ['title', 'duration'],
        'query': {
            'multi_match': {
            'query': qtxt,
            'fields': ['title']  ,
            'operator': 'and'  # Require all terms to match
            }
        }
    }
    client_search(client, index_name, query_bm25)

def search_recipeByTime(client, index_name, qtxt):
    query_bm25 = {
        'size': 5,
        '_source': ['title', 'duration'],
        'query': {
            'range': {
                'duration': {
                    'lte': qtxt
                }
            }
        }
    }
    client_search(client, index_name, query_bm25)




def search_titleIngredients_bool(client, index_name, qtxt):
    query_bm25 = {
        "size": 5,
        "_source": ["title", "ingredients"],
        "query": {
            "bool": {
                "must": [
                {
                        "match": {
                        "description": qtxt,
                        }   
                }
                ],
                "should": [
                {
                    "multi_match": {
                        "query": qtxt,
                        "fields": ["title", "description"]
                    }
                }
                ]
            }
        }
    }
    client_search(client, index_name, query_bm25)





def search_titleEmbedding(client, index_name, emb_query):
    query_denc = {
        'size': 5,
        '_source': ['title', 'description'],
        "query": {
            "knn": {
                "title_embedding": {
                    "vector": emb_query[0].numpy(),
                    "k": 2
                } 
            }
        }
    }
    client_search(client, index_name, query_denc)





#auxiliar method

def client_search(client, index_name, query):
    response = client.search(
        body = query,
        index = index_name
    )
    print('\nSearch results:')
    pp.pprint(response) 



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

def search_titleIngredients_bool(client, index_name, qtxt):
    query_bm25 = {
        "size": 5,
        "_source": ["title", "ingredients"],
        "query": {
            "bool": {
                "must": [
                {
                        "match": {
                        "description": "chicken marsala"
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


#auxiliar method

def client_search(client, index_name, query):
    response = client.search(
        body = query,
        index = index_name
    )
    print('\nSearch results:')
    pp.pprint(response) 



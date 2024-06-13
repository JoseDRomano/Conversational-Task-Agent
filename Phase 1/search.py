import pprint as pp
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

# Function to search for a title based on text query
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
    client_search(client, index_name, query_bm25,"title")

# Function to search for a title based on terms
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
    client_search(client, index_name, query_bm25,"term")

# Function to search for a title based on total time
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
    client_search(client, index_name, query_bm25,"time")

# Function to search for a recipe based on time constraint
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
    client_search(client, index_name, query_bm25,"time")

# Function to search for a title based on ingredients using boolean logic
def search_titleIngredients_bool(client, index_name, qtxt):
    query_bm25 = {
        "size": 5,
        "_source": ["title", "ingredients"],
        "query": {
            "bool": {
                "must": [
                {
                        "match": {
                        "ingredients": qtxt,
                        }   
                }
                ],
                "should": [
                {
                    "multi_match": {
                        "query": qtxt,
                        "fields": ["title", "ingredients"]
                    }
                }
                ]
            }
        }
    }
    client_search(client, index_name, query_bm25,"ingredients")

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def encode(texts):
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/msmarco-distilbert-base-v2")
    model = AutoModel.from_pretrained("sentence-transformers/msmarco-distilbert-base-v2")

    # Tokenize sentences
    encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input, return_dict=True)

    # Perform pooling
    embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # Normalize embeddings
    embeddings = F.normalize(embeddings, p=2, dim=1)
    
    return embeddings

# Note: this is the only method that gets the query as plain text
# Function to search for a title based on embedding
def search_titleEmbedding(client, index_name, query):
    emb_query = encode(query)
    query_denc = {
        'size': 5,
        '_source': ['title', 'index'],
        "query": {
            "knn": {
                "title_embedding": {
                    "vector": emb_query[0].numpy(),
                    "k": 2
                } 
            }
        }
    }
    return client_search(client, index_name, query_denc,"title")

# Function to search for a title and description based on embedding
def search_title_descEmbedding(client, index_name, emb_query):
    query_denc = {
        'size': 5,
        '_source': ['title', 'description'],
        "query": {
            "knn": {
                "descs_embedding": {
                    "vector": emb_query[0].numpy(),
                    "k": 2
                } 
            }
        }
    }
    client_search(client, index_name, query_denc,"title_desc")   



###Auxiliar functions:

# Auxiliar function to handle search response and print results
def client_search(client, index_name, query,info):
    response = client.search(
        body = query,
        index = index_name
    )
    return switch(response,info)

# Function to switch between different search cases and print results accordingly
def switch(response,info):
    hit_list = []

    #print('Found the following recipes:')
    print()
    if info == "title":
        for hit in response['hits']['hits']:
            pp.pprint(hit['_source']['title'])
            hit_list.append(hit['_source']['index'])

            print()
    if info == "title_desc":
        for hit in response['hits']['hits']:
            if("description" not in hit['_source']):
               continue
            else:
                pp.pprint('Description of recipe: ' + hit['_source']['description'])
            print()
    elif info == "term":
        for hit in response['hits']['hits']:
            pp.pprint(hit['_source']['title'] + ' - Containing the term' + hit['_source']['description'])
            print()
    elif info == "time":
        for hit in response['hits']['hits']:
            if("duration" not in hit['_source']):
                continue
            pp.pprint(hit['_source']['title'] + ' - Total time: ' + str(hit['_source']['duration']) + ' minutes')
            print()
    elif info == "ingredients":
        for hit in response['hits']['hits']:
            pp.pprint(hit['_source']['title'] + ' - Containing the following ingredients:  ' + str(hit['_source']['ingredients']))
            print()
    return hit_list


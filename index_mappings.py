import pprint as pp
import requests
from opensearchpy import OpenSearch
from opensearchpy import helpers

import json as json
import doc

host = 'api.novasearch.org'
port = 443
user = 'user201' # Add your user name here.
password = 'Lrr1531' # Add your user password here. For testing only. Don't store credentials in code. 
index_name = user

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = (user, password),
    url_prefix = 'opensearch',
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

def delete_index_mappings():
    response = client.indices.delete(index=user)
    return(response)

def create_index_mappings():
        index_body = {
        "settings": {
        "index": {
        "number_of_replicas":0,
        "number_of_shards":4,
        #"refresh_interval":"-1", -- it's crashing the search
        "knn": True,
        "knn.algo_param.ef_search": 100
        }
    },
        "mappings": {
            "properties": {
                "title": {
                    "type": "text"
                },
                "description": {
                    "type": "text"
                },
                "title_embedding": {
                    "type":"knn_vector",
                "dimension": 768,
                "method":{
                "name":"hnsw",
                "space_type":"innerproduct",
                "engine":"faiss",
                "parameters":{
                    "ef_construction":256,
                    "m":48
                }
                },
                },
                "ingredients": {
                    "type": "keyword"
                },
                "duration": {
                    "type": "integer"
                },
                "steps": {
                    "type": "text"
                },
            }
        }
    }

def create_index():
    if client.indices.exists(index=index_name):
        print("Index already existed. You may force the new mappings.")
    else:        
        response = client.indices.create(index_name, body=index_body)
        print('\nCreating index:')
        print(response)

def index_data(document_dir):
    with open(document_dir, "r") as read_file:
        data = json.load(read_file)

    doc.index_document(client, index_name, data)
     

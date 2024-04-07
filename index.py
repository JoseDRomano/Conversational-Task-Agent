import pickle

def create_index(client, index_name):
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
             "descs_embedding": {
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
    if client.indices.exists(index=index_name):
        print("Index already existed. You may force the new mappings.")
    else:        
        response = client.indices.create(index_name, body=index_body)
        print('\nCreating index:')
        print(response)

def delete_index(client, index_name):
    response = client.indices.delete(
        index = index_name
    )
    print(response) 

def index_document(client, index_name, data):
    for key, recipe in data.items():
        title = recipe['displayName']
        doc = {
            'title': title,
            'description': recipe['description'],
            'ingredients': get_ingredients(recipe),
            'duration': recipe['totalTimeMinutes'],
            'steps': get_steps(recipe)
        }
        resp = client.index(index=index_name, body=doc)
        print(resp['result'] + ": " + title)

def index_titleEmbeddings(client, index_name, titles):
    with open('./pickle_files/title_embeddings.pickle', 'rb') as f:
        title_embs = pickle.load(f)
    
    for i in range(len(title_embs)):
        response = client.index(index=index_name, body={"title": titles[i], "title_embedding": title_embs[i].numpy()})
        print(response['result'] + ": " + titles[i])


def index_descEmbeddings(client, index_name, descs):
    with open('./pickle_files/desc_embeddings.pickle', 'rb') as f:
        descs_embs = pickle.load(f)
    
    for i in range(len(descs_embs)):
        response = client.index(index=index_name, body={"title": descs[i], "descs_embedding": descs_embs[i].numpy()})
        print(response['result'] + ": " + descs[i])


## Auxiliary functions

def get_ingredients(recipe):
    ingredients = []
    for ingredient in recipe['ingredients']:
        ingredients.append(ingredient['ingredient'])
    return ingredients

def get_steps(recipe):
    steps = []
    for step in recipe['instructions']:
        steps.append(step['stepText'])
    return steps

def get_recipe(data,title):
    for key in data:
        if data[key]['displayName'] == title:
            return data[key]
    return None




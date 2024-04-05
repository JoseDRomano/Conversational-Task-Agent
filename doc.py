import json
import pickle

def index_document(client, index_name, data):
    count = 0
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


def index_embeddings(client, index_name, titles):

    with open('embeddings.pickle', 'rb') as f:
            embs = pickle.load(f)
    
    
    for i in range(len(embs)):
        response = client.index(index=index_name, body={"title": titles[i], "title_embedding": embs[i].numpy()})
        print(response['result'] + ": " + titles[i])
    

    




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
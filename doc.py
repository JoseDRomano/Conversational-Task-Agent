import json

def index_document(client, index_name, data):
    count = 0
    for key, recipe in data.items():
        count += 1

        title = recipe['displayName']

        doc = {
            'title': title,
            'description': recipe['description'],
            'ingredients': get_ingredients(recipe),
            'duration': recipe['totalTimeMinutes'],
            'steps': get_steps(recipe)
        }
        resp = client.index(index=index_name, id=count, body=doc)
        print(resp['result'] + ": " + title)


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
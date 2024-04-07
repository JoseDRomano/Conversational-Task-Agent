import json as json
import pickle
import random
import string

def get_recipes():
    with open("./recipes/recipes_data.json", "r") as read_file:
        data = json.load(read_file)
    return data


def get_recipe_titles():
    titles = []
    for key in get_recipes():
        titles.append(get_recipes()[key]['displayName'])
    with open('./pickle_files/recipe_titles.pkl', 'wb') as f:
        pickle.dump(titles, f)
    return titles

def get_recipe_descs():
    descs = []
    for key in get_recipes():
        if(get_recipes()[key]['description'] == None):
            #append random string of length 10
            descs.append(''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))
            
        else:
            descs.append(get_recipes()[key]['description'])
    with open('./pickle_files/recipe_descs.pkl', 'wb') as f:
        pickle.dump(descs, f)
    return descs


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
import json as json
import pickle

def get_recipes():
    with open("./recipes/recipes_data.json", "r") as read_file:
        data = json.load(read_file)
    return data


def get_recipe_titles():
    titles = []
    for key in get_recipes():
        titles.append(get_recipes()[key]['displayName'])
    with open('recipe_titles.pkl', 'wb') as f:
        pickle.dump(titles, f)
    return titles

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
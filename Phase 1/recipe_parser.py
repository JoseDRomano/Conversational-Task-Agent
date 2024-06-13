import json as json
import pickle
import random
import string

# Function to load recipes from a JSON file
def get_recipes():
    with open("../recipes/recipes_data.json", "r") as read_file:
        data = json.load(read_file)
    return data

# Function to retrieve recipe titles and store them in a pickle file
def get_recipe_titles():
    titles = []
    for key in get_recipes():
        titles.append(get_recipes()[key]['displayName'])
    with open('../pickle_files/recipe_titles.pkl', 'wb') as f:
        pickle.dump(titles, f)
    return titles

# Function to retrieve recipe descriptions and store them in a pickle file
def get_recipe_descs():
    descs = []
    for key in get_recipes():
        if(get_recipes()[key]['description'] == None):
            #append random string of length 10 that starts with test
            descs.append(''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))
        else:
            descs.append(get_recipes()[key]['description'])
    with open('../pickle_files/recipe_descs.pkl', 'wb') as f:
        pickle.dump(descs, f)
    return descs

# Function to retrieve recipe descriptions and store them in a pickle file
def get_recipe_steps():
    steps = []
    for key in get_recipes():
        steps.append(get_steps(get_recipes()[key]))
    with open('../pickle_files/recipe_steps.pkl', 'wb') as f:
        pickle.dump(steps, f)
    return steps


# Auxiliary function to extract ingredients from a recipe
def get_ingredients(recipe):
    ingredients = []
    for ingredient in recipe['ingredients']:
        ingredients.append(ingredient['ingredient'])
    return ingredients

# Auxiliary function to extract steps from a recipe
def get_steps(recipe):
    steps = []
    for step in recipe['instructions']:
        steps.append(step['stepText'])
    return steps
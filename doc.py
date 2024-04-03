import json

with open("./recipes/recipes_data.json", "r") as read_file:
    data = json.load(read_file)

ingredients = data['12']['ingredients']

for ingredient in ingredients:
    print(ingredient['displayText'])
 
def index_document(client, index_name):
    count = 0
    for key, recipe in data.items():
        count += 1
        ingredients = recipe[ingredients]
        
        doc = {
            'title': recipe['displayName'],
            'description': recipe['description'],
            'ingredients': recipe['ingredients'],     #TODO
            'duration': recipe['totalTimeMinutes'],
            'steps': recipe['instructions']           #TODO   
        }
        resp = client.index(index=index_name, id=count, body=doc)
        print(resp['result'])

#add this method to the method above when romano is done
def get_ingredients(recipe):
    ingredients = recipe[ingredients]
    
    for ingredient in ingredients:
        print(ingredient['displayText'])
    return
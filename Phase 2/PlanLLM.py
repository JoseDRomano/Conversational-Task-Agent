import json
import recipe_parser as rp
import os
import requests

CONVERSATION_PATH = '../Phase 2/conversation.json'

def setup_dialog(recipe_num):
    recipe_num = str(recipe_num)

    #recipe_len = len(rp.get_recipes())

    #print (f"Number of recipes: {recipe_len}")
    #print (f"Recipe number {recipe_num}")

    displayName = rp.get_recipes()[recipe_num]["displayName"]
    instructions = rp.get_recipes()[recipe_num]["instructions"]
    numInstructions = len(instructions)

    instructionsText = []

    for i in range(numInstructions):
        instructionsText.append(instructions[i]["stepText"])

    with open(CONVERSATION_PATH) as f:
        conversation = json.load(f)

    conversation['task']['recipe']['displayName'] = displayName
    conversation['task']['recipe']['instructions'] = [{'stepText': instruction} for instruction in instructionsText]
    conversation['dialog'] = []

    with open(CONVERSATION_PATH, 'w') as f:
        json.dump(conversation, f)

#"dialog": [{"current_step": 0, "user": "", "system": "\"All set? Here's Step 1: \\u201cBloom\\u201d the yeast by sprinkling the sugar and yeast in the warm water. Let sit for 10 minutes, until bubbles form on the surface. \"\n"}]}

def exit_command(user):
    return "exit" in user or "bye" in user or "quit" in user or "stop" in user or "end" in user or "done" in user or "finish" in user

def dialog():
    external_url = "https://twiz.novasearch.org/"
    max_timeout = 10

    def test_structured_post_request(url: str, conversation):

        url = os.path.join(url, "structured")

        # check this file to understand the structure of the data
        # with open('conversation.json') as f:
        #     data = json.load(f)

        data = {
            "dialog": conversation,
            "max_tokens": 100,
            "temperature": 0.0,
            "top_p": 1,
            "top_k": -1,
        }

        # Make the POST request
        response = requests.post(url, json=data, timeout=max_timeout)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.text
        else:
            print("POST request failed with status code:", response.status_code)

    current_step = 0
    user = input("Ask something!")
    while (not exit_command(user)):
        print()
        print(user)

        with open(CONVERSATION_PATH) as f:
            conversation = json.load(f)

        conversation['dialog'].append({'current_step' : current_step, 'user' : user})

        response = test_structured_post_request(external_url, conversation)

        print()
        print(response)

        conversation['dialog'][current_step]['system'] = response

        with open(CONVERSATION_PATH, 'w') as f:
            json.dump(conversation, f)

        user = input()
        current_step += 1



import json
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

def load_data():
    with open("all_intents.json", 'r') as json_in:
        return json.load(json_in)

def create_model(data):
    id_to_intent, intent_to_id = dict(), dict()
    for i, intent in enumerate(data):
        id_to_intent[i] = intent
        intent_to_id[intent] = i

    return AutoModelForSequenceClassification.from_pretrained(
        "NOVA-vision-language/task-intent-detector", 
        num_labels=len(data), 
        id2label=id_to_intent, 
        label2id=intent_to_id
    ), AutoTokenizer.from_pretrained("roberta-base")

def predict_intent(model, tokenizer, user_input):
    model_in = tokenizer(user_input, return_tensors='pt')
    with torch.no_grad():
        logits = model(**model_in).logits
        predicted_class_id = logits.argmax().item()
        return model.config.id2label[predicted_class_id]

def run(input):
    # Intent detection
    data = load_data()
    model, tokenizer = create_model(data)
    predicted_intent = predict_intent(model, tokenizer,input)

    # Slot filling
    intent_slot_mapping = {
        "GreetingIntent": ['What is the time of day', 'What is the name of the user?'],
        "IdentifyProcessIntent": ['What are the ingredients?', 'What is the cuisine type?', 'What is the meal type?'],
        "OutOfScopeIntent": [],
        "YesIntent": [],
        "NoIntent": [],
        "StartStepsIntent": ['What is the recipe?'],
        "NextStepIntent": ['Current Step Number'],
        "StopIntent": ['What is the reason for stopping?'],
    }

    model_name = "deepset/roberta-base-squad2"
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

    if predicted_intent in intent_slot_mapping:
        print('Intent: ' + predicted_intent + '\n')
        for slot in intent_slot_mapping[predicted_intent]:
            QA_input = {
                'question': slot,
                'context': input
            }
            res = nlp(QA_input)
            print('Slot: ' + slot)
            print('Slot Value: ' + str(res) + '\n')
    else:
        print("Intent not found in mapping")
        print("Intent: " + predicted_intent)

    return predicted_intent

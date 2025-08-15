import random
import json
import torch
from .model import NeuralNet
from .nltk_util import tokenize, bag_of_words

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('chatbot/intents.json', 'r') as f:
    intents = json.load(f)

data = torch.load("chatbot/data.pth")
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

def get_chat_response(msg):
    sentence = tokenize(msg)
    X=bag_of_words(sentence, all_words)
    X=torch.from_numpy(X).to(device)

    output=model(X)
    _, predicted = torch.max(output, dim=0)
    tag= tags[predicted.item()]

    probs = torch.softmax(output, dim=0)
    prob = probs[predicted.item()]

    if prob.item() > 0.7:
        for intent in intents["intents"]:
            if intent["tag"] == tag:
                return random.choice(intent["responses"])
    else:
        return "I'm not sure I understand. Can you rephrase?"
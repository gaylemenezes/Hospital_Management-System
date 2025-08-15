import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from .nltk_util import tokenize, stem, bag_of_words
from .model import NeuralNet
import numpy as np
import os

intent_path = os.path.join(os.path.dirname(__file__), 'intents.json')
with open(intent_path, 'r') as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        print(f"[DEBUG] tokenize = {tokenize}, type = {type(tokenize)}")
        w = tokenize(pattern)  # tokenize returns list of words
        all_words.extend(w)
        xy.append((w, tag))

ignore = ["?", ".", "!"]
all_words = sorted(set([stem(w) for w in all_words if w not in ignore]))
tags = sorted(set(tags))

X_train = []
y_train = []
for (pattern, tag) in xy:
    bag = bag_of_words(pattern, all_words)
    X_train.append(bag)
    y_train.append(tags.index(tag))

X_train = np.array(X_train)
y_train = np.array(y_train)

# Dataset class
class ChatDataset(Dataset):
    def __len__(self):
        return len(X_train)
    def __getitem__(self, idx):
        return X_train[idx], y_train[idx]

# Hyperparameters
batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(all_words)
learning_rate = 0.001
epochs = 1000

dataset = ChatDataset()
loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Instantiate the model
model = NeuralNet(input_size, hidden_size, output_size).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
for epoch in range(epochs):
    for words, labels in loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        output = model(words)
        loss = criterion(output, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

print(f"Final Loss: {loss.item():.4f}")

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}

torch.save(data, "chatbot/data.pth")
print("Training complete. Model saved to chatbot/data.pth")

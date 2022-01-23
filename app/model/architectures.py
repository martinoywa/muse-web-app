import numpy as np

import torch
import torch.utils as utils
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torchvision import transforms, datasets
from transformers import BertForSequenceClassification


class AudioNN(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.conv1 = nn.Conv2d(3, 16, 5)
        self.conv2 = nn.Conv2d(16, 32, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(32*13*40, 1024)
        self.fc2 = nn.Linear(1024, 4)
        
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        
        return x


def audio_model():
    model = AudioNN()

    return model


def lyrics_model():
    model = BertForSequenceClassification.from_pretrained("bert-base-uncased",
                                                          num_labels=4,
                                                          output_attentions=False,
                                                          output_hidden_states=False)

    return model

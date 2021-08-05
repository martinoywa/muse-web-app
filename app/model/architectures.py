import torch.nn as nn
import torchvision
from transformers import BertForSequenceClassification


def audio_model():
    model = torchvision.models.resnet18(pretrained=True)
    for param in model.parameters():
        param.requires_grad = False

    features = model.fc.in_features
    model.fc = nn.Linear(in_features=features, out_features=4)

    return model


def lyrics_model():
    model = BertForSequenceClassification.from_pretrained("bert-base-uncased",
                                                          num_labels=4,
                                                          output_attentions=False,
                                                          output_hidden_states=False)

    return model

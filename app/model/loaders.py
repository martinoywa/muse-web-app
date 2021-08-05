import torch

from .architectures import *


def load_audio_model(weights):
    model = audio_model()
    model.load_state_dict(torch.load(weights, map_location="cpu"), strict=False)
    model.to("cpu")
    model.eval()
    return model


def load_lyrics_model(weights):
    model = lyrics_model()
    model.load_state_dict(torch.load(weights, map_location="cpu"), strict=False)
    model.to("cpu")
    model.eval()
    return model

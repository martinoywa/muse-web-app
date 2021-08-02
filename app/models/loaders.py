import torch
from .architectures import *
from pathlib import Path


def load_audio_model():
    model = audio_model()
    weights_path = Path("app/models/weights/audio/finetuned_Full-RESNET_model.pt")
    model.load_state_dict(torch.load(weights_path, map_location="cpu"), strict=False)
    model.to("cpu")
    model.eval()

    return model

def load_lyrics_model():
    model = lyrics_model()
    weights_path = Path("app/models/weights/lyrics/finetuned_BERT_model-epoch-v.3.pt")
    model.load_state_dict(torch.load(weights_path, map_location="cpu"), strict=False)
    model.to("cpu")
    model.eval()

    return model

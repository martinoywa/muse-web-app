from .loaders import *
import torch
from torchvision import transforms
from transformers import BertTokenizer
from PIL import Image


audio_model = load_audio_model()
lyrics_model = load_lyrics_model()

audio_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.ToTensor()
])

lyrics_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased",
                                                 do_lower_case=True)


def audio_inference(spectrogram):
    image = Image.open(spectrogram).convert("RGB")
    input = audio_transforms(image).unsqueeze(0)
    output = audio_model(input)

    return output


def lyrics_inference(lyrics):
    encoded_input = lyrics_tokenizer.encode_plus(
        lyrics,
        add_special_tokens=True,
        return_attention_mask=True,
        padding=True,
        truncation=True,
        max_length=64,
        return_tensors="pt"
    )
    output = lyrics_model(**encoded_input)

    return output


def aggregate_inference(spectrogram, lyrics):
    audio_output = audio_inference(spectrogram)
    lyrics_output = lyrics_inference(lyrics)
    aggregate = audio_output + lyrics_output
    _, pred = torch.max(aggregate[0], dim=1)
    pred = pred.item()+1

    return pred

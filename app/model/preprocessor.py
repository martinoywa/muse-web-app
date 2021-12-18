from PIL import Image
from torchvision import transforms
from transformers import BertTokenizer


def audio_preprocessor(spectrogram):
    transform = transforms.Compose([
        transforms.ToTensor()
    ])

    image = Image.open(spectrogram).convert("RGB")

    return transform(image).unsqueeze(0)


def lyrics_preprocessor(lyrics):
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased",
                                              do_lower_case=True)

    encoded_lyrics = tokenizer.encode_plus(
        lyrics,
        add_special_tokens=True,
        return_attention_mask=True,
        padding=True,
        truncation=True,
        max_length=158,
        return_tensors="pt"
    )

    return encoded_lyrics

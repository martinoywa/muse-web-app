import os
import unittest
from pathlib import Path
from app.models.loaders import *
from app.models.preprocessor import *
from app.models.inference import *


class MyTestCase(unittest.TestCase):
    def test_audio_weights_exist(self):
        weights = Path("app/models/weights/audio/finetuned_Full-RESNET_model.pt")
        self.assertTrue(True, os.path.isfile(weights))

    def test_lyrics_weights_exist(self):
        weights = Path("app/models/weights/lyrics/finetuned_BERT_model-epoch-v.3.pt")
        self.assertTrue(True, os.path.isfile(weights))

    def test_audio_model_loading(self):
        weights = Path("app/models/weights/audio/finetuned_Full-RESNET_model.pt")
        self.assertIsNotNone(load_audio_model(weights))

    def test_lyrics_model_loading(self):
        weights = Path("app/models/weights/lyrics/finetuned_BERT_model-epoch-v.3.pt")
        self.assertIsNotNone(load_lyrics_model(weights))

    def test_audio_preprocessing(self):
        image_file = Path("app/models/tests/test_files/532171.png")
        self.assertEqual(torch.Tensor, type(audio_preprocessor(image_file)))

    def test_lyrics_encoding(self):
        lyrics_file = Path("app/models/tests/test_files/532171.txt")
        with open(lyrics_file, "r") as f:
            lyrics = f.readlines()
        self.assertEqual(['input_ids', 'token_type_ids', 'attention_mask'], list(lyrics_preprocessor(lyrics).keys()))

    def test_audio_inference(self):
        image_file = Path("app/models/tests/test_files/532171.png")
        self.assertEqual(4, len(audio_inference(image_file)[0]))

    def test_lyrics_inference(self):
        lyrics_file = Path("app/models/tests/test_files/532171.txt")
        with open(lyrics_file, "r") as f:
            lyrics = f.readlines()
        self.assertEqual(4, len(lyrics_inference(lyrics)[0][0]))

    def test_aggregate_inference(self):
        image_file = Path("app/models/tests/test_files/532171.png")
        lyrics_file = Path("app/models/tests/test_files/532171.txt")
        with open(lyrics_file, "r") as f:
            lyrics = f.readlines()
        self.assertEqual(1, aggregate_inference(image_file, lyrics))


    def test_inference_type(self):
        pass

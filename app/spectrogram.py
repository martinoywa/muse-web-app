import torch
import torchaudio

import librosa
import matplotlib.pyplot as plt

import numpy as np

from pydub import AudioSegment
from tempfile import mktemp


# parameters
SAMPLE_RATE = 44100
NFFT = 1024
HL = 512
MELS = 64
NUMBER_OF_SAMPLES = 88200

# mel spectrogram transformer
transformer = torchaudio.transforms.MelSpectrogram(
    sample_rate=SAMPLE_RATE,
    n_fft=NFFT,
    hop_length=HL,
    n_mels=MELS,
    center=True,
    pad_mode="reflect",
    power=2.0,
    norm='slaney',
    onesided=True,
    mel_scale="htk"
)

# mix down or convert to mono channel
def mix_down_if_necessary(signal):
    if signal.shape[0] > 1:
        signal = torch.mean(signal, dim=0, keepdim=True)
    return signal

# resample to SAMPLE_RATE
def resample_if_necessary(signal, sr):
    if sr != SAMPLE_RATE:
        resampler = torchaudio.transforms.Resample(
            orig_freq=sr,
            new_freq=SAMPLE_RATE
        )
        signal = resampler(signal)
    return signal

# cut signal if longer than NUMBER_OF_SAMPLES
def cut_if_necessary(signal):
    if signal.shape[1] > NUMBER_OF_SAMPLES:
        signal = signal[:, :NUMBER_OF_SAMPLES]
    return signal

# right pad if necessary if less than NUMBER_OF_SAMPLES
def right_pad_if_necessary(signal):
    if signal.shape[1] < NUMBER_OF_SAMPLES:
        num_to_pad = NUMBER_OF_SAMPLES - signal.shape[1]
        signal = torch.nn.functional.pad(signal, (0,num_to_pad))
    return signal


def create_mel_spectrogram(file):
    """
    Finds songs on YouTube using track and artist name then
    saves the song's mel spectrogram.
    :param id: Deezer Song ID
    :param track: The song name
    :param artist: The song artist
    :param path: path to store downloaded spectrograms
    :return: song spectrogram
    """

    path = "app/static/spectrogram"
    mp3_audio = AudioSegment.from_file(file, format="mp3")  # read mp3
    mp3_audio = mp3_audio.set_channels(1)  # set to mono channel
    ename = mktemp('.mp3')  # use temporary file
    mp3_audio.export(ename, format="mp3")

    signal, sr = torchaudio.load(ename)
    signal = mix_down_if_necessary(signal)
    signal = resample_if_necessary(signal, sr)
    signal = cut_if_necessary(signal)
    signal = right_pad_if_necessary(signal)
    signal = transformer(signal)

    # save the mel spectrogram
    id = "file"
    plt.imsave(f"{path}/{id}.png", librosa.power_to_db(signal[0].numpy(), ref=np.max), origin="lower", format='png')
    plt.close()

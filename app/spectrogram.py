from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile
from tempfile import mktemp


def create_spectrogram(file):
    path = "app/static/spectrogram"
    mp3_audio = AudioSegment.from_file(file, format="mp3")  # read mp3
    mp3_audio = mp3_audio.set_channels(1)  # set to mono channel
    wname = mktemp('.wav')  # use temporary file
    mp3_audio.export(wname, format="wav")  # convert to wav
    FS, data = wavfile.read(wname)  # read wav file

    # plot spectrogram
    plt.specgram(data, Fs=FS, NFFT=1024, noverlap=0)
    plt.xticks([])
    plt.yticks([])

    # save the spectrogram
    id = "file"
    plt.savefig(f"{path}/{id}", dpi=300)
    plt.close()

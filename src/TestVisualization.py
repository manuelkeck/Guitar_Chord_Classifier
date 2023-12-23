import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

from scipy.io import wavfile


def plot_spectogram(file_path):
    y, sr = librosa.load(file_path)
    d = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)
    librosa.display.specshow(d, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.show()


def plot_spectogram2(file_path):
    sample_rate, audio_data = wavfile.read(file_path)

    plt.figure(figsize=(10, 4))
    plt.specgram(audio_data, Fs=sample_rate, cmap='viridis', aspect='auto')
    plt.title(f"Spectrogram of Chord")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.colorbar(label="Amplitude (dB)")
    plt.show(block=True)




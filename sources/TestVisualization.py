import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

class TestVisualization:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate

    def visualize_chord(self, file_path):
        """
        Visualize a recorded guitar chord. Loads the audio file and plots its spectrogram.
        :param file_path: path to the audio file
        """
        # Laden Sie die Audiodatei
        sample_rate, audio_data = wavfile.read(file_path)

        # Spektrogramm erstellen
        plt.figure(figsize=(10, 4))
        plt.specgram(audio_data, Fs=sample_rate, cmap='viridis', aspect='auto')
        plt.title(f"Spectrogram of Chord")
        plt.xlabel("Time (s)")
        plt.ylabel("Frequency (Hz)")
        plt.colorbar(label="Amplitude (dB)")
        plt.show(block=True)


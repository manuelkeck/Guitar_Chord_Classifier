import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from sources.chord_detection.CNNHandler import CNN


def init_model():
    cnn = CNN((128, 87))
    cnn.load_model()
    return cnn


class ChordDetector:
    def __init__(self, path):
        self.file_path = path

    def plot_spectogram(self):
        y, sr = librosa.load(self.file_path)
        d = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)
        librosa.display.specshow(d, sr=sr, x_axis='time', y_axis='log')
        plt.colorbar(format='%+2.0f dB')
        plt.show()

    def classify_chord(self):
        cnn = init_model()
        chord = cnn.predict(self.file_path, False)
        print(f"Recorded chord is: {chord}")
        # handle exceptions

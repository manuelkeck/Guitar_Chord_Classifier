

from sources.chord_detection.CNNHandler import CNN


def init_model():
    cnn = CNN((128, 87))
    cnn.load_model()
    return cnn


class ChordDetector:
    def __init__(self, path, webcam):
        self.file_path = path
        self.webcam = webcam

    def classify_chord(self):
        cnn = init_model()
        chord = cnn.predict(self.file_path, False)

        # handle exceptions or chord not found

        return chord

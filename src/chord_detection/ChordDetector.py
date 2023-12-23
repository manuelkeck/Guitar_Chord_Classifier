from src.chord_detection.CNNHandler import CNN


def init_model():
    cnn = CNN((128, 87))
    cnn.load_model()
    return cnn


class ChordDetector:
    def __init__(self):
        self.cnn = init_model()

    def classify_chord(self, file_path):
        chord = self.cnn.predict(file_path, False)

        # todo: handle exceptions or chord not found

        return chord

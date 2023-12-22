from sources.device_handler.AudioInterface import AudioInterface
from sources.device_handler.Camera import Camera
from sources.audiostream_handler.AudioStream import AudioStream
from sources.chord_detection.ChordDetector import ChordDetector
from sources.Settings import CLASSES


class GUIAppController:
    def __init__(self, gui_app):
        self.gui_app = gui_app

    def start_chord_detection(self):
        print("Record button clicked")

        self.gui_app.record_button["state"] = "disabled"

        # Init audio interface and built-in webcam
        device, index = AudioInterface.find_device()
        webcam = Camera()

        # Record audio if audio interface was found
        if device is not None and index is not None:
            audio_stream = AudioStream(index)
            recorded_audio_path = audio_stream.record_audio()
            print(f"Recorded audio stored here: {recorded_audio_path}")

        # Temporary hardcoded paths to recorded audio (testing)
        recorded_audio_path = "data/records/Major_0.wav"

        # Find chord (record = CNN input, chord = CNN output) and capture image
        cd = ChordDetector(recorded_audio_path, webcam)
        chord = cd.classify_chord()
        if chord in CLASSES:
            print(f"Recorded chord is: {chord}. \nImage will be captured.")
            image_path = webcam.capture_image(recorded_audio_path)
            print(f"Image stored here: {image_path}")

        self.gui_app.record_button["state"] = "normal"

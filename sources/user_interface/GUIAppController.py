from sources.device_handler.AudioInterface import AudioInterface
from sources.device_handler.Camera import Camera
from sources.audiostream_handler.AudioStream import AudioStream
from sources.chord_detection.ChordDetector import ChordDetector
from sources.Settings import CLASSES
from sources.TestVisualization import plot_spectogram, plot_spectogram2


class GUIAppController:
    def __init__(self, gui_app):
        self.gui_app = gui_app
        self.latest_audio_path = ""
        self.latest_image_path = ""

    def start_chord_detection(self):
        self.gui_app.record_button["state"] = "disabled"

        # Init audio interface and built-in webcam
        device, index = AudioInterface.find_device()
        webcam = Camera()

        # Record audio if audio interface was found
        if device is not None and index is not None:
            audio_stream = AudioStream(index)
            self.latest_audio_path = audio_stream.record_audio()
            print(f"Recorded audio stored here: {self.latest_audio_path}")
            self.add_text(f"Record: Recorded audio stored here: {self.latest_audio_path}")

        else:
            self.latest_audio_path = "data/records/Major_0.wav"

        # Find chord (record = CNN input, chord = CNN output) and capture image
        cd = ChordDetector(self.latest_audio_path)
        chord = cd.classify_chord()
        if chord in CLASSES:
            print(f"Recorded chord is: {chord}. \nImage will be captured.")
            self.add_text(f"Record: Recorded chord is: {chord}. \nImage will be captured.")
            try:
                self.latest_image_path = webcam.capture_image(self.latest_audio_path)
                print(f"Image stored here: {self.latest_image_path}")
                self.add_text(f"Record: Image stored here: {self.latest_image_path}")
            except OSError:
                print("An error occurred: Camera not reachable.")
                self.add_text("Record: An error occurred: Camera not reachable.")

        self.gui_app.record_button["state"] = "normal"

    def show_spectogram(self):
        if self.latest_audio_path != "":
            print("Showing mel-spectogram of audio")
            self.add_text("Spectogram: Showing mel-spectogram of audio")
            plot_spectogram(self.latest_audio_path)
            # plot_spectogram2(self.latest_audio_path)
        else:
            print("Record audio first.")
            self.add_text("Spectogram: Record audio first.")

    def discard_record(self):
        # todo: delete label too

        if self.latest_audio_path == "" or self.latest_image_path == "":
            print("Recording audio needed to discard record.")
            self.add_text("Discard: Recording audio needed to discard record.")
        else:
            print("Recorded audio and captured image will be deleted.")
            self.add_text("Discard: Recorded audio and captured image will be deleted.")
            tmp_audio = self.latest_audio_path
            tmp_image = self.latest_image_path

            # todo: delete feature

            self.latest_audio_path = ""
            self.latest_audio_path = ""

            self.add_text(f"Discard: {tmp_audio} deleted.")
            self.add_text(f"Discard: {tmp_image} deleted.")

    def add_text(self, text):
        self.gui_app.textfield.insert("end", f"{text}\n")
        self.gui_app.textfield.see("end")

import os
import threading
import time

from src.device_handler.AudioInterface import AudioInterface
from src.audiostream_handler.AudioStream import AudioStream
from src.chord_detection.ChordDetector import ChordDetector
from Settings import CLASSES, DURATION
from src.TestVisualization import plot_spectogram
from datetime import datetime


class GUIAppController:
    """
    This class contains all needed functions which are implemented directly with GUI.
    If interactions with GUI will be performed, these functions contain the logic behind.
    """

    def __init__(self, gui_app):
        self.gui_app = gui_app
        self.latest_audio_path = ""
        self.latest_image_path = ""
        self.start_time = None
        self.recording_thread = None
        self.device, self.index = AudioInterface.find_device()
        self.cd = ChordDetector()

    def record_audio(self):
        """
        This function starts the recording process, if audio interface could be found.
        Recorded audio is going to be the input for CNN and outputs the identified chord.
        :return: None; If chord could be identified, an image will be captured and stored
        to local file system. In addition, this function calls in a second function with
        an own thread to visualize loading bar in GUI textfield.
        """
        if self.device is not None and self.index is not None:
            # Record audio
            audio_stream = AudioStream(self.index)
            self.latest_audio_path, name = audio_stream.record_audio()
            self.gui_app.progressbar.stop()

            print(f"Recorded audio stored here: {self.latest_audio_path}")
            self.add_text(f"[Record] Recorded audio stored here: ../data/records/{name}")

        else:
            self.add_text("[Record] Audio interface not found. Fallback to pre-defined audio path.")
            # C-Dur (Downloaded from kaggle)
            # self.latest_audio_path = "data/records/Major_0.wav"
            # Self-recorded C-Dur
            self.latest_audio_path = "data/records/record-20231223-141242.wav"
            # Self-recorded D-Dur
            # self.latest_audio_path = "data/records/record-20231223-141414.wav"
            # Self-recorded G-Dur
            # self.latest_audio_path = "data/records/record-20231223-141521.wav"


    def record_audio_test(self):
        print("Record audio started")
        time.sleep(5)

    def perform_chord_detection(self):
        """

        :return:
        """
        # Find chord (record = CNN input, chord = CNN output) and capture image
        chord = self.cd.classify_chord(self.latest_audio_path)
        if chord in CLASSES:
            print(f"Recorded chord is: {chord}. \nImage will be captured.")
            self.add_text(f"[Record] Recorded chord is: {chord}. \n[Record] Image will be captured.")
            try:
                self.latest_image_path, name = self.gui_app.camera.capture_image(self.latest_audio_path)
                print(f"Image stored here: {self.latest_image_path}")
                self.add_text(f"[Record] Image stored here: ../data/images/{name}.jpg")
            except OSError:
                print("An error occurred: Camera not reachable.")
                self.add_text("[Record] An error occurred: Camera not reachable.")

        self.gui_app.record_button["state"] = "normal"

    def show_spectogram(self):
        """
        This function calls one (or two) function to show a mel-spectogram of recorded
        audio.
        :return: None
        """
        if self.latest_audio_path != "":
            print("Showing mel-spectogram of audio")
            self.add_text("[Spectogram] Showing mel-spectogram of audio")
            plot_spectogram(self.latest_audio_path)
            # plot_spectogram2(self.latest_audio_path)
        else:
            print("Record audio first.")
            self.add_text("[Spectogram] Record audio first.")

    def discard_record(self):
        """
        This function discards the previously recorded audio file and captured image.
        This is needed, in case that identified chord was wrong or insufficient.
        :return: None
        """
        if self.latest_audio_path == "" or self.latest_image_path == "":
            print("Recording audio needed to discard record.")
            self.add_text("[Discard] Record audio first to discard record.")
        else:
            print("Recorded audio and captured image will be deleted.")
            tmp_audio = self.latest_audio_path
            tmp_image = self.latest_image_path

            # discard files
            try:
                # os.remove(self.latest_audio_path)
                os.remove(self.latest_image_path)
                print("Files were deleted.")
                audio_name = os.path.basename(tmp_audio)
                image_name = os.path.basename(tmp_image)
                self.add_text("[Discard] The following files will be discarded:")
                self.add_text(f"[Discard] {audio_name}")
                self.add_text(f"[Discard] {image_name}")
            except FileNotFoundError:
                print("Files to delete not found.")
                self.add_text("[Discard] Files not found.")
            except Exception as e:
                print("Error while deleting files.")
                self.add_text("[Discard] Error while deleting files.")

            # todo: delete label too

            self.latest_audio_path = ""
            self.latest_audio_path = ""

    def add_text(self, text):
        """
        This function can print messages to textfield in GUI.
        :param text: Text to be printed
        :return: None
        """
        self.gui_app.textfield.insert("end", f"{text}\n")
        self.gui_app.textfield.see("end")
        self.gui_app.update()

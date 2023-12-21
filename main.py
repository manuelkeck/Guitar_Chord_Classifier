import cv2
import tkinter as tk

from sources.device_handler.AudioInterface import AudioInterface
from sources.audiostream_handler.AudioStream import AudioStream
from sources.TestVisualization import plot_spectogram, plot_spectogram2
from sources.chord_detection.ChordDetector import ChordDetector
from sources.device_handler.Camera import Camera
from sources.Settings import CLASSES
from sources.user_interface.GUIApp import GUIApp
from sources.user_interface.GUIAppController import GUIAppController


def show_spectogram(recorded_audio_path):
    print("Show mel-spectogram of audio")
    # plot_spectogram(recorded_audio_path)
    # plot_spectogram2(recorded_audio_path)


def get_chord_capture_image(recorded_audio_path, camera):
    cd = ChordDetector(recorded_audio_path, camera)
    chord = cd.classify_chord()
    if chord in CLASSES:
        print(f"Recorded chord is: {chord}. \nImage will be captured.")
        image_path = camera.capture_image(recorded_audio_path)
        print(f"Image stored here: {image_path}")


def main():
    # Init audio interface and built-in webcam
    device, index = AudioInterface.find_device()
    webcam = Camera()

    while not webcam.is_opened():
        print("Waiting for webcam...")
        cv2.waitKey(1000)
        webcam.release()
        webcam = Camera()

    # Open graphical user interface after init complete
    root = tk.Tk()
    app = GUIApp(root)
    # Following line needed that GUIAppController can access GUIApp attributes
    GUIAppController.gui_app = app
    root.mainloop()

    # Record audio if audio interface was found
    if device is not None and index is not None:
        audio_stream = AudioStream(index)
        recorded_audio_path = audio_stream.record_audio()
        print(f"Recorded audio stored here: {recorded_audio_path}")

    # Temporary hardcoded paths to recorded audio (testing)
    # recorded_audio_path = "data/records/record-20231207-212628.wav"
    # recorded_audio_path = "data/records/Major_0.wav"
    recorded_audio_path = "data/records/record-20231207-212459.wav"

    # Show (mel-)spectogram of recorded audio
    show_spectogram(recorded_audio_path)

    # Find chord (record = CNN input, chord = CNN output) and capture image
    get_chord_capture_image(recorded_audio_path, webcam)


if __name__ == '__main__':
    main()

import tkinter as tk

from sources.TestVisualization import plot_spectogram, plot_spectogram2
from sources.chord_detection.ChordDetector import ChordDetector
from sources.Settings import CLASSES
from sources.user_interface.GUIApp import GUIApp


def show_spectogram(recorded_audio_path):
    print("Showing mel-spectogram of audio")
    plot_spectogram(recorded_audio_path)
    plot_spectogram2(recorded_audio_path)


def get_chord_capture_image(recorded_audio_path, camera):
    cd = ChordDetector(recorded_audio_path, camera)
    chord = cd.classify_chord()
    if chord in CLASSES:
        print(f"Recorded chord is: {chord}. \nImage will be captured.")
        image_path = camera.capture_image(recorded_audio_path)
        print(f"Image stored here: {image_path}")


def main():
    root = tk.Tk()
    GUIApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()

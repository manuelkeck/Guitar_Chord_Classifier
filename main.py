from sources.device_handler.AudioInterface import AudioInterface
from sources.audiostream_handler.AudioStream import AudioRecorder
from sources.TestVisualization import TestVisualization
from sources.chord_detection.ChordDetector import ChordDetector


def show_test_visualization():
    sample_rate = 44100
    visualizer = TestVisualization(sample_rate)
    file_path = "data/records/record-20231207-212628.wav"
    visualizer.visualize_chord(file_path)


def show_plot_spectogram():
    # file_path = "data/records/Major_0.wav"
    file_path = "data/records/record-20231207-212628.wav"
    cd = ChordDetector(file_path)
    # cd.plot_spectogram()
    # cd.recognize_chord()
    cd.classify_chord()


def main():
    device, index = AudioInterface.find_device()

    if device is not None and index is not None:
        audio_stream = AudioRecorder(index)
        audio_stream.record_audio()

    # show_test_visualization()
    show_plot_spectogram()


if __name__ == '__main__':
    main()

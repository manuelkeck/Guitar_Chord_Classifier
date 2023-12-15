from sources.AudioInterface import AudioInterface
from sources.AudioStreamPyaudio import AudioRecorder
from sources.TestVisualization import TestVisualization


def main():
    device, index = AudioInterface.find_device()

    if device is not None and index is not None:
        audio_stream = AudioRecorder(index)
        audio_stream.record_audio()

    # Test visualization
    sample_rate = 44100
    visualizer = TestVisualization(sample_rate)

    file_path = "data/records/record-20231207-212628.wav"

    visualizer.visualize_chord(file_path)


if __name__ == '__main__':
    main()

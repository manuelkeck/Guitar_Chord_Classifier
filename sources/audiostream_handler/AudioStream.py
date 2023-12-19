import pyaudio
import numpy as np
import wavio
from datetime import datetime
import matplotlib.pyplot as plt


class AudioStream:
    def __init__(self, device_index, sample_rate=44100, duration=5):
        self.device_index = device_index
        self.sample_rate = sample_rate
        self.duration = duration
        self.recorded_data = b''
        self.stream = ''

    def record_audio(self, sample_rate=44100, duration=5):
        """

        :param sample_rate:
        :param duration:
        :return:
        """
        p = pyaudio.PyAudio()

        try:
            self.stream = p.open(format=pyaudio.paInt16,
                                 channels=1,
                                 rate=sample_rate,
                                 input=True,
                                 input_device_index=self.device_index)

            print(f"Recording started for {duration} seconds...")
            frames = []

            for _ in range(int(sample_rate / 1024 * duration)):
                data = self.stream.read(1024)
                frames.append(np.frombuffer(data, dtype=np.int16))

            print("Recording finished.")

            # Convert frames to a numpy array
            recorded_data = np.concatenate(frames, axis=0)

            # Save recorded data as .wav file
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            record_filename = f'data/records/record-{timestamp}.wav'
            wavio.write(record_filename, recorded_data.astype(np.int16), sample_rate)

            print(f"Recording saved as {record_filename}")
            self.visualize_audio(recorded_data, record_filename)

            return record_filename

        finally:
            self.stream.stop_stream()
            self.stream.close()
            p.terminate()

    def visualize_audio(self, audio_data, title):
        """
        Visualize the audio stream. Recorded audio data is stored in a numpy array
        with shape (sample_rate x channels) where channels is the number of channels
        in the audio
        :param audio_data: recorded audio data
        :param title: title of plotted file (record-YYYYMMDD-HHMM)
        """
        time = np.arange(0, len(audio_data)) / self.sample_rate

        # Apply Fourier Transform to get the frequency spectrum
        freq_spectrum = np.fft.fft(audio_data)
        freq_values = np.fft.fftfreq(len(freq_spectrum), 1 / self.sample_rate)
        freq_values = freq_values[:len(freq_spectrum) // 2]  # Use only positive frequencies

        # Plot the frequency spectrum
        plt.figure(figsize=(10, 4))
        plt.plot(freq_values, np.abs(freq_spectrum[:len(freq_spectrum) // 2]), color="b")
        plt.title(f"Frequency Spectrum of {title}")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show(block=True)

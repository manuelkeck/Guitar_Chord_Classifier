"""
Author: Manuel Keck
"""
import pyaudio
import numpy as np
import wavio
import matplotlib.pyplot as plt
import sys

from datetime import datetime
from Settings import RECORDING_DIR, SAMPLE_RATE, DURATION, CHUNK_SIZE, MAX_INPUT_CHANNELS


class AudioStream:
    def __init__(self, device_index):
        self.device_index = device_index
        self.recorded_data = b''
        self.stream = ''
        self.record_filename = ""

    def record_audio(self):
        """
        This function records an audio stream from usb audio interface and stores
        it to local file system.
        :return: Path to stored audio record file
        """
        p = pyaudio.PyAudio()

        try:
            self.stream = p.open(
                format=pyaudio.paInt16,
                channels=MAX_INPUT_CHANNELS,
                rate=SAMPLE_RATE,
                input=True,
                input_device_index=self.device_index
            )

            print(f"Recording started for {DURATION} seconds...")
            frames = []

            for _ in range(int(SAMPLE_RATE / CHUNK_SIZE * DURATION)):
                data = self.stream.read(CHUNK_SIZE)
                frames.append(np.frombuffer(data, dtype=np.int16))

            print("Recording finished.")

            # Convert frames to a numpy array
            self.recorded_data = np.concatenate(frames, axis=0)

            # Preprocessing

            # Save recorded data as .wav file
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            file_name = f"record-{timestamp}.wav"
            self.record_filename = f'{RECORDING_DIR}{file_name}'
            wavio.write(self.record_filename, self.recorded_data.astype(np.int16), SAMPLE_RATE)

            print(f"Recording saved as {self.record_filename}")
            # self.visualize_audio(self.recorded_data, self.record_filename)

        except IOError as e:
            print(f"IOError: {e}")
            sys.exit(1)
        except ValueError as e:
            print(f"ValueError: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)

        finally:
            self.stream.stop_stream()
            self.stream.close()
            p.terminate()

        return self.record_filename, file_name

    def visualize_audio(self, audio_data, title):
        """
        Visualize the audio stream. Recorded audio data is stored in a numpy array
        with shape (sample_rate x channels) where channels is the number of channels
        in the audio
        :param audio_data: recorded audio data
        :param title: title of plotted file (record-YYYYMMDD-HHMM)
        """
        time = np.arange(0, len(audio_data)) / SAMPLE_RATE

        # Apply Fourier Transform to get the frequency spectrum
        freq_spectrum = np.fft.fft(audio_data)
        freq_values = np.fft.fftfreq(len(freq_spectrum), 1 / SAMPLE_RATE)
        freq_values = freq_values[:len(freq_spectrum) // 2]

        # Plot the frequency spectrum
        plt.figure(figsize=(10, 4))
        plt.plot(freq_values, np.abs(freq_spectrum[:len(freq_spectrum) // 2]), color="b")
        plt.title(f"Frequency Spectrum of {title}")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show(block=True)

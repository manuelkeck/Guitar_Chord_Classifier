import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import wavio
from datetime import datetime


class AudioStream:

    def __init__(self, device_index=0, sample_rate=44100, duration=5):
        self.device_index = device_index
        self.sample_rate = sample_rate
        self.duration = duration
        self.recorded_data = []

    def callback(self, data, frames, time, status):
        """
        Internal method used from sounddevice bib to record and store data asynchronously
        :param data: recorded data, stored as numpy array
        :param frames:
        :param time:
        :param status: checks audio stream status. Monitoring for record
        """
        if status:
            print(status)
        self.recorded_data.append(data.copy())

    def record_audio(self):
        """
        Records audio streamed in from Steinberg audio interface. Records for a
        duration of 5 seconds and stores file in temporary folder named ../data/records.
        """
        with sd.InputStream(
                device=self.device_index,
                channels=1,
                samplerate=self.sample_rate,
                callback=self.callback):
            print(f"Recording started for {self.duration} seconds...")
            # Wait for record to be done
            sd.sleep(self.duration * 1000)
            print("Recording finished.")

        # Convert to numpy array
        recorded_data = np.concatenate(self.recorded_data, axis=0)

        # Amplification of recorded data
        amp_factor = 100
        amp_recorded_data = recorded_data * amp_factor

        # Normalization (amplitude)
        # --- removed amp ---
        #norm_recorded_data = recorded_data / np.max((np.abs(recorded_data)))

        # Scale amplified data
        max_int32 = np.iinfo(np.int32).max
        min_int32 = np.iinfo(np.int32).min
        #scaled_recorded_data = (norm_recorded_data * max_int32).astype(np.int32)

        # Store recorded data as .wav file
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        record_filename = f'data/records/record-{timestamp}.wav'
        wavio.write(record_filename, recorded_data.astype(np.int32), self.sample_rate)

        self.visualize_audio(recorded_data, record_filename)

    def visualize_audio(self, audio_data, title):
        """
        Visualize the audio stream. Recorded audio data is stored in a numpy array
        with shape (sample_rate x channels) where channels is the number of channels
        in the audio
        :param audio_data: recorded audio data
        :param title: title of plotted file (record-YYYYMMDD-HHMM)
        """
        time = np.arange(0, len(audio_data)) / self.sample_rate

        plt.figure(figsize=(10, 4))
        plt.plot(time, audio_data, color="b")
        plt.title(f"Waveform of file {title}")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show(block=True)

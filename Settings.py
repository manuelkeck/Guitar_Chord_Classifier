"""
This code is based on https://github.com/ayushkumarshah/Guitar-Chords-recognition
with some modifications and extensions.
"""

import os

# The Root Directory of the project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(ROOT_DIR, 'models/chord_audio_detector')
MODEL_JSON = os.path.join(MODEL_DIR, 'model.json')
MODEL_H5 = os.path.join(MODEL_DIR, 'model.h5')

OUT_DIR = os.path.join(ROOT_DIR, 'data/')
RECORDING_DIR = os.path.join(OUT_DIR, 'records/')
IMAGE_DIR = os.path.join(OUT_DIR, 'images/')

# WAVE_OUTPUT_FILE = os.path.join(RECORDING_DIR, "recorded.wav")
# SPECTROGRAM_FILE = os.path.join(RECORDING_DIR, "spectrogram.png")

# Features
CLASSES = ['A', 'Am', 'Bm', 'C', 'D', 'Dm', 'E', 'Em', 'F', 'G']
CLASSES_MAP = {
    'A': 0,
    'Am': 1,
    'Bm': 2,
    'C': 3,
    'D': 4,
    'Dm': 5,
    'E': 6,
    'Em': 7,
    'F': 8,
    'G': 9
}

# Audio configurations
MAX_INPUT_CHANNELS = 1
SAMPLE_RATE = 44100
DURATION = 3
CHUNK_SIZE = 1024

# Camera configuration
CAMERA_INDEX = 1

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

OUT_DIR = os.path.join(ROOT_DIR, 'output/')
RECORDING_DIR = os.path.join(OUT_DIR, 'recording')
IMAGE_DIR = os.path.join(OUT_DIR, 'images')

WAVE_OUTPUT_FILE = os.path.join(RECORDING_DIR, "recorded.wav")
SPECTROGRAM_FILE = os.path.join(RECORDING_DIR, "spectrogram.png")

# Features
CLASSES = ['a', 'am', 'bm', 'c', 'd', 'dm', 'e', 'em', 'f', 'g']
CLASSES_MAP = {
    'a': 0,
    'am': 1,
    'bm': 2,
    'c': 3,
    'd': 4,
    'dm': 5,
    'e': 6,
    'em': 7,
    'f': 8,
    'g': 9
}

# Audio configurations
MAX_INPUT_CHANNELS = 1
DEFAULT_SAMPLE_RATE = 44100
DURATION = 5
CHUNK_SIZE = 1024

# Guitar Chord Detector

The main objective of this project is to create an own dataset with images from guitar chords.
To achieve this, an existing guitar chord detection is integrated.
If a chord was detected successfully, an image will be created, labelled and stored.

For chord detection, some parts of this project are integrated: https://github.com/ayushkumarshah/Guitar-Chords-recognition
This project is licenced under [GNU GPL3](https://www.gnu.org/licenses/gpl-3.0.en.html).

After the collection of a meaningful sum of images is done (separated in training and validation datasets), an own Convolutional Neural Network (CNN) will be trained, based on the created dataset.


## Getting started
Clone repository with `git clone https://gitlab.reutlingen-university.de/keckm/guitar_chord_detector.git`.

### Preconditions
1. Connect an audio interface (e.g. Steinberg UR22C)
2. Get interface ...
3. Get camera ID ...
4. 

### Install libraries
To get all needed libraries, open a new terminal and execute `pip install -r requirements.txt` in cloned folder `Guitar_Chord_Detector`. 
It is recommended to do this in a virtual environment which can be created with 
e.g. venv (https://docs.python.org/3/library/venv.html).

### Part 1: Create dataset(s) with chord images
To reproduce this part, change branch to `create_dataset` with command `git checkout create_dataset`.
After changing branch successfully, start with `python main.py`. A Graphical User Interface (GUI) will be opened.\
The GUI will look like this:
![Image](resources/Screenshot_part1.png)
In this screenshot you can see the camera preview to predict the image that will be captured 
if a chord could be detected. On right side you can see some statements like 'Recorded chord is: c'.

### Part 2: Create CNN based on captured images
tbd

## Authors and acknowledgment
Manuel Keck\
Human-Centered Computing (INF)\
Reutlingen University\
2023

## License
This project is an open-source project.
The following libraries are/were used and are categorized by licence.
The following information is not guaranteed to be complete and correct.

[MIT License](https://opensource.org/licenses/MIT):
pyaudio,
sounddevice,
pip,
wheel,
rsa,
setuptools,
gdown,
lazycats,
requests,
wrapt,
rich,
pyasn1,
termcolor,
pycparser,
pyparsing,
oauthlib,
MarkupSafe,
idna,
pyusb,
screeninfo,
cffi,
filelock,
platformdirs,
wrapt,
gdown,
lazycats,
pydub,
noisereduce,
pedalboard,
fonttools

[BSD License](https://opensource.org/licenses/BSD-3-Clause):
numpy,
scipy,
Pillow,
six,
numba,
packaging,
scikit-learn,
python-dateutil,
Markdown,
llvmlite,
h5py,
soundfile,
cachetools,
contourpy,
cycler,
kiwisolver,
opencv-python,
pooch,
joblib,
werkzeug,
contourpy,
decorator,
torchvision

[Apache License 2.0](https://opensource.org/licenses/Apache-2.0):
tensorflow,
tensorboard,
astunparse,
flatbuffers,
urllib3,
soupsieve,
cython,
msgpack,
requests

[LGPL (Lesser General Public License)](https://www.gnu.org/licenses/lgpl-3.0.html):
usb,
soxr

[ISC License](https://opensource.org/licenses/ISC):
librosa

[Matplotlib License](https://matplotlib.org/stable/users/license.html):
matplotlib,
cycler

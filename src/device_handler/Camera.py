"""
Author: Manuel Keck
"""
import cv2
import os
import time

from Settings import IMAGE_DIR, CAMERA_INDEX
from src.data.Image import ImageProcessing


class Camera:
    """
    This class initializes the hardware camera and implements functions for camera handling. This is needed for
    camera preview in GUI and capturing images.
    """
    def __init__(self, gui_app, controller):
        """
        The selected camera will be initialized. A live stream from camera image will be prepared with self.cap.
        The width and height parameters are needed values for GUI.
        :param camera_index: index of camera. macOS camera_index = 1, ubuntu camera_index = -1
        """
        self.camera_index = CAMERA_INDEX
        self.cap = cv2.VideoCapture(self.camera_index)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.gui_app = gui_app
        self.controller = controller
        self.image_processing = ImageProcessing(self.gui_app, self.controller)

        if not self.cap.isOpened():
            raise Exception("Camera could not be opened.")

    def is_opened(self):
        """
        This function returns the status about the camera stream.
        :return: true/false
        """
        return self.cap.isOpened()

    def release(self):
        """
        This function is needed to release the selected camera properly after quitting program.
        :return: None
        """
        self.cap.release()

    def get_frame(self):
        """
        This function reads a single frame from camera
        :return: Single frame from camera in RGB format
        """
        ret, frame = self.cap.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            return None

    def capture_image(self, recorded_audio_path):
        """
        This function is called after a chord was classified. An image will be
        captured and same name like corresponding audio file (with
        .jpg prefix) will be used. This function will call the get_frame() function
        to capture one single frame from camera stream.
        The captured frame will be processed in Image class to get a cropped image
        based on recognized hand. This image will be stored to local file system.
        :param recorded_audio_path: Path to previously recorded audio file
        :return: Path to captured image
        """
        frame = self.get_frame()
        counter = 0
        check_var = False

        print("Capturing image...")

        # To avoid OpenCV rowBytes == 0 error
        while frame is None and counter < 3:
            frame = self.get_frame()
            time.sleep(2)
            counter += 1

        if frame is None:
            raise Exception("Error while loading image from stream.")
        else:
            # Get name from recorded audio and remove .wav extension to store image with same name
            image_name, extension = os.path.splitext(os.path.basename(recorded_audio_path))
            file_extension = ".jpg"

            # Create path with file name to save image locally
            image_path = os.path.join(IMAGE_DIR, f"{image_name}{file_extension}")

            # Send image to crop function
            check_var = ImageProcessing.crop_captured_image(self.image_processing, frame, image_path)

        return check_var

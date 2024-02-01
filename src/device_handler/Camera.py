"""
Author: Manuel Keck
"""
import cv2
import os
import time

from Settings import CAMERA_INDEX
from src.data.Image import ImageProcessing
from src.data.ImageHelpers import get_index, get_folder, update_index


class Camera:
    """
    This class initializes the hardware camera and implements functions for camera handling. This is needed for
    camera preview in GUI and capturing images.
    """
    def __init__(self, gui_app, controller):
        """
        The selected camera will be initialized. A live stream from camera image will be prepared with self.cap.
        The width and height parameters are needed values for GUI.
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

    def capture_image(self, chord, flag: str):
        """
        This function is called after a chord was classified. An image will be
        captured and same name like corresponding audio file (with
        .jpg prefix) will be used. This function will call the get_frame() function
        to capture one single frame from camera stream.
        The captured frame will be processed in Image class to get a cropped image
        based on recognized hand. This image will be stored to local file system.
        :param chord: Chord which was identified. Needed for image path
        :param flag: Will be used to determine caller function (needed for fast-lane
        implementation)
        :return: Path to captured image
        """
        frame = self.get_frame()
        counter = 0
        path = get_folder(chord)
        index = get_index(path)
        pass
        tmp_path = os.path.join(path + f"training/{chord}/{chord}-{index}.jpg")

        # To avoid OpenCV rowBytes == 0 error
        while frame is None and counter < 3:
            frame = self.get_frame()
            time.sleep(2)
            counter += 1

        if frame is None:
            raise Exception("Error while loading image from stream.")
        else:
            # Return image as numpy array
            if flag == "fast-lane":
                return frame

            # Send image to crop function
            else:
                if ImageProcessing.get_hand_landmarks(self.image_processing, frame, tmp_path):
                    print(f"Index in folder for chord {chord} will be updated.")
                    self.controller.add_text(f"[Image] Index in folder for chord {chord} will be updated to {index}.")
                    update_index(path, index+1)

        return

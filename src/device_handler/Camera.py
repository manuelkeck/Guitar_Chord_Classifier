import cv2
import os


class Camera:
    """
    This class initializes the hardware camera and implements functions for camera handling. This is needed for
    camera preview in GUI and capturing images.
    """
    def __init__(self, camera_index=1):
        """
        The selected camera will be initialized. A live stream from camera image will be prepared with self.cap.
        The width and height parameters are needed values for GUI.
        :param camera_index: index of camera. macOS camera_index = 1, ubuntu camera_index = -1
        """
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

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
        This function is called after a chord was classified. An image will be captured and stored with same name like
        corresponding audio file (with .jpg prefix). This function will call the get_frame() function to capture one
        single frame from camera stream.
        :param recorded_audio_path: Path to previously recorded audio file
        :return: Path to captured image
        """
        frame = self.get_frame()

        if frame is None:
            raise Exception("Error while loading image from stream.")

        # Get name from recorded audio and remove .wav extension to store image with same name
        image_name, extension = os.path.splitext(os.path.basename(recorded_audio_path))
        image_directory = "data/images/"
        file_extension = ".jpg"

        # Save the single captured frame as an image
        image_path = os.path.join(image_directory, f"{image_name}{file_extension}")
        cv2.imwrite(image_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), [int(cv2.IMWRITE_JPEG_QUALITY), 100])

        return image_path

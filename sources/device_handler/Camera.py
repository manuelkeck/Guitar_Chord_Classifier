import cv2
import os


class Camera:
    def __init__(self, camera_index=1):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise Exception("Camera could not be opened.")

    def is_opened(self):
        return self.cap.isOpened()

    def release(self):
        self.cap.release()

    def capture_image(self, recorded_audio_path):
        ret, frame = self.cap.read()

        # Check if image can be read successfully
        if not ret:
            raise Exception("Error while loading image from stream.")

        # Get name from recorded audio and remove .wav extension to store image with same name
        image_name, extension = os.path.splitext(os.path.basename(recorded_audio_path))
        image_directory = "data/images/"
        file_extension = ".jpg"

        # Save the single captured frame as an image
        image_path = os.path.join(image_directory, f"{image_name}{file_extension}")
        # cv2.imwrite(image_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

        return image_path

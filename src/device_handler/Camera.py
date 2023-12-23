import cv2
import os


class Camera:
    def __init__(self, camera_index=-1):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if not self.cap.isOpened():
            raise Exception("Camera could not be opened.")

    def is_opened(self):
        return self.cap.isOpened()

    def release(self):
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            return None

    def capture_image(self, recorded_audio_path):
        frame = self.get_frame()

        if frame is None:
            raise Exception("Error while loading image from stream.")

        # Get name from recorded audio and remove .wav extension to store image with same name
        image_name, extension = os.path.splitext(os.path.basename(recorded_audio_path))
        image_directory = "data/images/"
        file_extension = ".jpg"

        # Save the single captured frame as an image
        image_path = os.path.join(image_directory, f"{image_name}{file_extension}")
        # cv2.imwrite(image_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        cv2.imwrite(image_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), [int(cv2.IMWRITE_JPEG_QUALITY), 100])

        return image_path

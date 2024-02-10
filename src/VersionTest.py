"""
Author: Manuel Keck
"""
from PIL import Image
import matplotlib.pyplot as plt
import os.path
import cv2
from Settings import ROOT_DIR
from src.train_model.TrainModelHelpers import resize_image

# Bild laden
image_path = os.path.join(ROOT_DIR, "data/images/training/C/C-142.jpg")

bgr_image = cv2.imread(image_path)

# Konvertierung von BGR zu RGB mit OpenCV
rgb_image = resize_image(cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB))

# Bild anzeigen
cv2.imshow("Gitarrenakkord: C-Dur", rgb_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

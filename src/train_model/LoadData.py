"""
Author: Manuel Keck
"""
import os.path
import cv2
import numpy as np

from Settings import IMAGE_DIR
from src.train_model.Dataset import Dataset
from src.train_model.HandDetection import detect_hand
from src.train_model.TrainModelHelpers import get_sub_folders, resize_image
from PIL import Image


def create_heatmaps_list(dataset) -> list:
    heatmaps_list: list = []  # list of lists containing 21 heatmap numpy arrays
    no_landmarks_found_counter = 0

    # for sample in dataset.data_samples:
    for image in dataset:
        # image = cv2.cvtColor(sample.image, cv2.COLOR_BGR2RGB)
        tmp_list = detect_hand(image)
        heatmaps_list.append(tmp_list)
        if tmp_list[1] == 1:
            no_landmarks_found_counter += 1

    # print(f"Amount of no landmarks found: {no_landmarks_found_counter}/{len(dataset.data_samples)}")
    print(f"Amount of no landmarks found: {no_landmarks_found_counter}/{len(dataset)}")
    return heatmaps_list


def convert_img_paths_to_numpy_arrays(list_of_lists) -> list:
    images_list: list = []

    for list_item in list_of_lists:
        for image_path in list_item:
            tmp_img = np.asarray(Image.open(image_path))
            image = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2RGB)
            images_list.append(image)

    pass
    return images_list


def load_full_size_images(folder_path) -> list:
    images: list = []  # List of lists containing paths to images

    # Loop through all dirs to append image paths to image_files
    sub_folders = get_sub_folders(folder_path)
    for sub_folder in sub_folders:
        tmp_dir = os.path.join(folder_path, sub_folder)
        chord_image_list = [os.path.join(tmp_dir, img) for img in os.listdir(tmp_dir) if img != 'info.json']
        images.append(chord_image_list)

    pass
    return images


def add_black_boarders(images: list) -> list:
    resized_images = []
    for image in images:
        resized_images.append(resize_image(image))

    return resized_images


def split_list_of_resized_full_size_images(images: list, amount_of_parts) -> list:
    images_list_len = len(images)
    part_size = images_list_len // amount_of_parts

    split_list = []

    for i in range(amount_of_parts):
        start_index = i * part_size
        end_index = (i + 1) * part_size
        tmp_split_list = images[start_index:end_index]
        split_list.append(tmp_split_list)

    return split_list


print("Loading training data...")
train_images_path = os.path.join(IMAGE_DIR, "training/")
train_dataset = Dataset(train_images_path)
print("Training data loaded.")

print("Loading list of full size images paths...")
list_of_list_with_img_paths = load_full_size_images(train_images_path)
print("Full size images paths loaded.")

print("Loading list of full size images...")
list_of_full_size_images = convert_img_paths_to_numpy_arrays(list_of_list_with_img_paths)
print("Full size images loaded.")

print("Loading list of full size images with black boarders (shape: 640x640)")
list_of_squared_images = add_black_boarders(list_of_full_size_images)
print("List loaded.")
pass

# print("Split list due to resource limitation (RAM)...")
# parts = 100
# split_list = split_list_of_resized_full_size_images(list_of_squared_images, parts)
# print(f"List split into {parts} parts.")
# counter = 0
# train_dataset_heatmaps = []
# # for part in split_list:
# while counter < parts:
#     print(f"Loading heatmaps from resized images part {counter+1}...")
#     tmp_item = create_heatmaps_list(split_list[counter])
#     train_dataset_heatmaps.append(tmp_item)
#     print(f"Finished with loading heatmaps for part {counter+1}.")
#     counter += 1
list_of_heatmaps = create_heatmaps_list(train_dataset)
print("Heatmaps loaded.")


pass

test_images_path = os.path.join(IMAGE_DIR, "testing/")
test_dataset = Dataset(test_images_path)

val_images_path = os.path.join(IMAGE_DIR, "validation/")
val_dataset = Dataset(val_images_path)

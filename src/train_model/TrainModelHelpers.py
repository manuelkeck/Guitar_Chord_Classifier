"""
Author: Manuel Keck
This file contains several functions which are needed/helpful preparations
to get an own trained model.
"""
import os
import random
import shutil
import cv2
import numpy as np

from Settings import IMAGE_DIR
from src.data.ImageHelpers import get_index

# Global definition needed to calculate 10 % for split function more accurately
amount_of_images = 0


def resize_image(image):
    """
    This function returns a single image resized to 224x224 and
    with black paddings on top and bottom to avoid distorting
    original image.
    param: return: Squared image with 16:9 original image and black boarders
    """
    input_shape = [224, 224, 3]

    # Scaling factors
    scale_x = input_shape[0] / image.shape[1]
    scale_y = input_shape[1] / image.shape[0]

    scale_factor = min(scale_x, scale_y)

    new_width = int(image.shape[1] * scale_factor)
    new_height = int(image.shape[0] * scale_factor)

    # Scale image
    resized_image = cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA
    )

    # This is to create black boarders because 16:9 image will be resized to 1:1
    padded_image = np.zeros((input_shape[0], input_shape[1], input_shape[2]), dtype=np.uint8)

    # Center image within black squared image (where image will be copied in
    x_offset = (padded_image.shape[1] - resized_image.shape[1]) // 2
    y_offset = (padded_image.shape[0] - resized_image.shape[0]) // 2

    # Copy image in padded_image
    padded_image[y_offset:y_offset + resized_image.shape[0],
    x_offset:x_offset + resized_image.shape[1]] = resized_image

    # img = cv2.imread(padded_image, 0)
    # print(f"Size of image: {padded_image.shape}")
    # plt.imshow(padded_image)
    # plt.show()

    return padded_image


def split_dataset():
    folder = f"{IMAGE_DIR}training"
    target_test = f"{IMAGE_DIR}testing"
    target_val = f"{IMAGE_DIR}validation"

    create_folder(target_test)
    create_folder(target_val)

    folder_sub_folder = get_sub_folders(folder)

    pass

    # Testing dataset
    for sub_folder in folder_sub_folder:
        # e.g. ../images/testing/A
        new_sub_folder = f"{target_test}/{sub_folder}"
        # e.g. ../images/training/A
        tmp_folder = f"{folder}/{sub_folder}"
        # Create folder at ../images/testing/ with name A if not exists
        create_folder(new_sub_folder)
        # Randomly move 10% to previously created folder
        move_images_randomly(tmp_folder, new_sub_folder)

    # Validation dataset
    for sub_folder in folder_sub_folder:
        new_sub_folder = f"{target_val}/{sub_folder}"
        tmp_folder = f"{folder}/{sub_folder}"
        create_folder(new_sub_folder)
        move_images_randomly(tmp_folder, new_sub_folder)


def create_folder(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created folder: {path}")


def move_images_randomly(folder: str, target: str):
    list_of_images = [file for file in os.listdir(folder) if file.lower().endswith(('.jpg', '.jpeg'))]
    amount = get_index(f"{folder}/") - 2
    calculated_amount = int(amount * 0.1)

    random_selection = random.sample(list_of_images, calculated_amount)

    # Move images
    for image in random_selection:
        image_path = os.path.join(folder, image)
        target_path = os.path.join(target, image)
        shutil.move(image_path, target_path)


def get_amount_of_images():
    folder_testing = f"{IMAGE_DIR}testing/"
    folder_training = f"{IMAGE_DIR}training/"
    folder_validation = f"{IMAGE_DIR}validation/"

    # Get all directories
    folder_testing_elements = get_sub_folders(folder_testing)
    folder_training_elements = get_sub_folders(folder_training)
    folder_validation_elements = get_sub_folders(folder_validation)

    # Get all amounts
    folder_testing_amount = count_images_in_folder(folder_testing, folder_testing_elements)
    folder_training_amount = count_images_in_folder(folder_training, folder_training_elements)
    folder_validation_amount = count_images_in_folder(folder_validation, folder_validation_elements)

    print(f"Total amount of images in testing folder: {folder_testing_amount}")
    print(f"Total amount of images in training folder: {folder_training_amount}")
    print(f"Total amount of images in validation folder: {folder_validation_amount}")
    print(f"= {folder_testing_amount + folder_training_amount + folder_validation_amount}\n")


def get_sub_folders(folder: str):
    folder_all_elements = os.listdir(folder)
    folder_sub_folder = [element for element in folder_all_elements if os.path.isdir(os.path.join(folder, element))]
    return folder_sub_folder


def count_images_in_folder(folder: str, elements: list):
    counter = 0
    for sub_folder in elements:
        tmp_path = os.path.join(folder, sub_folder)
        tmp_path_elements = os.listdir(tmp_path)
        for element in tmp_path_elements:
            tmp_image_path = os.path.join(tmp_path, element)
            if os.path.isfile(tmp_image_path) and element.lower().endswith(('.jpg', '.jpeg')):
                counter += 1
    return counter


def undo_split():
    # Move back images from /testing and /validation to /training
    training_dir = f"{IMAGE_DIR}training"
    testing_dir = f"{IMAGE_DIR}testing"
    validation_dir = f"{IMAGE_DIR}validation"

    # Loop through each sub dir and move images back to root dir
    testing_sub_folders = get_sub_folders(testing_dir)
    validation_sub_folders = get_sub_folders(validation_dir)
    remove_images(testing_sub_folders, testing_dir, training_dir)
    remove_images(validation_sub_folders, validation_dir, training_dir)

    print("Un-split done.")


def remove_images(folders: list, source_dir: str, root_dir: str):
    for sub_folder in folders:
        tmp_path = os.path.join(source_dir, sub_folder)
        for element in os.listdir(tmp_path):
            target_path = os.path.join(root_dir, sub_folder)
            target_path = os.path.join(target_path, element)
            source_path = os.path.join(tmp_path, element)
            shutil.move(source_path, target_path)


def is_split():
    path = f"{IMAGE_DIR}testing/Bm"
    path_elements = os.listdir(path)
    if len(path_elements) == 0:
        return False
    return True

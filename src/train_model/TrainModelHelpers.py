"""
Author: Manuel Keck
This file contains several functions which are needed/helpful preparations
to get an own trained model.
"""
import os
import random
import shutil

from Settings import IMAGE_DIR


def crop_images():
    pass


def get_model():
    # Return google net model
    pass


def split_dataset():
    folder = f"{IMAGE_DIR}training"
    target_test = f"{IMAGE_DIR}testing"
    target_val = f"{IMAGE_DIR}validation"

    create_folder(target_test)
    create_folder(target_val)

    folder_sub_folder = get_sub_folders(folder)

    # Testing dataset
    for sub_folder in folder_sub_folder:
        new_sub_folder = f"{target_test}/{sub_folder}"
        tmp_folder = f"{folder}/{sub_folder}"
        create_folder(new_sub_folder)
        move_images_randomly(tmp_folder, new_sub_folder)

    # Validation dataset
    for sub_folder in folder_sub_folder:
        new_sub_folder = f"{target_val}/{sub_folder}"
        tmp_folder = f"{folder}/{sub_folder}"
        create_folder(new_sub_folder)
        move_images_randomly(tmp_folder, new_sub_folder)


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created folder: {path}")
    else:
        print(f"Folder '{path}' found.")


def move_images_randomly(folder: str, target: str):
    list_of_images = [file for file in os.listdir(folder) if file.lower().endswith(('.jpg', '.jpeg'))]
    print(f"List of all images: ")
    calculated_amount = int(len(list_of_images) * 0.1)
    print(f"Calculated amount: {calculated_amount}")
    random_selection = random.sample(list_of_images, calculated_amount)

    # Move images
    for image in random_selection:
        image_path = os.path.join(folder, image)
        target_path = os.path.join(target, image)
        shutil.move(image_path, target_path)


def get_amount_of_images():
    folder_testing = f"{IMAGE_DIR}/testing/"
    folder_training = f"{IMAGE_DIR}/training/"
    folder_validation = f"{IMAGE_DIR}/validation/"

    # Get all directories
    folder_testing_elements = get_sub_folders(folder_testing)
    folder_training_elements = get_sub_folders(folder_training)
    folder_validation_elements = get_sub_folders(folder_validation)

    folder_testing_amount = 0
    folder_training_amount = 0
    folder_validation_amount = 0

    for sub_folder in folder_testing_elements:
        tmp_path = os.path.join(folder_testing, sub_folder)
        if os.path.isfile(tmp_path) and element.lower().endswith(('.jpg', '.jpeg')):

    print(folder_testing_elements)
    print(folder_training_elements)
    print(folder_validation_elements)


def get_sub_folders(folder):
    folder_all_elements = os.listdir(folder)
    folder_sub_folder = [element for element in folder_all_elements if os.path.isdir(os.path.join(folder, element))]
    return folder_sub_folder

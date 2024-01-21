"""
Author: Manuel Keck
"""
from src.train_model.TrainModelHelpers import split_dataset, undo_split, get_amount_of_images, is_split


def main():
    if is_split():
        print("Data was already split. Will be undone and re-split.")
        undo_split()
        print("\nTotal amount of elements:")
        get_amount_of_images()
    else:
        print("Data was not split.")
    print("Splitting data...")
    split_dataset()
    get_amount_of_images()


if __name__ == '__main__':
    main()

"""
Author: Manuel Keck
"""
from src.train_model.ChordDetectionVGG16 import ChordDetectionVGG16


def main():
    model = ChordDetectionVGG16
    model.test()
    pass


if __name__ == '__main__':
    main()

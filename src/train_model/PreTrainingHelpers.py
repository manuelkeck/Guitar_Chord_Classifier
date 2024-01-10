"""
Author: Manuel Keck
This file contains functions to pre-train a CNN based on GoogLe Net
"""
from src.train_model.TrainModelHelpers import get_model


def transfer_learning():
    # 1. Get GoogLe Net model
    # 2. Remove last layer
    # 3. Remove weights
    # 4. Add own layers at the end of model
    # 5. Re-train model

    google_net = get_model()


    pass

"""
Author: Manuel Keck
"""
import numpy as np
import os.path
from sklearn.metrics import precision_score, recall_score, f1_score
from Settings import ROOT_DIR
from src.train_model.ChordDetectionVGG16 import ChordDetectionVGG16
from src.train_model.LoadData import val_dataset

# Load model
path = os.path.join(ROOT_DIR, "output/vgg/model/vgg16_model_v8.keras")
model = ChordDetectionVGG16()
model.load_model(path)

predictions = model.predict(val_dataset)

# one hot encoding
predictions_encoded = []
for array in predictions:
    max_index = np.argmax(array)
    tmp_array = np.zeros_like(array)
    tmp_array[max_index] = 1
    predictions_encoded.append(tmp_array)

# predicted_labels = np.argmax(predictions, axis=1)

labels_list = [label for _, label in val_dataset]
true_labels = np.concatenate(labels_list, axis=0)
# true_labels = np.argmax(true_labels, axis=1)
# wie bekomme ich gleiche shape?!
pass

precision = precision_score(true_labels, predictions, average='weighted')
recall = recall_score(true_labels, predictions, average='weighted')
f1 = f1_score(true_labels, predictions, average='weighted')

print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

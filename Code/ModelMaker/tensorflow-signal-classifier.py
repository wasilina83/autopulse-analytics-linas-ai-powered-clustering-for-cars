# Klassen und Funktionen importieren
import sys
from typing import Dict, List
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import LabelEncoder
import numpy as np
from DataPraipare import *
import csv
from Trainingparams import data_params, model_params
from scikeras.wrappers import KerasClassifier
from sklearn.metrics import precision_score, f1_score

# Zusätzliche Imports für Optimizer
from keras.optimizers import SGD, Adam, Adadelta, RMSprop

# Lokale Imports
sys.path.insert(0, r'Code\DataMaker')
from SignalGenerator import signal_functions, noise_beta
from GenDataPath import noise_levels

data_dir_1 = r'Daten\Trainingsdaten\Ansauglufttemperatur'
data_dir_3 =r'Daten\Trainingsdaten\Lambdasonde'
data_dir_2 =r'Daten\Trainingsdaten\Luftmassenmesser'
attribute = 'cluster'
noise_type = None

# Laden Sie den Datensatz
path_dict_1 = red_file_path_dict(gen_dir_dict(data_dir_2, attribute, noise_type), data_params['data_size']/100)
# path_dict_2 = red_file_path_dict(gen_dir_dict(data_dir_2, attribute, noise_type), data_params['data_size']/100)
# path_dict_3 = red_file_path_dict(gen_dir_dict(data_dir_3, attribute, noise_type), data_params['data_size']/100)
data_1 = from_file_to_data(path_dict_1)
# data_2 = from_file_to_data(path_dict_2)
# data_3 = from_file_to_data(path_dict_3)
data = data_1
# data = data_1.append(data_2, ignore_index=True)
# data = data.append(data_3, ignore_index=True)
print(type(data))

# In Test- und Trainingsdaten aufteilen
y = data['label']
X = data.drop('label', axis=1)

# Ausgabevariable kodieren
encoder = LabelEncoder()
encoder.fit(y)
encoded_Y = encoder.transform(y)
dummy_y = tf.keras.utils.to_categorical(encoded_Y)
print(dummy_y)

X_train, X_test, y_train, y_test = train_test_split(X, dummy_y, test_size=data_params['test_size'], random_state=data_params['random_state'])
print(len(X_train.columns))

# Model erstellen
model = Sequential()
model.add(Dense(256, input_dim=len(X_train.columns) ,activation="relu"))
model.add(Dense(128, activation="relu"))
model.add(BatchNormalization())
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(3, activation="softmax"))
model.compile(Adam(learning_rate=0.0005), "categorical_crossentropy", metrics=["accuracy"])

model.build()
model.summary()

# Model trainieren
history = model.fit(X_train, y_train, verbose=1, batch_size=32, epochs=500, validation_data=(X_test, y_test))

# Vorhersagen und Evaluierung
y_pred_prob = model.predict(X_test)
y_pred_class = np.argmax(y_pred_prob, axis=1)
y_pred = model.predict(X_test)
y_test_class = np.argmax(y_test, axis=1)

# Confusion Matrix und Classification Report
conf_matrix = confusion_matrix(y_test_class, y_pred_class)
class_report = classification_report(y_test_class, y_pred_class)

print("Confusion Matrix:\n", conf_matrix)
print("Classification Report:\n", class_report)
print(f"\ny_test_class, y_pred_class, zero_division: {classification_report(y_test_class, y_pred_class, zero_division=1)}")


# Calculate precision and F-score with zero_division parameter
precision = precision_score(y_test_class, y_pred_class, average='weighted', zero_division=1)
f_score = f1_score(y_test_class, y_pred_class, average='weighted', zero_division=1)

# Print or use the precision and F-score as needed
print("Weighted Precision:", precision)
print("Weighted F-score:", f_score)
# Plot Lernkurven
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Modellgenauigkeit')
plt.xlabel('Epochen')
plt.ylabel('Genauigkeit')
plt.legend(['Training', 'Validierung'], loc='upper left')
plt.savefig('Dokumentation/Model/Modellgenauigkeit.png')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Modellverlust')
plt.xlabel('Epochen')
plt.ylabel('Verlust')
plt.legend(['Training', 'Validierung'], loc='upper left')
plt.savefig('Dokumentation/Model/Modellverlust.png')
plt.show()
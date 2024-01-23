import os
import sys
from typing import Dict, List
import random
import logging
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, BatchNormalization
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np
from DataPraipare import *
import csv

sys.path.insert(0, r'Code\DataMaker')
from SignalGenerator import signal_functions, noise_beta
from GenDataPath import noise_levels

data_dir = r'Daten\Trainingsdaten\Ansauglufttemperatur'
attribute = 'cluster'
noise_type = None

# Lade Daten und beschrifte Daten
path_dict = red_file_path_dict(gen_dir_dict(data_dir, attribute), 0.1)
data = from_file_to_data(path_dict)
print(type(data))

with open('daten_lukas.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(data.columns)

    # Write rows
    for index, row in data.iterrows():
        csv_writer.writerow(row)
                
# In Test- und Trainingsdaten aufteilen
X_train, X_test, y_train, y_test = train_test_split(data.drop('label', axis=1), data['label'], test_size=0.33, random_state=42)
print(len(X_train.columns))

# Modell definieren
model = Sequential([
    Dense(256, activation='relu'),
    BatchNormalization(),
    Dense(128, activation='relu'),
    BatchNormalization(),
    Dense(64, activation='relu'),
    Dense(3)
])

optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

# Early Stopping hinzufügen
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Learning Rate Scheduler hinzufügen
def lr_schedule(epoch):
    return 0.001 * np.exp(-epoch / 10)

lr_scheduler = tf.keras.callbacks.LearningRateScheduler(lr_schedule)

# Training mit Early Stopping und Learning Rate Scheduler
hist = model.fit(X_train, y_train, epochs=200, validation_data=(X_test, y_test), callbacks=[early_stopping, lr_scheduler])
model.summary()

logdir = r'Dokumentation\Model'
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)

# Softmax Layer hinzufügen
probability_model = Sequential([model, tf.keras.layers.Softmax()])
predictions = probability_model.predict(X_test)

# Confusion Matrix und Classification Report erstellen
y_pred = np.argmax(predictions, axis=1)
cm = confusion_matrix(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)
print("Confusion Matrix:\n", cm)
print("Classification Report:\n", classification_rep)

# Plot der Training Metrics
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
axes[0].plot(hist.history['loss'], color='teal', label='Training Loss')
axes[0].plot(hist.history['val_loss'], color='orange', label='Validation Loss')
axes[0].set_title('Loss', fontsize=16)
axes[0].legend(loc="upper left")

axes[1].plot(hist.history['accuracy'], color='teal', label='Training Accuracy')
axes[1].plot(hist.history['val_accuracy'], color='orange', label='Validation Accuracy')
axes[1].set_title('Accuracy', fontsize=16)
axes[1].legend(loc="upper left")

title = f"Training Metrics: epochs={lr_scheduler}, batch_size={batch_size} model = Sequential()\n model.add(Dense(units=256, activation=relu))\n model.add(BatchNormalization())\n model.add(Dense(units=128, activation=relu))\n model.add(BatchNormalization())\n model.add(Dense(units=64, activation=relu))\n model.add(Dense(units=3))"
fig.suptitle(title, fontsize=20)

plt.tight_layout()
plt.savefig(r'Dokumentation\Model\noise-classifier_2hep_4ley-BatchNormalization_1dat.png')

model.save(os.path.join('Modelle', 'noise-classifier_2hep_4ley-BatchNormalization_1pad.h5'))
plt.show()

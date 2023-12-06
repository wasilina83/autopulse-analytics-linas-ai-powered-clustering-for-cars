import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from sklearn.metrics import accuracy_score
import cv2
import imghdr
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
import os
import pandas as pd

data_dir = 'data' 

def check_and_remove_non_csv(data_dir):
    not_csv_exts = ['jpeg', 'jpg', 'bmp', 'png']
    for csv_class in os.listdir(data_dir):
        for csv_file in os.listdir(os.path.join(data_dir, csv_class)):
            csv_path = os.path.join(data_dir, csv_class, csv_file)
            try:
                fimg = cv2.imread(csv_path)
                tip = imghdr.what(csv_path)
                if tip in not_csv_exts:
                    print('CSV not in ext list {}'.format(csv_path))
                    os.remove(csv_path)
            except Exception as e: 
                print('Issue with CSV {}'.format(csv_path))

def from_file_to_good_data(data_dir):
    good_data = []

    for filename in os.listdir(os.path.join(data_dir, 'good')):
        if filename.endswith('.csv'):
            csv_path = os.path.join(data_dir, 'good', filename)
            good_df = pd.read_csv(csv_path)

            # Erstelle einen neuen DataFrame für jede CSV-Datei
            combined_df = pd.DataFrame({'signal': good_df['signal']})
            combined_df = combined_df.transpose()

            # Füge den aktuellen DataFrame zur Liste hinzu
            good_data.append(combined_df)

    return good_data

def from_file_to_bad_data(data_dir):
    bad_data = []
    for filename in os.listdir(os.path.join(data_dir, 'bad')):
        if filename.endswith('.csv'):
            csv_path = os.path.join(data_dir, 'bad', filename)
            bad_df = pd.read_csv(csv_path)

            # Erstelle einen neuen DataFrame für jede CSV-Datei
            combined_df = pd.DataFrame({'signal': bad_df['signal']})
            combined_df = combined_df.transpose()

            # Füge den aktuellen DataFrame zur Liste hinzu
            bad_data.append(combined_df)

    return bad_data

def label_data(data, label):
    for df in data:  
        df['label'] = label
    print(data)
    return data

# Überprüfe und entferne nicht benötigte Bilder
check_and_remove_non_csv(data_dir)

# Lade Daten
good_data = from_file_to_good_data(data_dir)
bad_data = from_file_to_bad_data(data_dir)

# Beschrifte Daten
good_data_labeled = label_data(good_data, 1)  # 'good' mit Label 1
bad_data_labeled = label_data(bad_data, 0)    # 'bad' mit Label 0
all_data = pd.concat(good_data_labeled + bad_data_labeled, ignore_index=True)
print(all_data)
X_train, X_test, y_train, y_test = train_test_split(all_data.drop('label', axis=1), all_data['label'], test_size=0.2, random_state=42)

model = Sequential()
model.add(Dense(units=32, activation='relu', input_dim=len(X_train.columns)))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary() 
logdir='logs'
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)

hist = model.fit(X_train, y_train, epochs=200, batch_size=32, use_multiprocessing=True, validation_data=(X_test, y_test))

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))


axes[0].plot(hist.history['loss'], color='teal', label='Training Loss')
axes[0].plot(hist.history['val_loss'], color='orange', label='Validation Loss')
axes[0].set_title('Loss', fontsize=16)
axes[0].legend(loc="upper left")


axes[1].plot(hist.history['accuracy'], color='teal', label='Training Accuracy')
axes[1].plot(hist.history['val_accuracy'], color='orange', label='Validation Accuracy')
axes[1].set_title('Accuracy', fontsize=16)
axes[1].legend(loc="upper left")


fig.suptitle('Training Metrics', fontsize=20)


plt.tight_layout()

plt.savefig('Signalclassifier-tain.png')
plt.show()
model.save(os.path.join('models','Signalclassifier.h5'))
     

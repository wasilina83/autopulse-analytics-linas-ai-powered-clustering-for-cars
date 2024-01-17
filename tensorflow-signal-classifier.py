import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from sklearn.metrics import accuracy_score
from CreateData2 import *
import cv2
import imghdr
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split



 
data_dir = 'data' 
not_csv_exts = ['jpeg','jpg', 'bmp', 'png']
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




bad_data = pd.DataFrame()

def from_file_to_good_pivot(data_dir):
    good_data = pd.DataFrame()
    for filename in os.listdir(os.path.join(data_dir, 'good')):
        if filename.endswith('.csv'):
            csv_path = os.path.join(data_dir, 'good', filename)
            good_data = pd.concat([good_data, pd.read_csv(csv_path)])

    # Duplikate entfernen (falls noch nicht entfernt)
    good_data.drop_duplicates(subset='time', inplace=True)

    # Pivot-Operation für jede 'signal'-Spalte separat durchführen
    good_data_pivoted = good_data.pivot(index='time', columns='signal', values='signal')

    # Die Multi-Index-Spalten entfernen und DataFrame neu indexieren

    good_data_pivoted.reset_index(inplace=True)

    print(f'good_data_pivoted: {good_data_pivoted}')
    return good_data_pivoted


good_data_pivoted = from_file_to_good_pivot(data_dir)

for filename in os.listdir(os.path.join(data_dir, 'bad')):
    if filename.endswith('.csv'):
        bad_data = pd.concat([bad_data, pd.read_csv(os.path.join(data_dir, 'bad', filename))])
        #bad_data.drop_duplicates(subset='time', inplace=True)
        bad_data_pivoted = bad_data.pivot_table(index='time',aggfunc='mean')
        # Die Multi-Index-Spalten entfernen und DataFrame neu indexieren
        good_data_pivoted.columns = good_data_pivoted.columns.droplevel(0)
        good_data_pivoted.reset_index(inplace=True)
print(good_data_pivoted)

for df in good_data_pivoted:
    df['label'] = 1  # 1 für "gut"

for df in bad_data:
    df['label'] = 0  # 0 für "schlecht"


all_data = pd.concat(good_data + bad_data, ignore_index=True)
# data_pivoted = all_data.pivot(index='time', columns='signal')

# # Die Multi-Index-Spalten entfernen und DataFrame neu indexieren
# data_pivoted.columns = data_pivoted.columns.droplevel(0)
# data_pivoted.reset_index(inplace=True)
# print(data_pivoted)
# X_train, X_test, y_train, y_test = train_test_split(all_data.drop('label', axis=1), all_data['label'], test_size=0.2, random_state=42)

# model = tf.keras.Sequential([
#     tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1:],)),
#     tf.keras.layers.Dense(1, activation='sigmoid')
# ])

# model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
# model.summary() 
# logdir='logs'
# tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)

# hist = model.fit(X_train, y_train, epochs=20, batch_size=32, use_multiprocessing=True, validation_data=(X_test, y_test))

# fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))


# axes[0].plot(hist.history['loss'], color='teal', label='Training Loss')
# axes[0].plot(hist.history['val_loss'], color='orange', label='Validation Loss')
# axes[0].set_title('Loss', fontsize=16)
# axes[0].legend(loc="upper left")


# axes[1].plot(hist.history['accuracy'], color='teal', label='Training Accuracy')
# axes[1].plot(hist.history['val_accuracy'], color='orange', label='Validation Accuracy')
# axes[1].set_title('Accuracy', fontsize=16)
# axes[1].legend(loc="upper left")


# fig.suptitle('Training Metrics', fontsize=20)


# plt.tight_layout()
# plt.show()
# plt.savefig('Signalclassifier-tain.png')

# model.save(os.path.join('models','Signalclassifier.h5'))
     

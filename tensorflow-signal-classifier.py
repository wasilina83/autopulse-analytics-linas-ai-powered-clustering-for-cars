import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from sklearn.metrics import accuracy_score
from CreateData import *
import cv2
import imghdr
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split



 
data_dir = 'data' 
# not_csv_exts = ['jpeg','jpg', 'bmp', 'png']
# for csv_class in os.listdir(data_dir):
#     for csv_file in os.listdir(os.path.join(data_dir, csv_class)):
#         csv_path = os.path.join(data_dir, csv_class, csv_file)
#         try:
#             fimg = cv2.imread(csv_path)
#             tip = imghdr.what(csv_path)
#             if tip in not_csv_exts:
#                 print('CSV not in ext list {}'.format(csv_path))
#                 os.remove(csv_path)
#         except Exception as e: 
#             print('Issue with CSV {}'.format(csv_path))  



good_data = []
bad_data = []

for filename in os.listdir(os.path.join(data_dir, 'good')):
    if filename.endswith('.csv'):
        csv_path = os.path.join(data_dir, 'good', filename)
        print(csv_path)
        good_data.append(pd.read_csv(csv_path))
        print(good_data)

for filename in os.listdir(os.path.join(data_dir, 'bad')):
    if filename.endswith('.csv'):
        bad_data.append(pd.read_csv(os.path.join(data_dir, 'bad', filename)))

for df in good_data:
    df['label'] = 1  # 1 für "gut"

for df in bad_data:
    df['label'] = 0  # 0 für "schlecht"


all_data = pd.concat(good_data + bad_data, ignore_index=True)
for data in all_data:
    print(data)
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
     

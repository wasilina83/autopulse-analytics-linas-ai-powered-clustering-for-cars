import os
import sys
from typing import Dict, List
import random
import logging
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from sklearn.metrics import accuracy_score
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split


sys.path.insert(0, r'Code\DataMaker')
from SignalGenerator import signal_functions, noise_beta
from GenDataPath import noise_levels

def gen_dir_dict(data_dir: str, attribute: str, noise_type=None) -> Dict[str, List[str]]:
    file_path_dict = {}
    path_dict = {}

    for dirpath, dirnames, filenames in os.walk(data_dir):
        for dirname in dirnames:
            wanted_dir = os.path.join(dirpath, dirname)
            
            if attribute == 'cluster':
                for noise_type in noise_beta:
                    if noise_type in wanted_dir:
                        for noise_level_name in noise_levels:
                            if noise_levels[noise_level_name] != 0 and noise_level_name in wanted_dir:
                                label_key = f"{noise_type}"
                                if label_key not in file_path_dict:
                                    file_path_dict[label_key] = []

                                for _, _, filenames in os.walk(wanted_dir):
                                    for filename in filenames:
                                        if filename.endswith('.csv'):
                                            file_dir = os.path.join(wanted_dir, filename)
                                            file_path_dict[label_key].append(file_dir)

                no_noise_label_key = "no_noise"
                no_noise_dir = r"Daten\Trainingsdaten\Ansauglufttemperatur\Rosa\Rauschen_0"
                no_noise_dict = {no_noise_label_key: []}

                for _, _, no_noise_filenames in os.walk(no_noise_dir):
                    for no_noise_filename in no_noise_filenames:
                        if no_noise_filename.endswith('.csv'):
                            no_noise_file_dir = os.path.join(no_noise_dir, no_noise_filename)
                            no_noise_dict[no_noise_label_key].append(no_noise_file_dir)

                path_dict = file_path_dict
                
            elif attribute == 'regression':
                if noise_type in ['Rot', 'Weis', 'Rosa']:
                    for dirname in dirnames:
                        if noise_type.capitalize() in dirname:
                            wanted_dir = os.path.join(dirpath, dirname)
                            for noise_level_name in noise_levels:
                                dir_path = os.path.join(wanted_dir, noise_level_name)

                                if noise_level_name in dir_path:
                                    label_key = noise_levels[noise_level_name]
                                    if label_key not in file_path_dict:
                                        file_path_dict[label_key] = []

                                    for _, _, filenames in os.walk(dir_path):
                                        for filename in filenames:
                                            if filename.endswith('.csv'):
                                                file_dir = os.path.join(dir_path, filename)
                                                file_path_dict[label_key].append(file_dir)

                    path_dict = file_path_dict

                else:
                    raise ValueError("Invalid attribute. Use 'Rot', 'Weis', 'Rosa'")  
            else:
                raise ValueError("Invalid attribute. Use 'cluster' or 'regression'.")

    return path_dict

data_dir = r'Daten\Trainingsdaten\Ansauglufttemperatur'
attribute = 'cluster'
#noise_type = 'Rot'
noise_type = None

# logging
log_filename = r'Dokumentation\TreainigsdatenAuswahl.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

file_path_dict = gen_dir_dict(data_dir, attribute, noise_type)
num_random_elements = int(min(len(value) for value in file_path_dict.values())/2)
red_file_path_dict ={}
for key, value in file_path_dict.items():
    random_elements = random.sample(value, num_random_elements)
    logging.info(f"Key: {key}, Number of Elements: {len(random_elements)}")
    #logging.info(f"Key: {key}, Number of Elements: {len(file_path_dict)}")
    for file_path in random_elements:
        logging.info(f"  {file_path}")
    
    

print(f"Log written to {log_filename}")

def label_data(data, label): 
    data['label'] = label
    print(data)
    return data

def from_file_to_data(path_dict):
    data = []
    for key in path_dict:
        label= noise_beta[key]
        #print(f"lable: {lable}, typ: {type(lable)}, key: {key}")
        for path in path_dict[key]:
            df= pd.read_csv(path)
            combined_df = pd.DataFrame({'signal': df['signal']})
            combined_df = combined_df.transpose()
            label_data(combined_df, label)
            data.append(combined_df)
        
    return data

# Lade Daten und beschrifte Daten
data = from_file_to_data(random_elements)

#in test und tainigs daten aufteilen
X_train, X_test, y_train, y_test = train_test_split(data.drop('label', axis=1), data['label'], test_size=0.33, random_state=42)
print(len(X_train.columns))
model = Sequential()
model.add(Dense(units=32, activation='relu', input_dim=len(X_train.columns)))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=3, activation='sigmoid'))
model.add(Dense(3))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary() 
logdir=r'Dokumentation\Model'
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

title= f"Training Metrics: epochs=200, batch_size=32\n model = Sequential()\n model.add(Dense(units=32, activation=relu, input_dim=len(X_train.columns)))\n model.add(Dense(units=64, activation=relu))\n model.add(Dense(units=3, activation=sigmoid))\n model.add(Dense(3))' fig.suptitle(title, fontsize=20)"


plt.tight_layout()

plt.savefig(r'Dokumentation\Model\noise-classifier_1.png')

model.save(os.path.join('Modelle','noise-classifier_1.h5'))
plt.show()  







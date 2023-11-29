import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from sklearn.metrics import accuracy_score
from CreateData import *

#get data from funktion
signals_list = generate_labled_signals_list(generate_rectangle_signal, None)
signals_list.append(generate_labled_signal_with_noise_list(generate_rectangle_signal, None))
print(signals_list)
#df = pd.DataFrame(signals_list, columns=['column_name'])

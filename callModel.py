from tensorflow.keras.models import load_model
import os

# Pfade zu deinem gespeicherten Modell
model_path = os.path.join('models', 'Signalclassifier.h5')

# Modell laden
loaded_model = load_model(model_path)
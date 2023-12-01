import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import joblib
import os
import matplotlib as plt

# Schritt 1: Dateinamen aus den Verzeichnissen holen
good_files = [os.path.join('data/good', file) for file in os.listdir('data/good') if file.endswith('.csv')]
bad_files = [os.path.join('data/bad', file) for file in os.listdir('data/bad') if file.endswith('.csv')]

#get & label data  
good_data = pd.concat([pd.read_csv(file) for file in good_files])
bad_data = pd.concat([pd.read_csv(file) for file in bad_files])

good_data['label'] = 'good'
bad_data['label'] = 'bad'

#use data
data = pd.concat([good_data, bad_data])
X = data.drop('label', axis=1)
y = data['label']

# generate & rain Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.fit_transform(X_test)

model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500)
hist = model.fit(X_train_scaled, y_train)

# eval model
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f'Genauigkeit des Modells: {accuracy}')

# sichern model
joblib.dump(model, 'trained_model.joblib')

# Schritt 6: Neue Daten vorhersagen
new_data = pd.read_csv('csv_file.csv')
new_data_scaled = scaler.transform(new_data)
predicted_labels = model.predict(new_data_scaled)
print(predicted_labels)
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

# Loss
axes[0].plot(hist.history['loss'], color='teal', label='Training Loss')
axes[0].plot(hist.history['val_loss'], color='orange', label='Validation Loss')
axes[0].set_title('Loss', fontsize=16)
axes[0].legend(loc="upper left")

# Accuracy
axes[1].plot(hist.history['accuracy'], color='teal', label='Training Accuracy')
axes[1].plot(hist.history['val_accuracy'], color='orange', label='Validation Accuracy')
axes[1].set_title('Accuracy', fontsize=16)
axes[1].legend(loc="upper left")

# Gemeinsamer Titel für beide Subplots
fig.suptitle('Training Metrics', fontsize=20)

# Layout anpassen
plt.tight_layout()
plt.show()

# Speichern des Plots
plt.savefig('training_metrics.png')
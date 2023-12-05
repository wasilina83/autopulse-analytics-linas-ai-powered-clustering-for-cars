import os
import pandas as pd
import numpy as np
import tensorflow as tf

# Laden Sie Ihr trainiertes Modell
model = tf.keras.models.load_model(os.path.join('models', 'Signalclassifier.h5'))

# Funktion zur Vorhersage für eine einzelne CSV-Datei
def predict_label(csv_path):
    try:
        # Annahme: Ihre CSV-Datei hat dieselbe Struktur wie die, die zum Trainieren verwendet wurde
        new_data = pd.read_csv(csv_path)

        # Vorverarbeitung Ihrer Daten (abhängig von Ihrer Modellvorbereitung)
        # Hier könnten Sie z.B. Funktionen wie das Skalieren der Daten anwenden
        # Beispiel: new_data = preprocess_data(new_data)

        # Vorhersage durchführen
        prediction = model.predict(new_data)

        # Hier können Sie eine Schwellenwertlogik oder ähnliches anwenden, um das endgültige Label zu erhalten
        label = 1 if prediction > 0.5 else 0

        return label

    except Exception as e:
        print(f'Error processing CSV file {csv_path}: {str(e)}')
        return None

# Beispielaufruf für eine CSV-Datei
csv_file_path = r'C:\Users\Engelmann\OneDrive\Dokumente\arbeit\autopulse-analytics-linas-ai-powered-clustering-for-cars\csv_file.csv'  # Ersetzen Sie dies durch den tatsächlichen Pfad Ihrer CSV-Datei
predicted_label = predict_label(csv_file_path)

if predicted_label is not None:
    print(f'Predicted label for {csv_file_path}: {predicted_label}')

import os
from CreateData import *
from SignalGenerator import *
import numpy as np
import time 

def create_project_structure(project_path):
    # Erstelle den Hauptprojektordner
    os.makedirs(project_path, exist_ok=True)

    # Erstelle Unterordner für Daten
    data_path = os.path.join(project_path, "Daten")
    os.makedirs(data_path, exist_ok=True)

    # Erstelle Unterordner für Trainings-, Validierungs- und Testdaten
    split = "Trainingsdaten"
    split_path = os.path.join(data_path, split)
    os.makedirs(split_path, exist_ok=True)

        # Erstelle Unterordner für verschiedene Sensoren
    for sensor in ["Luftmassenmesser"]:
        sensor_path = os.path.join(split_path, sensor)
        os.makedirs(sensor_path, exist_ok=True)
        signal_function =signal_functions[sensor]
            
        # Erstelle Unterordner für verschiedene Arte des Rauschens
        for noise in ["Rosa", "Weis", "Rot"]:
            noise_path = os.path.join(sensor_path, noise)
            os.makedirs(sensor_path, exist_ok=True)
            noise_name = noise
            print(f"noise: {noise}")
                
                # Erstelle Unterordner für verschiedene Rauschstärken
            for noise_level in ["Rauschen_0", "Rauschen_25", "Rauschen_50", "Rauschen_75", "Rauschen_100"]:
                print(f"noise_level: {noise_level}")
                data_path = os.path.join(noise_path, noise_level)
                noise_amplitude = noise_levels[noise_level]
                generate_and_save_signal_loop(signal_function, noise_name, noise_amplitude, data_path)


    # Erstelle Unterordner für Modelle
    models_path = os.path.join(project_path, "Modelle")
    os.makedirs(models_path, exist_ok=True)

    # Erstelle Unterordner für Code
    code_path = os.path.join(project_path, "Code")
    os.makedirs(code_path, exist_ok=True)

    # Erstelle Unterordner für Dokumentation
    docs_path = os.path.join(project_path, "Dokumentation")
    os.makedirs(docs_path, exist_ok=True)
    
noise_levels = {"Rauschen_0" : 0, 
            "Rauschen_25" : .25, 
            "Rauschen_50" : .5, 
            "Rauschen_75" : 0.75, 
            "Rauschen_100" :1}

if __name__ == "__main__":
    project_directory = "c:/Users/Engelmann/OneDrive/Dokumente/arbeit/autopulse-analytics-linas-ai-powered-clustering-for-cars"
    create_project_structure(project_directory)
    print(f"Projektstruktur wurde erfolgreich unter {project_directory} erstellt.")




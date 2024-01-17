import os
import matplotlib as plt
import csv
from SignalGenerator import *
import textwrap
import matplotlib.pyplot

def export_signal_data(time, signal, duration_label, amplitude_label, frequency_label, offset_label, path):
    folder_path = path
    
    os.makedirs(folder_path, exist_ok=True)
    csv_filename = os.path.join(folder_path,  f"signals_data_{duration_label}_{amplitude_label}_{frequency_label}_{offset_label}.csv")
    
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        header = ['time', 'signal']
        csv_writer.writerow(header)
        for i, x in enumerate(time):
            csv_writer.writerow([x, signal[i]])

    # Speichere als PNG-Datei
    myTitle = f"Daten Plot: Signal gegen Zeit\n{duration_label}_{amplitude_label}_{frequency_label}_{offset_label}"
    png_filename = os.path.join(folder_path,  f"signals_data_{duration_label}_{amplitude_label}_{frequency_label}_{offset_label}.png")
    plt.figure()
    plt.plot(time, signal)  # Hier wird das erste Signal geplottet (du kannst anpassen)
    plt.xlabel('Zeit [t]')
    plt.ylabel('Signal [U]')
    plt.title("\n".join(textwrap.wrap(myTitle, 40)))
    (matplotlib.pyplot).tight_layout()
    plt.savefig(png_filename)
    plt.close()

def generate_and_save_signal_loop(signal_function, noise_name, noise_amplitude, path):
    for duration in range(5, 16, 1):
        print(duration)
        for amplitude in range(1, 20, 1):
            for frequency in range(1, 6, 1):
                for offset in range(0, 20, 51): 
                    time, signal = signal_function(duration, amplitude, frequency, offset/10)
                    time, signal_with_noise = add_noise_to_signal(time, signal, noise_name, noise_amplitude)
                    duration_label = f'Signal-duration_{duration}'
                    amplitude_label = f'Signal-amplitude_{amplitude}'
                    frequency_label = f'Signal-frequency_{frequency}'
                    offset_label = f'Signal-offset_{offset}'
                    export_signal_data(time, signal_with_noise, duration_label, amplitude_label, frequency_label, offset_label, path)
    
import os
import matplotlib as plt
import csv
from SignalGenerator import *
import textwrap
import matplotlib.pyplot
import numpy as np

def export_signal_data(time, signal, duration_label, amplitude_label, frequency_label, offset_label, phase_shift_label, path):
    folder_path = path
    
    os.makedirs(folder_path, exist_ok=True)
    csv_filename = os.path.join(folder_path,  f"signals_data_{phase_shift_label}_{amplitude_label}_{frequency_label}_{offset_label}.csv")
    
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        header = ['time', 'signal']
        csv_writer.writerow(header)
        for i, x in enumerate(time):
            csv_writer.writerow([x, signal[i]])

    # Speichere als PNG-Datei
    myTitle = f"Daten Plot: Signal gegen Zeit\n{phase_shift_label}_{amplitude_label}_{frequency_label}_{offset_label}"
    png_filename = os.path.join(folder_path,  f"signals_data_{phase_shift_label}_{amplitude_label}_{frequency_label}_{offset_label}.png")
    plt.figure()
    plt.plot(time, signal)  # Hier wird das erste Signal geplottet (du kannst anpassen)
    plt.xlabel('Zeit [t]')
    plt.ylabel('Signal [U]')
    plt.title("\n".join(textwrap.wrap(myTitle, 40)))
    (matplotlib.pyplot).tight_layout()
    plt.savefig(png_filename)
    plt.close()

def generate_and_save_signal_loop(signal_function, noise_name, noise_amplitude, path):
    duration =5
    for phase_shift in np.arange(0, 2*np.pi, np.pi/4):
        print(f"phase_shift: {phase_shift}")
        for amplitude in range(1, 10, 1):
            print(f"amplitude: {amplitude}")
            for frequency in range(1, 6, 1):
                for offset in range(0, 10, 1): 
                    time, signal = signal_function(duration, amplitude, frequency, offset/10, phase_shift)
                    time, signal_with_noise = add_noise_to_signal(time, signal, noise_name, noise_amplitude)
                    duration_label = f'duration_{duration}'
                    amplitude_label = f'amplitude_{amplitude}'
                    frequency_label = f'frequency_{frequency}'
                    offset_label = f'offset_{offset}'
                    phase_shift_label = f'phase_{phase_shift}'
                    export_signal_data(time, signal_with_noise, duration_label, amplitude_label, frequency_label, offset_label, phase_shift_label, path)
    
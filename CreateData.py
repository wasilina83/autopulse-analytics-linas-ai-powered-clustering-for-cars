import numpy as np
import matplotlib.pyplot as plt
from siglanGen import *
import siglanGen as sig
import csv
import os

def generate_labled_signals_list(signal_function, some_to_input= None):
    signals_list = []
    if some_to_input is not None:    
        dur_min, dur_max, dur_step = map(int, input('dur_min, dur_max, dur_step').split(','))
        amp_min, amp_max, amp_step = map(int, input('amp_min, amp_max, amp_step').split(','))
        fre_min, fre_max, fre_step = map(int, input('fre_min, fre_max, fre_step').split(','))
        samp_min, samp_max, samp_step = map(int, input('samp_min, samp_max, samp_step').split(','))
        of_min, of_max, of_step = map(int, input('of_min, of_max, of_step').split(','))
    else:
        dur_min, dur_max, dur_step = [10,11,1]
        amp_min, amp_max, amp_step = [1,6,1]
        fre_min, fre_max, fre_step = [1,6,1]
        samp_min, samp_max, samp_step = [1000,1500,500]
        of_min, of_max, of_step = [0,3,1] 
    for duration in range(dur_min, dur_max, dur_step):
        for amplitude in range(amp_min, amp_max, amp_step):
            for frequency in range(fre_min, fre_max, fre_step):
                for sampling_rate in range(samp_min, samp_max, samp_step):
                    for offset in range(of_min, of_max, of_step):
                            # Generiere Rechtecksignal
                            time, signal = signal_function(duration, amplitude, frequency, sampling_rate, offset)
                            # Füge das Signal der Liste hinzu, zusammen mit einem Label
                            amplitude_label = f'Signal-amplitude {amplitude}'
                            frequency_label = f'Signal-frequency {frequency}'
                            sampling_rate_label = f'Signal-sampling_rate {sampling_rate}'
                            offset_label = f'Signal-offset {offset}'
                            label = 'good'
                            signals_list.append([time, signal, amplitude_label, frequency_label, sampling_rate_label, offset_label, label])
                            export_signal_data(time, signal, amplitude_label, frequency_label, sampling_rate_label, offset_label, label,)     
    return np.array(signals_list, dtype=object)

def generate_labled_signal_with_noise_list(signal_function,some_to_input = None):
    noise_signals_list = [] 
    if some_to_input != None:
        noise_amplitude = float(input('noise_amplitude'))
        signals_list = generate_labled_signals_list(signal_function, 'foobar')
    else:
        noise_amplitude = .02
        
        signals_list = generate_labled_signals_list(signal_function, some_to_input)
    # Durchlaufe jedes Element in der Liste
    for signal_data in signals_list:
    # Extrahiere die Werte
        time = signal_data[0]
        signal = signal_data[1]
        label = signal_data[-1]  # Der Label-Wert befindet sich am Ende der Liste
        time, noise_signal = generate_signal_with_noise(time, signal, noise_amplitude)
        amplitude_label = signal_data[3]
        frequency_label = signal_data[4]
        sampling_rate_label = signal_data[5]
        offset_label = signal_data[6]
        label = 'good'
        # Aktualisiere die Werte im ursprünglichen Signal-Datenpunkt
        signal_data[1] = noise_signal
        signal_data[-1] = label
        signal_data[0] = time 
        noise_signals_list.append(signal_data)
        export_signal_data(time, noise_signal, amplitude_label, frequency_label, sampling_rate_label, offset_label, label, noise_amplitude)

    return np.array(noise_signals_list, dtype=object)

def export_signal_data(time, signal,  amplitude_label, frequency_label, sampling_rate_label, offset_label, label, noise_amplitude = 0):
    folder_path = os.path.join("data", label)
    os.makedirs(folder_path, exist_ok=True)
    csv_filename = os.path.join(folder_path,  f"signals_data_{amplitude_label}_{frequency_label}_{sampling_rate_label}_{offset_label}_{noise_amplitude}.csv")
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        header = ['time', 'signal']
        csv_writer.writerow(header)
        for i, x in enumerate(time):
            csv_writer.writerow([x, signal[i]])

    # Speichere als PNG-Datei
    png_filename = os.path.join(folder_path,  f"signals_data_{amplitude_label}_{frequency_label}_{sampling_rate_label}_{offset_label}.png")
    plt.figure()
    plt.plot(time, signal)  # Hier wird das erste Signal geplottet (du kannst anpassen)
    plt.savefig(png_filename)
    plt.close()

                        

with open("file_bad.txt", "w") as f_b:
    f_b.write(str(generate_labled_signal_with_noise_list(generate_rectangle_signal, None)))

with open("file_good.txt", "w") as f_g:
    f_g.write(str(generate_labled_signal_with_noise_list(generate_rectangle_signal, None)))

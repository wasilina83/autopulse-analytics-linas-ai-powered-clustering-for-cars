import numpy as np
import matplotlib.pyplot as plt
from siglanGen import generate_rectangle_signal, generate_signal_with_noise

 
    signals_list = []
    for duration in range(1,6,1):
        for amplitude in range(1,6,1):
            for frequency in range(1,6,1):
                for sampling_rate in range(1500,2000,500):
                    for offset in range(0,3,1):
                        # Generiere Rechtecksignal
                            time, rectangle_signal = generate_rectangle_signal(duration, amplitude, frequency, sampling_rate, offset)
                            
                        # Füge das Signal der Liste hinzu, zusammen mit einem Label
                            duration_label = f'Signal-duration {duration}'
                            amplitude_label = f'Signal-amplitude {amplitude}'
                            frequency_label = f'Signal-frequency {frequency}'
                            sampling_rate_label = f'Signal-sampling_rate {sampling_rate}'
                            offset_label = f'Signal-offset {offset}'
                            lable_label = 'good'
                            signals_list.append([time, rectangle_signal, duration_label, amplitude_label, frequency_label, sampling_rate_label, offset_label, lable_label])     

print(signals_list)
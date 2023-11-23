import numpy as np
import matplotlib.pyplot as plt
from siglanGen import generate_rectangle_signal, generate_signal_with_noise

def generate_labled_signals_list(): 
    signals_list = []
    dur_min, dur_max, dur_step = input('dur_min, dur_max, dur_step')
    for duration in range(dur_min, dur_max, dur_step):
        amp_min, amp_max, amp_step = input('amp_min, amp_max, amp_step')
        for amplitude in range(amp_min, amp_max, amp_step):
            fre_min, fre_max, fre_step = input('fre_min, fre_max, fre_step')
            for frequency in range(fre_min, fre_max, fre_step):
                samp_min, samp_max, samp_step = input('samp_min, samp_max, samp_step')
                for sampling_rate in range(samp_min, samp_max, samp_step):
                    of_min, of_max, of_step = input('of_min, of_max, of_step')
                    for offset in range(of_min, of_max, of_step):
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
    return(signals_list)

def generate_labled_signal_with_noise_list(): 
    noise_signals_list = []
    dur_min, dur_max, dur_step = map(int, input('dur_min, dur_max, dur_step').split(','))
    for duration in range(dur_min, dur_max, dur_step):
        amp_min, amp_max, amp_step = map(int, input('amp_min, amp_max, amp_step').split(','))
        for amplitude in range(amp_min, amp_max, amp_step):
            fre_min, fre_max, fre_step = map(int, input('fre_min, fre_max, fre_step').split(','))
            for frequency in range(fre_min, fre_max, fre_step):
                samp_min, samp_max, samp_step = map(int, input('samp_min, samp_max, samp_step').split(','))
                for sampling_rate in range(samp_min, samp_max, samp_step):
                    of_min, of_max, of_step = map(int, input('of_min, of_max, of_step').split(','))
                    for offset in range(of_min, of_max, of_step):
                        # Generiere Rechtecksignal
                            time, rectangle_signal = generate_rectangle_signal(duration, amplitude, frequency, sampling_rate, offset)
                            noise_amplitude = input('noise_amplitude')
                            time, signal_with_noise =generate_signal_with_noise( time, rectangle_signal, noise_amplitude)
                        # Füge das Signal der Liste hinzu, zusammen mit einem Label
                            duration_label = f'Signal-duration {duration}'
                            amplitude_label = f'Signal-amplitude {amplitude}'
                            frequency_label = f'Signal-frequency {frequency}'
                            sampling_rate_label = f'Signal-sampling_rate {sampling_rate}'
                            offset_label = f'Signal-offset {offset}'
                            lable_label = 'bad'
                            noise_signals_list.append([time, signal_with_noise, duration_label, amplitude_label, frequency_label, sampling_rate_label, offset_label, lable_label])     
    return(noise_signals_list)

print(generate_labled_signal_with_noise_list())
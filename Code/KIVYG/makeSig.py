#!/usr/bin/env python3
import matplotlib
import numpy as np
import math
from matplotlib import pyplot as plt
import redpitaya_scpi as scpi
import matplotlib.animation as animation 
from celluloid import Camera
matplotlib.use('Agg')
import time as t
import os

def sin_sig(amplitude, frequency):
    old_gif_path = 'KIVYG/images/animation.gif'
        # Löschen des alten GIF
    if os.path.exists(old_gif_path):
            os.remove(old_gif_path)
    sampling_rate = 16384
    time = np.linspace(0, 1, sampling_rate)*2*np.pi
    signal = amplitude * np.sin(2 * np.pi * (frequency/100) * time)
    fig = plt.figure()
    ax = plt.axes()
    ax.set(xlim=[min(time)-.1, max(time)+.1], ylim=[min(signal)-.1, max(signal)+.1], xlabel='Zeit (sec)', ylabel='Spannung (V)')
    plt.title(f'Dein Signal der Batterie')
    camera = Camera(fig)
    # Berechnen Sie die Anzahl der Schritte basierend auf der Bildrate
    step_count = int(len(time) / 10)
    print(step_count)

    step_size = max(1, step_count)  # Stellen Sie sicher, dass der Schritt mindestens 1 ist
    
    for i in range(0, len(time), step_size):
        ax.plot(time[:i], signal[:i], 'blue')
        plt.pause(0.00001)
        camera.snap()
    animation = camera.animate()
    animation.save('KIVYG/images/animation.gif', writer='PillowWriter', fps=.5)
    plt.close(fig)  # Plot schließen, um sicherzustellen, dass er nicht angezeigt wird
    
    return 0


def saw_sig(amplitude, frequency):
    old_gif_path = 'KIVYG/images/animation.gif'
        # Löschen des alten GIF
    if os.path.exists(old_gif_path):
            os.remove(old_gif_path)
    sampling_rate = 16384
    time = np.linspace(0, 1, sampling_rate)*2*np.pi
    # Generate the saw-up waveform
    duration =1
    period = 1 / (frequency/10)
    cycles = int(duration / period)
    ramp = np.tile(np.linspace(-1, 1, int(period * sampling_rate)), cycles)
    signal = amplitude * ramp[:len(time)]
    fig = plt.figure()
    ax = plt.axes()
    ax.set(xlim=[min(time)-.1, max(time)+.1], ylim=[min(signal)-.1, max(signal)+.1], xlabel='Zeit (sec)', ylabel='Spannung (V)')
    plt.title(f'Dein Signal der Lichtmaschine')
    camera = Camera(fig)
    # Berechnen Sie die Anzahl der Schritte basierend auf der Bildrate
    step_count = int(len(time) / 8)
    print(step_count)
    step_size = max(1, step_count)  # Stellen Sie sicher, dass der Schritt mindestens 1 ist
    
    for i in range(0, len(time), step_size):
        ax.plot(time[:i], signal[:i], 'blue')
        plt.pause(0.00001)
        camera.snap()
    animation = camera.animate()
    animation.save('KIVYG/images/animation.gif', writer='PillowWriter', fps=.5)
    plt.close(fig)  # Plot schließen, um sicherzustellen, dass er nicht angezeigt wird
    return 0


def generate_custom_waveform_and_plot(funk, amplitude, frequency):
    IP = '169.254.6.100'
    rp_s = scpi.scpi(IP)
    func_dict={'Batterie': 'sine',
               'Lichtmaschine':'SAWU'}
    
    signal_functions={'Batterie': sin_sig,
               'Lichtmaschine':saw_sig}
    

    
    wave_form = func_dict[funk]
    freq = frequency
    ampl = amplitude
    signal_functions[funk](amplitude, frequency)

    rp_s.tx_txt('GEN:RST')

    rp_s.tx_txt('SOUR1:FUNC ' + str(wave_form).upper())
    rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(freq))
    rp_s.tx_txt('SOUR1:VOLT ' + str(ampl))

    #Enable output
    rp_s.tx_txt('OUTPUT1:STATE ON')
    rp_s.tx_txt('SOUR1:TRIG:INT')
    rp_s.close()

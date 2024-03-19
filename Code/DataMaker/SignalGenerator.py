import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation 
from celluloid import Camera
import matplotlib
matplotlib.use('Agg')
import time as t
import os

def generate_rectangle_signal(duration=10, amplitude=1, frequency=1, offset=0, phase_shift=0):
    # Generate the rectangular signal with dynamic amplitude
    sampling_rate = 16384
    time = np.linspace(0, duration, duration*sampling_rate)
    signal = offset + amplitude * np.sign(np.sin(2 * np.pi * frequency * time + phase_shift))
    return time, signal

def generate_sine_signal(duration, amplitude=1, frequency=1, offset=0, phase_shift=0):
    sampling_rate = 16384
    time = np.linspace(0, duration, duration*sampling_rate)
    signal = offset + amplitude * np.sin(2 * np.pi * frequency * time + phase_shift)
    return time, signal

def generate_triangle_signal(duration=2, amplitude=1, frequency=1, offset=0, phase_shift=0):
    sampling_rate = 16384
    time = np.linspace(0, duration, duration*sampling_rate)
    signal = offset + amplitude * np.abs((time * frequency - np.floor(0.5 + time * frequency) + phase_shift/(2*np.pi)))
    return time, signal

signal_functions = {
        "Hupe": generate_triangle_signal,
        "Schuhe": generate_rectangle_signal,
        "Gepäck": generate_sine_signal
    }
pron = {
        "Hupe": "der Hupe",
        "Schuhe": "der Schuhe",
        "Gepäck": "des Gepäcks"
    }
 
noise_beta = "lulululu"
def genSigPNG(funk, duration, amplitude, frequency, offset, phase_shift):
    signal_function = signal_functions[funk]
    time, signal = signal_function(duration, amplitude, frequency, offset, phase_shift)
    
    fig = plt.figure()
    ax = plt.axes()
    ax.set(xlim=[min(time)-.1, max(time)+.1], ylim=[min(signal)-.1, max(signal)+.1], xlabel='Zeit (sec)', ylabel='Spannung (V)')
    plt.title(f'Dein Signal {pron[funk]}')
    camera = Camera(fig)
    # Berechnen Sie die Anzahl der Schritte basierend auf der Bildrate
    step_count = int(len(time) / 10)
    step_size = max(1, step_count)  # Stellen Sie sicher, dass der Schritt mindestens 1 ist
    
    for i in range(0, len(time), step_size):
        ax.plot(time[:i], signal[:i], 'blue')
        plt.pause(0.0001)
        camera.snap()
    animation = camera.animate()
    animation.save('GUI/images/animation.gif', writer='PillowWriter', fps=.5)
    plt.close(fig)  # Plot schließen, um sicherzustellen, dass er nicht angezeigt wird
    
    t.sleep(5)
    
    return 0

# Signalparameter und Funktionsaufruf hier anpassen...

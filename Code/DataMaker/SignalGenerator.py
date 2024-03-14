import numpy as np
import matplotlib.pyplot as plt
from random import seed, random
import colorednoise as cn
import math


def generate_rectangle_signal(duration=10, amplitude=1, frequency=1, offset=0, phase_shift=0):
    """
    Generate a rectangular signal.

    Parameters:
    - duration: Duration of the signal in seconds (default is 10).
    - amplitude: Amplitude of the signal (default is 1).
    - frequency: Frequency of the signal in Hertz (default is 1).
    - offset: Offset of the signal (default is 0).
    - phase_shift: Phase shift of the signal in radians (default is 0).

    Returns:
    - time: Time array for the signal.
    - signal: Generated rectangular signal.
    """
    sampling_rate = 16384                   # Number of samples scipi
    time = np.linspace(0, 1, sampling_rate)*2*math.pi

    # Generate the rectangular signal with dynamic amplitude
    signal = offset + amplitude * np.sign(np.sin(frequency * time + phase_shift))

    return time, signal

def generate_sine_signal(duration, amplitude=1, frequency=1, offset=0, phase_shift=0):
    """
    Generate a sine signal.

    Parameters:
    - duration: Duration of the signal in seconds.
    - amplitude: Amplitude of the signal (default is 1).
    - frequency: Frequency of the signal in Hertz (default is 1).
    - offset: Offset of the signal (default is 0).
    - phase_shift: Phase shift of the signal in radians (default is 0).

    Returns:
    - time: Time array for the signal.
    - signal: Generated sine signal.
    """
    sampling_rate = 16384                   # Number of samples
    time = np.linspace(0, 1, sampling_rate)*2*math.pi
    signal = offset + amplitude * np.sin(frequency * time + phase_shift)
    return time, signal

def generate_triangle_signal(duration=2, amplitude=1, frequency=1, offset=0, phase_shift=0):
    """
    Generate a triangle signal.

    Parameters:
    - duration: Duration of the signal in seconds.
    - amplitude: Amplitude of the signal (default is 1).
    - frequency: Frequency of the signal in Hertz (default is 1).
    - offset: Offset of the signal (default is 0).
    - phase_shift: Phase shift of the signal in radians (default is 0).

    Returns:
    - time: Time array for the signal.
    - signal: Generated triangle signal.
    """
    sampling_rate = 16384                   # Number of samples
    time = np.linspace(0, 1, sampling_rate )*2*math.pi
    signal = offset + amplitude * np.abs((time * frequency - np.floor(0.5 + time * frequency) + phase_shift/(2*np.pi)))
    return time, signal


def add_noise_to_signal(time, signal, noise_name, noise_amplitude = .25):
    """
    Added  noise to a generated signal.

    Parameters:
    - time: Time array for the original signal.
    - signal: Values from the original signal.
    - noise_amplitude: Amplitude of the white noise (default is 0.25).
    - noise: canbe choosen of noise_beta as a key "Weis": 0, "Rosa": 1, "Rot": 2
    
    
    Returns:
    - time: Time array for the signal.
    - signal_with_noise: Generated rectangular signal with added white noise.
    """
    beta = noise_beta[noise_name]
    samples = len(time)
    
    noise_signal = noise_amplitude * cn.powerlaw_psd_gaussian(beta, samples)
    # Add white noise to the signal
    signal_with_noise = signal + noise_signal

    return time, signal_with_noise

signal_functions = {
    "Huppe": generate_triangle_signal,
    "Schuhe": generate_rectangle_signal,
    "Gepäck":generate_sine_signal
    }
pron = {
    "Huppe": "der Huppe",
    "Schuhe":"der Schuhe",
    "Gepäck":"des Gepäcks"
    }

def genSigPNG(funk, duration, amplitude, frequency, offset, phase_shift):
    signal_function = signal_functions[funk]
    time, signal = signal_function(duration, amplitude, frequency, offset, phase_shift)
    plt.figure()
    plt.plot(time, signal)
    plt.title(f'Dein Signal {pron[funk]}')
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Amplitude')
    plt.savefig(r'GUI/images/test-1.png')
    return 0
    
    

noise_beta = {
    "Weis": 0,
    "Rosa": 1,
    "Rot": 2
    }


import numpy as np
import matplotlib.pyplot as plt
from random import seed, random
import colorednoise as cn


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
    sampling_rate = 1000
    time = np.arange(0, duration, 1/sampling_rate)

    # Generate the rectangular signal with dynamic amplitude
    signal = offset + amplitude * np.sign(np.sin(2 * np.pi * frequency * time + phase_shift))

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
    sampling_rate = 1000
    time = np.arange(0, duration, 1/sampling_rate)
    signal = offset + amplitude * np.sin(2 * np.pi * frequency * time + phase_shift)
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
    sampling_rate = 1000
    time = np.arange(0, duration, 1/sampling_rate)
    signal = offset + amplitude * np.abs(2 * (time * frequency - np.floor(0.5 + time * frequency) + phase_shift/(2*np.pi)))
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
    "Ansauglufttemperatur": generate_triangle_signal,
    "Luftmassenmesser": generate_rectangle_signal,
    "Lambdasonde":generate_sine_signal
    }


noise_beta = {
    "Weis": 0,
    "Rosa": 1,
    "Rot": 2
    }


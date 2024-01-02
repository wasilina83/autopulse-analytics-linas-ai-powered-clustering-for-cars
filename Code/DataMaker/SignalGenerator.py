import numpy as np
import matplotlib.pyplot as plt
from random import seed, random

def generate_rectangle_signal(duration=10, amplitude=1, frequency=1, sampling_rate=1000, offset=0):
    """
    Generate a rectangular signal.

    Parameters:
    - duration: Duration of the signal in seconds (default is 10).
    - max_amplitude: amplitude of the signal (default is 1).
    - frequency: Frequency of the signal in Hertz (default is 1).
    - sampling_rate: Sampling rate of the signal (default is 1000 samples per second).

    Returns:
    - time: Time array for the signal.
    - signal: Generated rectangular signal.
    """

    # Calculate the time array
    time = np.arange(0, duration, 1/sampling_rate)

    # Generate the rectangular signal with dynamic amplitude
    signal =offset + amplitude * np.sign(np.sin(2 * np.pi * frequency * time))

    return time, signal

def generate_sine_signal(duration, amplitude=1, frequency=1, sampling_rate=1000, offset=0):
    """
    Generate a sine signal.

    Parameters:
    - duration: Duration of the signal in seconds.
    - amplitude: Amplitude of the signal (default is 1).
    - frequency: Frequency of the signal in Hertz (default is 1).
    - sampling_rate: Sampling rate of the signal (default is 1000 samples per second).
    - offset: Offset of the signal (default is 0).

    Returns:
    - time: Time array for the signal.
    - signal: Generated sine signal.
    """
    time = np.arange(0, duration, 1/sampling_rate)
    signal = offset + amplitude * np.sin(2 * np.pi * frequency * time)
    return time, signal

def generate_triangle_signal(duration=2, amplitude=1, frequency=1, sampling_rate=1000, offset=0):
    """
    Generate a triangle signal.

    Parameters:
    - duration: Duration of the signal in seconds.
    - amplitude: Amplitude of the signal (default is 1).
    - frequency: Frequency of the signal in Hertz (default is 1).
    - sampling_rate: Sampling rate of the signal (default is 1000 samples per second).
    - offset: Offset of the signal (default is 0).

    Returns:
    - time: Time array for the signal.
    - signal: Generated triangle signal.
    """
    time = np.arange(0, duration, 1/sampling_rate)
    signal = offset + amplitude * np.abs(2 * (time * frequency - np.floor(0.5 + time * frequency)))
    return time, signal

def add_white_noise_to_signal(time, signal, noise_amplitude = .2):
    """
    Added white noise to a generated signal.

    Parameters:
    - time: Time array for the original signal.
    - signal: Values from the original signal.
    - noise_amplitude: Amplitude of the white noise (default is 0.2).
    
    Returns:
    - time: Time array for the signal.
    - signal_with_noise: Generated rectangular signal with added white noise.
    """
   
    white_noise = noise_amplitude * np.random.normal(size=len(time))
    # Add white noise to the signal
    signal_with_noise = signal + white_noise

    return time, signal_with_noise



signal_functions = {
    "Ansauglufttemperatur": generate_rectangle_signal,
    "Luftmassenmesser": generate_triangle_signal,
    "Lambdasonde":generate_sine_signal
    }

noise_beta = {
    "Weis": 0,
    "Rosa": 1,
    "Rot": 2
    }
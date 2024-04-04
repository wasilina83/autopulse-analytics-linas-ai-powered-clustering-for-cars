#!/usr/bin/env python3
import matplotlib
import numpy as np
import math
from matplotlib import pyplot as plt
import redpitaya_scpi as scpi
import sys
sys.path.insert(0, 'DataMaker')
from SignalGenerator import signal_functions, genSigPNG
 
def generate_custom_waveform_and_plot(funk, duration, amplitude, frequency, offset, phase_shift):
    IP = '192.168.178.20'
    rp_s = scpi.scpi(IP)

    wave_form = 'arbitrary'
    N = 16384                   # Number of samples
    freq = 1
    ampl = 1
    funkion =signal_functions[funk] 
    time, signal = funkion(duration, amplitude, frequency, offset, phase_shift)

    plt.plot(time, signal)
    title=f"Sigmal: {funk}"
    plt.title(title)
    matplotlib.pyplot.savefig('GUI/images/test-12.png')

    rp_s.tx_txt('GEN:RST')

    # Function for configuring a Source
    rp_s.sour_set(1, wave_form, ampl, freq, data = signal)
       
    rp_s.tx_txt('OUTPUT:STATE ON')
    rp_s.tx_txt('SOUR:TRIG:INT')

    rp_s.close()

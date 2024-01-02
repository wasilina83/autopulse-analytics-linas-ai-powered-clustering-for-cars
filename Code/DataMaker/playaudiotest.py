import numpy as np
from scipy.io.wavfile import write
import colorednoise as cn

rate = 44100
#input values
# the exponent: 0=white noite; 1=pink noise;  2=red noise (also "brownian noise")
samples = 2**16  # number of samples to generate (time series extension)

#Deffing some colores
white =0
Aw = cn.powerlaw_psd_gaussian(white, samples) # the exponent: 0=white noite; 1=pink noise;  2=red noise (also "brownian noise")
scaled = np.int16(Aw / np.max(np.abs(Aw)) * 32767)
write('white.wav', rate, scaled)

#Deffing some colores
pink =1
Ap = cn.powerlaw_psd_gaussian(pink, samples) # the exponent: 0=white noite; 1=pink noise;  2=red noise (also "brownian noise")
scaled = np.int16(Ap / np.max(np.abs(Ap)) * 32767)
write('pink.wav', rate, scaled)

#Deffing some colores
red =2
Ar = cn.powerlaw_psd_gaussian(red, samples) # the exponent: 0=white noite; 1=pink noise;  2=red noise (also "brownian noise")
scaled = np.int16(Ap / np.max(np.abs(Ar)) * 32767)
write('red.wav', rate, scaled)
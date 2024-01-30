import numpy as np
from scipy.io.wavfile import write
import colorednoise as cn
import pandas as pd

# rate = 44100
# #input values
# # the exponent: 0=white noite; 1=pink noise;  2=red noise (also "brownian noise")
# samples = 2**16  # number of samples to generate (time series extension)

# #Deffing some colores
# white =0
# Aw = cn.powerlaw_psd_gaussian(white, samples) # the exponent: 0=white noite; 1=pink noise;  2=red noise (also "brownian noise")
# scaled = np.int16(Aw / np.max(np.abs(Aw)) * 32767)
# write('white.wav', rate, scaled)

# #Deffing some colores
# pink =1
# Ap = cn.powerlaw_psd_gaussian(pink, samples) # the exponent: 0=white noite; 1=pink noise;  2=red noise (also "brownian noise")
# scaled = np.int16(Ap / np.max(np.abs(Ap)) * 32767)
# write('pink.wav', rate, scaled)

# #Deffing some colores
# red =2
# Ar = cn.powerlaw_psd_gaussian(red, samples) # the exponent: 0=white noite; 1=pink noise;  2=red noise (also "brownian noise")
# scaled = np.int16(Ar / np.max(np.abs(Ar)) * 32767)
# write('red.wav', rate, scaled)
rate = 5000
f='Daten\Trainingsdaten\Ansauglufttemperatur\Rosa\Rauschen_100\signals_data_Signal-duration_15_Signal-amplitude_19_Signal-frequency_5_Signal-offset_-10.csv'
data=pd.read_csv(f)
y_data=data['signal']
scaled = np.int16(y_data / np.max(np.abs(y_data)) * 32767*10)
write('soundcheck.wav', rate, scaled)
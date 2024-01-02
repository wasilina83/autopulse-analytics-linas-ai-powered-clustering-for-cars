import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz, firls, filtfilt

def design_filter(numtaps):
    # Normalisierte Frequenzen
    fv = np.linspace(0, 1, 20)
    # Amplituden von '1/f^2'
    a = 1. / ((1 + fv * 2)**2)
    # Koeffizienten des Filter-Numerators
    b = firls(numtaps, fv, a)
    return b

def plot_bode_plot(b):
    # Bode-Plot des Filters
    w, h = freqz(b, 1, worN=2**17)
    plt.figure()
    plt.plot(0.5 * w / np.pi, np.abs(h))
    plt.title('Filter Bode Plot')
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Amplitude')
    plt.show()

def generate_noise_and_plots(b, num_samples=1E+6):
    N = int(num_samples)
    ns = np.random.rand(N)
    
    # '1/f'-Rauschen erzeugen
    invfn = filtfilt(b, 1, ns)  

    # Zeitbereichs-Plot des Rauschens
    plt.figure()
    plt.plot(np.arange(N), invfn)
    plt.title('Rauschen im Zeitbereich')
    plt.grid()
    plt.show()

    # Fourier-Transformierte des Rauschens
    FTn = np.fft.fft(invfn - np.mean(invfn)) / N
    plt.figure()
    plt.plot(np.arange(N // 2 + 1), np.abs(FTn[:N // 2 + 1]) * 2)
    plt.title('Fourier-Transformierte des Rauschens')
    plt.grid()
    plt.show()

if __name__ == "__main__":
    # Filterentwurf
    filter_coefficients = design_filter(43)

    # Bode-Plot des Filters
    plot_bode_plot(filter_coefficients)

    # Rauschen generieren und plotten
    generate_noise_and_plots(filter_coefficients)

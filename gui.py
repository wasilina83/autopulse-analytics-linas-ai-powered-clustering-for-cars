import tkinter as tk
from tkinter import filedialog
from siglanGen import generate_rectangle_signal, generate_signal_with_noise
from CreateData import generate_labled_signal_with_noise_list, generate_labled_signals_list

class SignalGeneratorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Signal Generator")

        # Buttons
        self.button_generate_signals = tk.Button(master, text="Generate Signals", command=self.generate_signals)
        self.button_generate_signals.pack(pady=10)

        self.button_generate_noisy_signals = tk.Button(master, text="Generate Noisy Signals", command=self.generate_noisy_signals)
        self.button_generate_noisy_signals.pack(pady=10)

    def generate_signals(self):
        signals_list = generate_labled_signals_list()
        # Hier können Sie mit den generierten Signalen arbeiten

    def generate_noisy_signals(self):
        noise_signals_list = generate_labled_signal_with_noise_list()
        # Hier können Sie mit den generierten verrauschten Signalen arbeiten

def main():
    root = tk.Tk()
    app = SignalGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

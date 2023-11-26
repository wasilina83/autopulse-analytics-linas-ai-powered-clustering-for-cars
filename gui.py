import tkinter as tk
from tkinter import *
from siglanGen import generate_signal, signal_functions
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk


class SignalClassifierGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Signal Classifier")
        
        # Parameter
        self.duration_var = tk.IntVar() 
        self.amplitude_var = tk.IntVar()
        self.frequency_var = tk.IntVar()
        self.sampling_rate_var = tk.IntVar()
        self.offset_var = tk.DoubleVar()
        self.signal_type_var = tk.StringVar()
    

        # Eigabefelder
        self.label_duration = Label(master, text="Dauer")
        self.label_duration.grid(row=1, column=0)
        self.entry_duration = Entry(master, textvariable=self.duration_var)
        self.entry_duration.grid(row=1, column=1)

        self.label_amplitude = Label(master, text="Amplitude")
        self.label_amplitude.grid(row=2, column=0)
        self.entry_amplitude = Entry(master, textvariable=self.amplitude_var)
        self.entry_amplitude.grid(row=2, column=1)
        
        self.label_frequency = Label(master, text="Frequenz")
        self.label_frequency.grid(row=3, column=0)
        self.entry_frequency = Entry(master, textvariable=self.frequency_var)
        self.entry_frequency.grid(row=3, column=1)
        
        self.label_sampling_rate = Label(master, text="Abtastrate")
        self.label_sampling_rate.grid(row=4, column=0)
        self.entry_sampling_rate = Entry(master, textvariable=self.sampling_rate_var)
        self.entry_sampling_rate.grid(row=4, column=1)

        self.label_offset = Label(master, text="Offset")
        self.label_offset.grid(row=5, column=0)
        self.entry_offset = Entry(master, textvariable=self.offset_var)
        self.entry_offset.grid(row=5, column=1)

        # Dropdown
        self.label_signal_type = Label(master, text="Signaltyp")
        self.label_signal_type.grid(row=6, column=0)
        self.combo_signal_type = ttk.Combobox(master, textvariable=self.signal_type_var, values=list(signal_functions.keys()))
        self.combo_signal_type.grid(row=6, column=1)
        self.combo_signal_type.set("^.^")

        # Button
        self.button_generate_signals = ttk.Button(master, text="Generate Signals", command=self.generate_signals, bootstyle=(SUCCESS, OUTLINE) )
        self.button_generate_signals.grid(row=7, column=1, columnspan=2, pady=10)
        
        # Leinwand für das Diagramm
        self.frame = ttk.Frame(master)
        self.frame.grid(row=8, column=0, columnspan=2)
        self.canvas = FigureCanvasTkAgg(Figure(), master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=8, column=3)
        #self.canvas.get_tk_widget().update_idletasks()
        #width, height = self.canvas.get_tk_widget().winfo_width(), self.canvas.get_tk_widget().winfo_height()
        #self.canvas.get_tk_widget().place(in_=background_label, anchor="center", relx=.5, rely=.5, width=width, height=height)

    def generate_signals(self):
        duration = self.duration_var.get() 
        amplitude = self.amplitude_var.get()
        sampling_rate = self.sampling_rate_var.get()
        offset = self.offset_var.get()
        signal_type = self.signal_type_var.get()
        frequency = self.frequency_var.get()
        signal_function =signal_functions.get(signal_type)
        time, signal = signal_function(duration, amplitude, frequency, sampling_rate, offset)

        self.canvas.get_tk_widget().destroy
        self.canvas = FigureCanvasTkAgg(generate_signal(time, signal), master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)
     
    
def main():
    root = ttk.Window(themename="aw4null")
    root.geometry("800x500")
    # Hintergrundbild einbinden
    background_image = PhotoImage(file="images/bild-hintergrund-zitat.png")
    background = Label(root, image=background_image)
    background.place(x=0, y=0, relwidth=1, relheight=1)
    app = SignalClassifierGUI(root)
    
    
    root.mainloop()

if __name__ == "__main__":
    main()

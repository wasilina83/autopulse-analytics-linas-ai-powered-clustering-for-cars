import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import tkinter.ttk as ttk
from siglanGen import generate_signal, signal_functions
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tensorflow.keras.models import load_model
import os
from callModel import predict_label

class FunctionalityManager:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
    
    def start_button_click(self):
        self.ui_manager.generate_signals_and_predict()        
        
class SignalClassifierGUI:
    def __init__(self, master, ui_manager):
        self.ui_manager = ui_manager
        self.master = master

        # Parameter
        self.duration_var = tk.IntVar()
        self.amplitude_var = tk.IntVar()
        self.frequency_var = tk.IntVar()
        self.sampling_rate_var = tk.IntVar()
        self.offset_var = tk.DoubleVar()
        

        # Kleines Canvas im Haupt-Canvas
        self.setup_sidebar_canvas()

    def setup_sidebar_canvas(self):
        self.sidebar_canvas = tk.Canvas(self.master, width=193, height=325, highlightbackground='#0046F0', bg='#0046F0')
        self.sidebar_canvas.place(x=199, y=105)

        # horizontale Scrollbars für Parameter
        self.setup_parameter_slider("Dauer", 5, 25, 10, 23, self.duration_var)
        self.setup_parameter_slider("Amplitude", 1, 10, 10, 100, self.amplitude_var)
        self.setup_parameter_slider("Frequenz", 1, 8, 10, 178, self.frequency_var)
        self.setup_parameter_slider("Offset", -10.5, 10.5, 10, 256, self.offset_var)

    def setup_parameter_slider(self, label, from_val, to_val, x_pos, y_pos, variable):
        # Label
        label_widget = Label(self.sidebar_canvas, text=label, font=("MicrosoftJhengHei", 16), fg='white', bg='#0046F0')
        label_widget.place(x=x_pos, y=y_pos)

        # Slider
        scale = Scale(self.sidebar_canvas, from_=from_val, to=to_val, orient="horizontal", bg='#0046F0',
                      highlightbackground='#0046F0', troughcolor='white', font=("MicrosoftJhengHei", 16), fg='white',
                      variable=variable)
        scale.place(x=x_pos, y=y_pos + 30, width=160)

class UIManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Signal Classifier")
        self.master.geometry("999x1080")
        self.master.attributes("-fullscreen", True)
        self.functionality = FunctionalityManager(self)

        self.signal_type_var = tk.StringVar()
        self.setup_ui()
        self.is_generated = False
        

    def setup_ui(self):
        self.BG_canvas = Canvas(self.master, width=999, height=1080)
        self.BG_canvas.pack(fill=BOTH, expand=True)
        self.bg = PhotoImage(file="images/BG.png")
        self.imgbox = self.BG_canvas.create_image(0, 0, image=self.bg, anchor='nw')

        self.BG_canvas.create_text(190, 70, text="Signalparameter:", font=("MicrosoftJhengHei", 30), fill="#0046F0")
        self.BG_canvas.create_text(170, 710, text="     Signal \n generieren", font=("MicrosoftJhengHei", 28), fill="white")
        start_button_label_img = PhotoImage(file='images/spiel.png')
        resized_image = start_button_label_img.subsample(3, 3)
        self.start_button_image = resized_image
        start_button_label = Label(image=resized_image)
        self.button_generate_signals = Button(self.BG_canvas, image=resized_image, command=self.generate_signals_and_predict, borderwidth=0, background='white', activebackground='white')
        self.button_generate_signals.place(x=115, y=800)

        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", lambda event: self.master.attributes("-fullscreen", False))

        self.signal_classifier_gui = SignalClassifierGUI(self.master, self)

        # Label and Combobox for Signal Type
        self.BG_canvas.create_text(72, 553, text="Signaltyp: ", font=("MicrosoftJhengHei", 15), fill="#0046F0")
        style = ttk.Style()
        style.configure("TCombobox", fieldbackground="#0046F0", foreground="#0046F0", inputbg="#0046F0",
                        inputfg='#0046F0', background='#0046F0', border="#0046F0", bordercolor="#0046F0",
                        highlightbackground='#0046F0', troughcolor='white')

        combo_signal_type = ttk.Combobox(self.BG_canvas, style="TCombobox", textvariable=self.signal_type_var,
                                         values=list(signal_functions.keys()), width=8, font=("MicrosoftJhengHei", 16),
                                         background='#0046F0', foreground='#0046F0')
        combo_signal_type.place(x=145, y=545)

        # Leinwand für das Diagramm
        self.frame = ttk.Frame(self.master)
        self.canvas = FigureCanvasTkAgg(Figure(), master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1, anchor='se')

        # # Leinwand für das Diagramm
        # self.frame = ttk.Frame(self.master)
        # self.frame.place(relx=0.7, rely=0.7, relwidth=0.5, relheight=0.5, x=345, y=245, anchor='se')
        # self.canvas = FigureCanvasTkAgg(Figure(), master=self.frame)
        # self.canvas.draw()
        # self.canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1, anchor='se')
        
    def generate_signals_and_predict(self):
        # Werte der Schieberegler und Eingabefelder, wenn der Button gedrückt wird
        duration = self.signal_classifier_gui.duration_var.get()
        amplitude = self.signal_classifier_gui.amplitude_var.get()
        frequency = self.signal_classifier_gui.frequency_var.get()
        sampling_rate = 1000
        offset = self.signal_classifier_gui.offset_var.get()
        signal_type = self.signal_type_var.get()
        print(signal_type, duration, amplitude, frequency, sampling_rate, offset)
        signal_function = signal_functions.get(signal_type)
        if signal_function is None:
            print(f"Error: Signalfunktion für '{signal_type}' nicht gefunden.")
            return

        time, signal = signal_function(duration, amplitude, frequency, sampling_rate, offset)

        # Erstelle und platziere die Leinwand nach Bedarf
        if not hasattr(self, 'canvas_placed'):
            self.canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1, anchor='se')
            self.canvas_placed = True
        time, signal = signal_function(duration, amplitude, frequency, sampling_rate, offset)

        self.canvas.get_tk_widget().destroy
        self.canvas = FigureCanvasTkAgg(generate_signal(time, signal), master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=3, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)
        model_path = os.path.join('models', 'Signalclassifier.h5')
        # Modell laden
        loaded_model = load_model(model_path)
        csv_file_path = r'C:\Users\Engelmann\OneDrive\Dokumente\arbeit\autopulse-analytics-linas-ai-powered-clustering-for-cars\csv_file.csv'

        answer = predict_label(csv_file_path)
        print(answer)
        # Assuming you have a prediction_label defined in your GUI
        self.prediction_label.config(text=answer)

    def toggle_fullscreen(self, event):
        self.master.attributes("-fullscreen", not self.master.attributes("-fullscreen", False))

    def update_image(self, image_path):
        try:
            pil_image = Image.open(image_path)
            w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
            pil_image = pil_image.resize((w, h), Image.BICUBIC)
            self.photo_image = ImageTk.PhotoImage(pil_image)
            self.BG_canvas.itemconfig(self.imgbox, image=self.photo_image)
        except Exception as e:
            print(f"Error updating image: {e}")

def main():
    root = tk.Tk()
    ui_manager = UIManager(root)
    functionality = FunctionalityManager(ui_manager)
    ui_manager.update_image("images/BG.png")
    root.mainloop()

if __name__ == "__main__":
    main()

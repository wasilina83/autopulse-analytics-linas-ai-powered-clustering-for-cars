import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from siglanGen import generate_rectangle_signal, signal_functions
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tensorflow.keras.models import load_model
import os
import callModel
from callModel import predict_label


class FunctionalityManager:
    def __init__(self, ui_manger):
        self.ui_manager = ui_manger
        

    def on_button_click(self):
        print('Button clicked!')
        self.ui_manager.generate_signals_and_predict()
        
class SignalClassifierGUI:
    def __init__(self, master, ui_manager):
        self.ui_manager = ui_manager

class UIManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Signal Classifier")
        self.master.geometry("999x1080")
        self.master.attributes("-fullscreen", True)
        self.functionality = FunctionalityManager(self)

        self.setup_ui()

    def setup_ui(self):
        self.BG_canvas = Canvas(self.master, width=999, height=1080)
        self.BG_canvas.pack(fill=BOTH, expand=True)
        self.bg =PhotoImage(file="images\BG.png")
        self.imgbox = self.BG_canvas.create_image(0, 0, image=self.bg, anchor='nw')

        self.BG_canvas.create_text(190, 90, text="Signalparameter:", font=("MicrosoftJhengHei", 30), fill="#0046F0")
        button1 = Button(self.master, text="Start", command=self.functionality.on_button_click)
        button1_window = self.BG_canvas.create_window(10, 10, anchor="nw", window=button1)

        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", lambda event: self.master.attributes("-fullscreen", False))
        
        self.signal_classifier_gui = SignalClassifierGUI(self.master, self)
        
    def generate_signals_and_predict(self):
        self.signal_classifier_gui.generate_signals()
        model_path = os.path.join('models', 'Signalclassifier.h5')
        loaded_model = load_model(model_path)
        csv_file_path = r'C:\Users\Engelmann\OneDrive\Dokumente\arbeit\autopulse-analytics-linas-ai-powered-clustering-for-cars\csv_file.csv'
        answer = predict_label(csv_file_path)
        print(answer)
        self.signal_classifier_gui.prediction_label.config(text=answer)  

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
    functionality = FunctionalityManager()
    root = Tk()

    ui_manager = UIManager(root, functionality)
    ui_manager.update_image(r"C:\Users\Engelmann\OneDrive\Dokumente\arbeit\autopulse-analytics-linas-ai-powered-clustering-for-cars\images\BG.png")
    root.mainloop()

if __name__ == "__main__":
    main()
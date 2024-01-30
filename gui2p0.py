import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import tkinter.ttk as ttk
from siglanGen import signal_functions, generate_signal
from matplotlib. 


class FunctionalityManager:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager

    def on_button_click(self):
        print('Button clicked!')
        
        self.ui_manager.generate_signals_and_predict()

class SignalClassifierGUI:
    def __init__(self, master, ui_manager):
        self.ui_manager = ui_manager
        self.master = master

        # Parameter
        self.duration_var = tk.IntVar(value=5)
        self.amplitude_var = tk.IntVar()
        self.frequency_var = tk.IntVar()
        self.sampling_rate_var = tk.IntVar()
        self.offset_var = tk.DoubleVar()
        self.signal_type_var = tk.StringVar()

        # Kleines Canvas im Haupt-Canvas
        self.sidebar_canvas = tk.Canvas(self.master, width=193, height=325, highlightbackground='#0046F0', bg='#0046F0')
        self.sidebar_canvas.place(x=199, y=105)
        
        # Parameter
        self.duration_var = tk.IntVar()
        self.amplitude_var = tk.IntVar()
        self.frequency_var = tk.IntVar()
        self.sampling_rate_var = tk.IntVar()
        self.offset_var = tk.DoubleVar()

        # horizontale Scrollbars für Parameter 
        duration_slider = Scale(self.sidebar_canvas, from_=5, to=25, orient="horizontal", bg='#0046F0', highlightbackground='#0046F0', troughcolor='white', command=self.on_parameter_scroll, font=("MicrosoftJhengHei", 16), fg='white')
        duration_slider.place(x=10, y=32, width=160)
        amplitude_slider = Scale(self.sidebar_canvas, from_=1, to=10, orient="horizontal", bg='#0046F0', highlightbackground='#0046F0', troughcolor='white', variable=self.amplitude_var, command=self.on_parameter_scroll, font=("MicrosoftJhengHei", 16), fg='white')
        amplitude_slider.place(x=10, y=100, width=160)
        frequency_slider = Scale(self.sidebar_canvas, from_=1, to=8, orient="horizontal", bg='#0046F0', highlightbackground='#0046F0', troughcolor='white', variable=self.frequency_var, command=self.on_parameter_scroll, font=("MicrosoftJhengHei", 16), fg='white')
        frequency_slider.place(x=10, y=178, width=160)
        offset_slider = Scale(self.sidebar_canvas, from_=-10.5, to=10.5, orient="horizontal", bg='#0046F0', highlightbackground='#0046F0', troughcolor='white', variable=self.offset_var, command=self.on_parameter_scroll, font=("MicrosoftJhengHei", 16), fg='white')
        offset_slider.place(x=10, y=256, width=160)

    def on_parameter_scroll(self, *args):
        # Hier kannst du die Aktionen für jeden Parameter anpassen, falls nötig
        pass

class UIManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Signal Classifier")
        self.master.geometry("999x1080")
        self.master.attributes("-fullscreen", True)
        self.functionality = FunctionalityManager(self)
        
        self.signal_type_var = tk.StringVar()

        self.setup_ui()

    def setup_ui(self):
        self.BG_canvas = Canvas(self.master, width=999, height=1080)
        self.BG_canvas.pack(fill=BOTH, expand=True)
        self.bg = PhotoImage(file="images\BG.png")
        self.imgbox = self.BG_canvas.create_image(0, 0, image=self.bg, anchor='nw')

        self.BG_canvas.create_text(190, 70, text="Signalparameter:", font=("MicrosoftJhengHei", 30), fill="#0046F0")
        start_button_label_img = PhotoImage(file=r'C:\Users\Engelmann\OneDrive\Dokumente\arbeit\autopulse-analytics-linas-ai-powered-clustering-for-cars\images\Bplay.png')
        resized_image = start_button_label_img.subsample(2, 2)  # Hier kannst du die Verkleinerungsfaktoren anpassen
        start_button_label = Label(image=resized_image)
        button1 = Button(self.BG_canvas, start_button_label, command=self.functionality.on_button_click)
        button1.place(x=145, y=745)

        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", lambda event: self.master.attributes("-fullscreen", False))

        self.signal_classifier_gui = SignalClassifierGUI(self.master, self)

        # Label and Combobox for Signal Type
       
        self.BG_canvas.create_text(72, 553, text="Signaltyp: ", font=("MicrosoftJhengHei", 15), fill="#0046F0")
        style = ttk.Style()
        self.master.title("Signal Classifier")
        style.configure("TCombobox", fieldbackground="#0046F0", foreground="#0046F0", inputbg="#0046F0", inputfg='#0046F0', background='#0046F0', border="#0046F0", bordercolor="#0046F0",  highlightbackground='#0046F0', troughcolor='white' )

        combo_signal_type = ttk.Combobox(self.BG_canvas, style="TCombobox", textvariable=self.signal_type_var, values=list(signal_functions.keys()), width=8, font=("MicrosoftJhengHei", 16), background='#0046F0', foreground='#0046F0')
        combo_signal_type.place(x=145, y=545)  # Here you can adjust the side alignment


    def generate_signals_and_predict(self):
        # Here you can add the method to generate signals and make predictions
        pass

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
    ui_manager.update_image(r"C:\Users\Engelmann\OneDrive\Dokumente\arbeit\autopulse-analytics-linas-ai-powered-clustering-for-cars\images\BG.png")
    root.mainloop()

if __name__ == "__main__":
    main()
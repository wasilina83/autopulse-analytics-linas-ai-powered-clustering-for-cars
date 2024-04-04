# 1. Imports
import os
import math
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.graphics import RoundedRectangle, Color
from SignalGenerator import signal_functions, pron, genSigPNG


# 2.  Kivy Builder String hier
# Laden der KV-Datei mit den Widgets
Builder.load_file('widgets.kv')

# 3.
def calculate_size_properties(min_size=True, pos_x=True, pos_y=True):
    window_width, window_height = Window.size
    if min_size:
        min_size = int(min(window_width, window_height) * .1)
    else:
        min_size = None
    
    if pos_x:
        pos_x = window_width * .1
    else:
        pos_x = None
    
    if pos_y:
        pos_y = window_height * .1
    else:
        pos_y = None

    return min_size, pos_x, pos_y

# 3. Custom Widgets und Layouts
class SignalclassifierLayout(RelativeLayout):
    def refreshWindow(self, signal_type, duration, amplitude, frequency, offset, phase_shift):
        # Laden des Layouts für das Bild nur bei Bedarf
        Builder.load_string('''
            <ImageUpdater>:
                Image:
                    id: gif
                    source: 'KIVYG/images/animation.gif'
                    size_hint: None, None
                    size: 640, 480
                    allow_stretch: True
                    anim_delay: -1
                    anim_loop: 1
                    center: self.parent.center
                    pos_hint: {'center_x': 0.69, 'top': 0.9}
            ''')
        # Jetzt können wir auf das ImageUpdater-Layout zugreifen
        image_updater = ImageUpdater()
        # Generieren des neuen GIF
        genSigPNG(signal_type, duration, amplitude, frequency, offset, phase_shift)
        # Aktualisieren der Bildquelle im Kivy-Layout
        image_updater.ids.gif.source = 'KIVYG/images/animation.gif'
        # Neuzeichnen des Bildes
        image_updater.ids.gif.reload()
        # Hinzufügen des ImageUpdater-Layouts zum SignalclassifierLayout
        self.add_widget(image_updater)

# Layout nur für die Aktualisierung des Bildes
class ImageUpdater(RelativeLayout):
    pass

class CustomLabelBox(RoundedRectangle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0, 0.2745, 0.9412, 1)
        self.bind(pos=self.on_size, size=self.on_size)

    def on_size(self, *args):
        # Update RoundedRectangle properties when size changes
        self.radius = self.calculate_radius()

    def calculate_radius(self):
        # Calculate the radius based on the size of the rectangle
        smallest_dimension = min(self.size)
        radius = smallest_dimension / 6  # Approximately 1/6 of the smallest dimension
        return [(radius, radius), (radius, radius), (radius, radius), (radius, radius)]


class CustomSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_graphics_instructions, size=self.update_graphics_instructions)

    def update_graphics_instructions(self, *args):
        self.canvas.before.clear()  
        with self.canvas.before:
            Color(0, 0.2745, 0.9412, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.calculate_radius())

    def calculate_radius(self):
        smallest_dimension = min(self.size)
        radius = smallest_dimension / 6  
        return [(radius, radius), (radius, radius), (radius, radius), (radius, radius)]            
            
            
# 4. Signal Generation and Animation Logic
class SignalGenerator:
    @staticmethod
    def generate_signal(self):
        amplitude = self.amplitude_slider.value
        frequency = self.frequency_slider.value
        offset = self.offset_slider.value
        phase_shift = self.phase_shift_slider.value
        signal_type = self.signal_type_spinner.text
        duration = 3
        genSigPNG(signal_type, duration, amplitude, frequency, offset, phase_shift)

# 5. Main App Class
def set_widgets_opacity_by_suffix(widget_dict, opacity_value):
            for key, widget in widget_dict.items():
                        widget.opacity = opacity_value

class SignalclassifierApp(App):
    def calculate_size(self, min_size=True, pos_x=True, pos_y=True):
        window_width, window_height = Window.size
        if min_size:
            min_size = int(min(window_width, window_height) * .1)
        else:
            min_size = None
        
        if pos_x:
            pos_x = window_width * .1
        else:
            pos_x = None
        
        if pos_y:
            pos_y = window_height * .1
        else:
            pos_y = None

        return min_size, pos_x, pos_y
    
    def build(self):
        #fullscreen mode
        Window.fullscreen = 'auto'
        self.layout = RelativeLayout()
        self.background = Image(source='KIVYG/images/BG.png', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background)
        window_width, window_height = Window.size
        # Load the image for the logo (with transparent background)
        logo_size = int(window_width*1.63)  # 20% of the smaller dimension
        prolab_size = int(window_width*0.7)
        self.logo_pic = Image(source='KIVYG/images/logo.png', size_hint=(None, None), size=(logo_size, logo_size), pos_hint={'center_x': 0.49, 'top': 1.4})
        self.layout.add_widget(self.logo_pic)
        self.prolab_con = Image(source='KIVYG/images/prolab.png', size_hint=(None, None), size=(prolab_size, prolab_size), allow_stretch=True, keep_ratio=True, pos_hint={'center_x': 0.8, 'top': .45})
        self.layout.add_widget(self.prolab_con)
        # Add other widgets or elements if needed
        self.text_label3 = Label(text='Generator starten', font_size=int(window_height*.08), pos_hint={'center_x':.3, 'top': 1})
        self.layout.add_widget(self.text_label3)
        # Load the image for the Play button
        play_button_size = int(min(window_width, window_height)*.4)  # 10% of the smaller dimension
        self.play_button = Button(background_normal='KIVYG/images/play.png', size_hint=(None, None), size=(play_button_size, play_button_size), pos_hint={'center_x': 0.3, 'top':  .4}, border=(0, 0, 0, 0))
        self.play_button.bind(on_press=self.on_play_button_click)
        self.layout.add_widget(self.play_button)
        
        return self.layout
    
    def update_label_text(self, slider_instance, slider_value, label_instance, label_text):
        # Hier wird der Text des zugehörigen Labels aktualisiert
        label_instance.text = f'{label_text}: {slider_value}'
        return label_instance.text

    def on_slider_value_change(self, instance, value, label_text):
        # Hier können Sie den geänderten Wert des Sliders verwenden und entsprechende Aktionen ausführen
        # Rufen Sie die update_label_text-Funktion auf, um den Text des zugehörigen Labels zu aktualisieren
        label_instance = self.slider_label_mapping[instance]
        self.update_label_text(instance, value, label_instance, label_text)
        
    #return self.layout
    def on_play_button_click(self, instance):
        # Remove the Play button and Label3
        self.layout.remove_widget(self.play_button)
        self.layout.remove_widget(self.text_label3)
        self.layout.remove_widget(self.logo_pic)
        
        window_width, window_height = Window.size
        logo_size = int(window_width*.39)
        self.new_background = Image(source='KIVYG/images/BGWeis.png', allow_stretch=True, keep_ratio=False, x=-Window.width, size_hint_x=0.5)
        self.layout.add_widget(self.new_background)
        self.logo_stat = Image(source='KIVYG/images/logo.png', size_hint=(None, None), size=(logo_size, logo_size), pos_hint={'center_x': .78, 'top': 1.199})
        self.layout.add_widget(self.logo_stat)
        
#         widget_dict = {
#     'start_sig_box': self.start_sig_box,
#     'start_sig': self.start_sig,
#     'play_button2': self.play_button2,
#     'signal_type_spinner': self.signal_type_spinner,
#     'phase_shift_label': self.phase_shift_label,
#     'setup_param_label': self.setup_param_label,
#     'amplitude_label': self.amplitude_label,
#     'frequency_label': self.frequency_label,
#     'offset_label': self.offset_label,
#     'amplitude_label_box': self.amplitude_label_box,
#     'frequency_label_box': self.frequency_label_box,
#     'offset_label_box': self.offset_label_box,
#     'phase_shift_label_box': self.phase_shift_label_box,
#     'setup_param_box': self.setup_param_box,
#     'amplitude_slider': self.amplitude_slider,
#     'frequency_slider': self.frequency_slider,
#     'offset_slider': self.offset_slider,
#     'phase_shift_slider': self.phase_shift_slider
# }
#         # Animation for wigets
#         new_animation = Animation(x=0, duration=1)
#         new_animation.start(self.new_background)
#         Clock.schedule_once(self.delayed_appearance, 1.5)
        
#           # Liste der Suffixe, nach denen gesucht werden soll
#         set_widgets_opacity_by_suffix(widget_dict, 0)
    
    def delayed_appearance(self, widget_dict):
        # Start the animation to change the opacity from 0 to 1
        for widget_id, widget in widget_dict.items():
            Animation(opacity=1, duration=1).start(widget)

    
        
    
        

    def on_play_button_click2(self, instance):
        # Handle play button click event for second scenario
        pass

    def on_replay_button_click(self, instance):
        # Handle replay button click event
        pass

# Main entry point
if __name__ == '__main__':
    SignalclassifierApp().run()
import kivy
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
from SignalGenerator import signal_functions, pron, genSigPNG
import math
from kivy.graphics import RoundedRectangle, Color, Rectangle
from kivy.uix.video import Video
from kivy.lang import Builder
import os
from functools import partial
import time
from makeSig import generate_custom_waveform_and_plot
from kivy.core.text import FontContextManager as FCM
from functools import partial
import kivy.utils as utils
import random
# Create a font context containing system fonts + one custom TTF



class SignalclassifierLayout(RelativeLayout):
    def refreshWindow(self, signal_type, duration, amplitude, frequency, offset, phase_shift):
        # Pfad zum alten GIF
        old_gif_path = 'KIVYG/images/animation.gif'
        
        # Löschen des alten GIF
        if os.path.exists(old_gif_path):
            os.remove(old_gif_path)
        
        # Generieren des neuen GIF
        genSigPNG(signal_type, duration, amplitude, frequency, offset, phase_shift)
        
        # Aktualisieren der Bildquelle im Kivy-Layout
        self.ids.gif.source = old_gif_path

        # Neuzeichnen des Bildes
        self.ids.gif.reload()
        
class CustomLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Initialize the rectangle with graphics instructions
        with self.canvas:
            Color(0, 0.2745, 0.9412, 1)  # Set the color to blue
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[(5, 5), (5, 5), (5,5), (5,5)])

        # Update the rectangle when the size or position changes
        self.bind(pos=self.on_size, size=self.on_size)

    def on_size(self, *args):
        # Check if the rectangle already exists
        if hasattr(self, 'rect'):
            # Update the size and position of the rectangle
            self.rect.size = self.size
            self.rect.pos = self.pos


class CustomSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Schedule the creation of graphics instructions on the main thread
        Clock.schedule_once(self.create_graphics_instructions)

    def create_graphics_instructions(self, dt):
        # Initialize the rectangle with graphics instructions
        with self.canvas.before:
            Color(0, 0.2745, 0.9412, 1)  # Set the color to blue
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[(5, 5), (5, 5), (5, 5), (5, 5)])

        # Update the rectangle when the size or position changes
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        # Check if the rectangle already exists
        if hasattr(self, 'rect'):
            # Update the size and position of the rectangle
            self.rect.size = self.size
            self.rect.pos = self.pos
                    
            
class SignalclassifierApp(App):
    
    def build(self):
        self.signal_win = None
        # Set the window to fullscreen mode
        Window.fullscreen = 'auto'
        self.orientation = 'vertical'
        # Create a RelativeLayout as the main layout
        self.layout = RelativeLayout()

        # Load the background image
        self.background = Image(source='KIVYG/images/BG.png', allow_stretch=True, keep_ratio=False)

        # Add the image to the layout
        self.layout.add_widget(self.background)

        # Add a text label before the image
        win_w, win_h = Window.size

        # Load the image for the logo (with transparent background)
        self.logo = Image(source='KIVYG/images/lolgo.png', size_hint=(None, None), size=(win_h*1.65, win_h*1.65), pos_hint={'center_x': .49, 'top': 1.6})
        self.layout.add_widget(self.logo)
        self.prolab = Image(source='KIVYG/images/prolab.png', size_hint=(None, None), size=(win_h*.65, win_h*.65), allow_stretch=True, keep_ratio=True, pos_hint={'center_x': 0.8, 'top': .46})
        self.layout.add_widget(self.prolab)

        # Add other widgets or elements if needed
        self.text_label3 = Label(text=f'Starten', font_size=win_h*.06, pos_hint={'center_x': .29, 'top': .7}, font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.layout.add_widget(self.text_label3)

        # Load the image for the Play button
        self.play_button = Button(background_normal='KIVYG/images/play1.png', size_hint=(None, None), size=(win_h*.28, win_h*.28), pos_hint={'center_x': .3, 'top': .6}, border=(0, 0, 0, 0))
        self.play_button.bind(on_press=self.on_play_button_click)
        self.layout.add_widget(self.play_button)
        self.esxit_button = Button(background_normal='KIVYG/images/schaltflache-abbrechen.png', size_hint=(None, None), size=(win_h*.05, win_h*.05), pos_hint={'center_x': .98, 'top': .991}, border=(0, 0, 0, 0) )
        self.esxit_button.bind(on_press = self.on_exit_click)
        self.layout.add_widget(self.esxit_button)

        return self.layout
    
    def on_exit_click(self, instance):
        App.get_running_app().stop()
        quit()
         
    def on_play_button_click(self, instance):
        
        # Remove the Play button and Label3
        self.layout.remove_widget(self.play_button)
        self.layout.remove_widget(self.text_label3)
        self.layout.remove_widget(self.logo)

        # Load the new background image
        window_width, window_height = Window.size
        
        self.new_background = Image(source='KIVYG/images/BGWeis.png', allow_stretch=True, keep_ratio=False, x=-Window.width, size_hint_x=0.5)
        self.layout.add_widget(self.new_background)
        self.logo = Image(source='KIVYG/images/lolgo.png', size_hint=(None, None), size=(int(window_width*.4), int(window_width*.4)), pos_hint={'center_x': .78, 'top': 1.2})
        self.layout.add_widget(self.logo)
        
        
        # Add Sliders for the parameters
        self.amplitude_slider = CustomSlider(min=3, max=5, step=.25,  orientation='horizontal', size_hint=(None, None), size=(int(window_width*.33), int(window_height*.065)), pos_hint={'center_x': 0.2, 'top': 0.835})
        
        self.frequency_slider = CustomSlider(min=159, max=165, step=1, orientation='horizontal', size_hint=(None, None), size=(int(window_width*.33), int(window_height*.065)), pos_hint={'center_x': 0.2, 'top': 0.705})
        self.amplitude_label = Label(text=f'Amplitude: {self.amplitude_slider.value}', size_hint=(None, None), size=(int(window_width*.25), int(window_height*.045)), pos_hint={'center_x': 0.2, 'top': 0.89}, color=(1, 1, 1, 1), font_size='14sp',font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.frequency_label = Label(text=f'Frequenz: {self.frequency_slider.value}', size_hint=(None, None), size=(int(window_width*.25), int(window_height*.045)), pos_hint={'center_x': 0.2, 'top': 0.76}, color=(1, 1, 1, 1), font_size='14sp',font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        
        def OnamplitudeValueChange(instance, value):
            
            self.amplitude_label.text = f"Amplitude: {value}"

    # Define the OnfrequencyValueChange function outside of the on_play_button_click method
        def OnfrequencyValueChange(instance,  value):
            
            self.frequency_label.text = f"Frequenz: {value}"
        self.frequency_slider.bind(value=OnfrequencyValueChange)
        self.amplitude_slider.bind(value=OnamplitudeValueChange)
        self.layout.add_widget(self.amplitude_slider)
        self.layout.add_widget(self.frequency_slider)
       
        # Add Labels for the Slider values
        self.amplitude_label_box = CustomLabel(size_hint=(None, None), size=(int(window_width*.33), int(window_height*.045)), pos_hint={'center_x': 0.2, 'top': 0.89}, color=(1, 1, 1, 1))
        self.frequency_label_box = CustomLabel(size_hint=(None, None), size=(int(window_width*.33), int(window_height*.045)), pos_hint={'center_x': 0.2, 'top': 0.76}, color=(1, 1, 1, 1))
        self.layout.add_widget(self.amplitude_label_box)
        self.layout.add_widget(self.frequency_label_box)
        self.setup_param_box = CustomLabel(text=f'Sätze deine Parameter', size_hint=(None, None), size=(int(window_width*.35), int(window_height*.06)), pos_hint={'center_x': 0.2, 'top': .96}, color=(1, 1, 1, 1))
        self.setup_param_label = Label(text=f'Parameter setzen', size_hint=(None, None), size=(int(window_width*.25), int(window_height*.05)), pos_hint={'center_x': 0.2, 'top': 0.96}, color=(1, 1, 1, 1), font_size='16sp', font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.layout.add_widget(self.setup_param_box)
        self.layout.add_widget(self.setup_param_label)
        self.start_sig_box = CustomLabel(text=f'Gererieren', size_hint=(None, None), size=(int(window_width*.13), int(window_height*.1)), pos_hint={'center_x': 0.28, 'top': 0.408}, color=(1, 1, 1, 1))
        self.start_sig = Label(text=f'Generieren', size_hint=(None, None), size=(int(window_width*.13), int(window_height*.1)), pos_hint={'center_x': 0.28, 'top': 0.408}, color=(1, 1, 1, 1), font_size='13sp',  font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.play_button2 = Button(background_normal='KIVYG/images/play.png', size_hint=(None, None), size=(window_height*.12, window_height*.12), pos_hint={'center_x': 0.34, 'top': 0.488}, border=(0, 0, 0, 0))
        self.play_button2.bind(on_press=self.on_play_button_click2)
        self.layout.add_widget(self.start_sig_box)
        self.layout.add_widget(self.start_sig)
        self.layout.add_widget(self.play_button2)
               
        self.layout.add_widget(self.amplitude_label)
        self.layout.add_widget(self.frequency_label)

        self.setup_sig_label = Label(text=f'Komponente wählen', size_hint=(None, None), size=(int(window_width*.25), int(window_height*.05)), pos_hint={'center_x': 0.2, 'top': 0.63}, color=(1, 1, 1, 1), font_size='13sp', font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.setup_sig_box = CustomLabel(text=f'sig', size_hint=(None, None), size=(int(window_width*.25), int(window_height*.05)), pos_hint={'center_x': 0.2, 'top': .635}, color=(1, 1, 1, 1))
        self.layout.add_widget(self.setup_sig_box)
        self.layout.add_widget(self.setup_sig_label)
        #Zufals Signal
        self.rem_sig_label = Label(text=f'Zufallssignal', size_hint=(None, None), size=(int(window_width*.13), int(window_height*.1)), pos_hint={'center_x': 0.098, 'top': 0.408}, color=(1, 1, 1, 1), font_size='13sp', font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.rem_sig_box = CustomLabel(text=f'zu sig', size_hint=(None, None), size=(int(window_width*.13), int(window_height*.1)), pos_hint={'center_x': 0.098, 'top': 0.408}, color=(1, 1, 1, 1))
        self.layout.add_widget(self.rem_sig_box)
        self.layout.add_widget(self.rem_sig_label)
        self.rem_button = Button(background_normal='KIVYG/images/rem.png', size_hint=(None, None), size=(window_height*.12, window_height*.12), pos_hint={'center_x': 0.16, 'top': 0.49}, border=(0, 0, 0, 0))
        self.rem_button.bind(on_press=self.on_rem_button_click)
        self.layout.add_widget(self.rem_button)
        #Richtiges Signal
        self.rig_sig_label = Label(text=f'Referenzsignal', size_hint=(None, None), size=(int(window_width*.13), int(window_height*.1)), pos_hint={'center_x': 0.098, 'top': 0.2}, color=(1, 1, 1, 1), font_size='13sp', font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.rig_sig_box = CustomLabel(text=f'sig', size_hint=(None, None), size=(int(window_width*.13), int(window_height*.1)), pos_hint={'center_x': 0.098, 'top': .2}, color=(1, 1, 1, 1))
        self.layout.add_widget(self.rig_sig_box)
        self.layout.add_widget(self.rig_sig_label)
        self.ok_button = Button(background_normal='KIVYG/images/uberprufen.png', size_hint=(None, None), size=(window_height*.12, window_height*.12), pos_hint={'center_x': 0.148, 'top': 0.28}, border=(0, 0, 0, 0))
        self.ok_button.bind(on_press=self.on_ok_button_click)
        self.layout.add_widget(self.ok_button)
        
        # Add a Combobox for signal type
        signal_types = ['Batterie', 'Lichtmaschine']
        self.signal_type_spinner = Spinner(text='Lichtmaschine', values=signal_types, size_hint=(None, None), size=(int(window_width*.2), int(window_width*.04)), pos_hint={'center_x': 0.2, 'top': 0.583}, background_color=utils.get_color_from_hex('#0046F0'), outline_color=(0, 0.2745, 0.9412, 1), disabled_outline_color=(0, 0.2745, 0.9412, 1), color='white', font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.layout.add_widget(self.signal_type_spinner)

        self.boby= Image(source='KIVYG/images/boby.png',size_hint=(.45, .45), allow_stretch=True, pos_hint={'center_x': 0.67, 'top': 0.8})
        self.layout.add_widget(self.boby)

        self.car= Image(source='KIVYG/images/car.png',size_hint=(None, None), size=(int(window_width*.09), int(window_width*.09)), pos_hint={'center_x': 0.265, 'top': 0.23})
        self.layout.add_widget(self.car)
        self.sig= Image(source='KIVYG/images/skp.png',size_hint=(None, None), size=(int(window_width*.06), int(window_width*.06)), pos_hint={'center_x': 0.265, 'top': 0.289})
        self.layout.add_widget(self.sig)
        Clock.schedule_interval(self.toggle_image_visibility, 2)
    

        # Animation
        # Animation for the new background image
        new_animation = Animation(x=0, duration=1)
        new_animation.start(self.new_background)
        Clock.schedule_once(self.delayed_appearance, 1.5)
        # Set the opacity of all widgets to 0
        for widget in [self.sig,
                       self.car, self.boby, self.ok_button, self.rig_sig_box, self.rig_sig_label, self.rem_button, self.rem_sig_box,
                        self.rem_sig_label, self.setup_sig_label, self.setup_sig_box, self.start_sig_box, self.start_sig, 
                        self.play_button2, self.signal_type_spinner, self.setup_param_label,
                        self.amplitude_label, self.frequency_label, self.amplitude_label_box,
                        self.frequency_label_box,
                        self.setup_param_box, self.amplitude_slider, self.frequency_slider]:
            widget.opacity = 0

        return self.layout
    
    def toggle_image_visibility(self, dt):
        if self.sig.opacity == 1:  # Wenn das Bild sichtbar ist
            self.sig.opacity = 0    # Bild ausblenden
        else:
            self.sig.opacity = 1    # Bild wieder anzeigen


    def on_rem_button_click(self, instance):
        # Define the range and step for random amplitude and frequency
    
        amplitude_min = 3
        amplitude_max = 5
        amplitude_step = 0.25
        frequency_min = 159
        frequency_max = 165
        frequency_step = 1
        
        # Generate random amplitude and frequency
        amplitude = round(random.uniform(amplitude_min, amplitude_max) / amplitude_step) * amplitude_step
        frequency = round(random.uniform(frequency_min, frequency_max) / frequency_step) * frequency_step
        
        signal_type = self.signal_type_spinner.text
        old_gif_path = 'KIVYG/images/animation.gif'
        
        # Delete the old GIF
        if self.signal_win is not None:
            self.layout.remove_widget(self.signal_win)
            self.signal_win = None  
        generate_custom_waveform_and_plot(signal_type, amplitude, frequency)
        
        # Wait for the new GIF to be generated

        # Remove the placeholder image and display the new GIF
        if os.path.exists(old_gif_path):
            if self.boby is not None:
                self.layout.remove_widget(self.boby)
            self.signal_win = Image(source='KIVYG/images/animation.gif', size_hint=(.5, .5), allow_stretch=True, pos_hint={'center_x': 0.7, 'top': 0.77})
            self.layout.add_widget(self.signal_win)
        self.signal_win.reload()
        self.sig.source='KIVYG/images/sg.png'
        self.sig.reload()
        
    
    def on_ok_button_click(self, instnce):
        # Ok Signals are [positive Signal in beiden Fällen bei einer Amplitude von 4 und einer Frequenz von 164]
        amplitude = 4
        frequency = 164
        signal_type = self.signal_type_spinner.text
        old_gif_path = 'KIVYG/images/animation.gif'
        # Löschen des alten GIF
        if self.signal_win is not None:
            self.layout.remove_widget(self.signal_win)
            self.signal_win =None
        
        generate_custom_waveform_and_plot(signal_type, amplitude, frequency)
        if os.path.exists(old_gif_path):
            if self.boby is not None:
                self.layout.remove_widget(self.boby)
            self.signal_win= Image(source='KIVYG/images/animation.gif',size_hint=(.5, .5), allow_stretch=True, pos_hint={'center_x': 0.7, 'top': 0.77})
            self.layout.add_widget(self.signal_win)
        self.signal_win.reload()
        self.sig.source='KIVYG/images/sg.png'
        self.sig.reload()
        
    def delayed_appearance(self, dt):
        # Start the animation to change the opacity from 0 to 1
        for widget in [self.car, self.boby, self.ok_button, self.rig_sig_box, self.rig_sig_label, self.rem_button, self.rem_sig_box, 
                        self.rem_sig_label, self.setup_sig_label, self.setup_sig_box, self.start_sig_box, self.start_sig, 
                        self.play_button2, self.signal_type_spinner, self.setup_param_label,
                        self.amplitude_label, self.frequency_label, self.amplitude_label_box,
                        self.frequency_label_box,
                        self.setup_param_box, self.amplitude_slider, self.frequency_slider]:
            Animation(opacity=1, duration=1).start(widget)


    def on_play_button_click2(self, instance):
        
        # Read parameters
        amplitude = self.amplitude_slider.value
        frequency = self.frequency_slider.value
        signal_type = self.signal_type_spinner.text
        old_gif_path = 'KIVYG/images/animation.gif'
        if self.signal_win is not None:
            self.layout.remove_widget(self.signal_win)
            self.signal_win =None
        
        generate_custom_waveform_and_plot(signal_type, amplitude, frequency)
        if os.path.exists(old_gif_path):
            if self.boby is not None:
                self.layout.remove_widget(self.boby)
            self.signal_win= Image(source='KIVYG/images/animation.gif',size_hint=(.5, .5), allow_stretch=True, pos_hint={'center_x': 0.7, 'top': 0.77})
            self.layout.add_widget(self.signal_win)
        self.signal_win.reload()
        
        # Function to generate the animation in a separate thread
        # Perform the animation based on the read parameters
        print(f'Amplitude: {amplitude}, Frequenz: {frequency}, Signaltyp: {signal_type}')
        self.sig.source='KIVYG/images/sg.png'
        self.sig.reload()
        return self.layout


        

if __name__ == '__main__':
    SignalclassifierApp().run()

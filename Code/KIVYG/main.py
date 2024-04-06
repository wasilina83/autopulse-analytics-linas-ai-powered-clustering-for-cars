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
import sys
sys.path.insert(0, 'DataMaker')
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
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[(20, 20), (20, 20), (20, 20), (20, 20)])

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
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[(20, 20), (20, 20), (20, 20), (20, 20)])

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
        self.text_label3 = Label(text=f'Signalgenerator \n        starten', font_size=win_h*.06, pos_hint={'center_x': .29, 'top': .7}, font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.layout.add_widget(self.text_label3)

        # Load the image for the Play button
        self.play_button = Button(background_normal='KIVYG/images/play.png', size_hint=(None, None), size=(win_h*.28, win_h*.28), pos_hint={'center_x': .3, 'top': .6}, border=(0, 0, 0, 0))
        self.play_button.bind(on_press=self.on_play_button_click)
        self.layout.add_widget(self.play_button)

        return self.layout


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
        self.amplitude_slider = CustomSlider(min=3, max=5, step=.25, orientation='horizontal', size_hint=(None, None), size=(int(window_width*.33), int(window_height*.055)), pos_hint={'center_x': 0.2, 'top': 0.835})
        self.frequency_slider = CustomSlider(min=159, max=165, step=1, orientation='horizontal', size_hint=(None, None), size=(int(window_width*.33), int(window_height*.055)), pos_hint={'center_x': 0.2, 'top': 0.705})
        # self.offset_slider = CustomSlider(min=-1, max=1, step=.1, orientation='horizontal', size_hint=(None, None), size=(500, 60), pos_hint={'center_x': 0.2, 'top': 0.6})
        # self.phase_shift_slider = CustomSlider(min=0, max=2*math.pi, step=math.pi/8, orientation='horizontal', size_hint=(None, None), size=(500, 60), pos_hint={'center_x': 0.2, 'top': 0.5})
        self.layout.add_widget(self.amplitude_slider)
        self.layout.add_widget(self.frequency_slider)
        # self.layout.add_widget(self.offset_slider)
        # self.layout.add_widget(self.phase_shift_slider)
        
        # Add Labels for the Slider values
        self.amplitude_label_box = CustomLabel(size_hint=(None, None), size=(int(window_width*.33), int(window_height*.045)), pos_hint={'center_x': 0.2, 'top': 0.89}, color=(1, 1, 1, 1))
        self.frequency_label_box = CustomLabel(size_hint=(None, None), size=(int(window_width*.33), int(window_height*.045)), pos_hint={'center_x': 0.2, 'top': 0.76}, color=(1, 1, 1, 1))
        # self.offset_label_box = CustomLabel( size_hint=(None, None), size=(500, 45), pos_hint={'center_x': 0.2, 'top': 0.64}, color=(1, 1, 1, 1))
        # self.phase_shift_label_box = CustomLabel(size_hint=(None, None), size=(500, 45), pos_hint={'center_x': 0.2, 'top': 0.54}, color=(1, 1, 1, 1))
        self.setup_param_box = CustomLabel(text=f'Sätze die Parameter nach wunsch', size_hint=(None, None), size=(int(window_width*.35), int(window_height*.06)), pos_hint={'center_x': 0.2, 'top': .96}, color=(1, 1, 1, 1))
        self.start_sig_box = CustomLabel(text=f'Signal gererieren', size_hint=(None, None), size=(int(window_width*.15), int(window_height*.1)), pos_hint={'center_x': 0.25, 'top': 0.3}, color=(1, 1, 1, 1))
        self.layout.add_widget(self.start_sig_box)
        self.layout.add_widget(self.setup_param_box)
        self.layout.add_widget(self.amplitude_label_box)
        self.layout.add_widget(self.frequency_label_box)
        # self.layout.add_widget(self.offset_label_box)
        # self.layout.add_widget(self.phase_shift_label_box)
        self.amplitude_label = Label(text=f'Amplitude: {self.amplitude_slider.value}', size_hint=(None, None), size=(int(window_width*.25), int(window_height*.045)), pos_hint={'center_x': 0.2, 'top': 0.89}, color=(1, 1, 1, 1), font_size='15sp',font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.frequency_label = Label(text=f'Frequenz: {self.frequency_slider.value}', size_hint=(None, None), size=(int(window_width*.25), int(window_height*.045)), pos_hint={'center_x': 0.2, 'top': 0.76}, color=(1, 1, 1, 1), font_size='15sp',font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        # self.offset_label = Label(text=f'Offset: {self.offset_slider.value}', size_hint=(None, None), size=(500, 45), pos_hint={'center_x': 0.2, 'top': 0.64}, color=(1, 1, 1, 1), font_size='15sp')
        # self.phase_shift_label = Label(text=f'Phasenverschiebung: {self.phase_shift_slider.value}', size_hint=(None, None), size=(500, 45), pos_hint={'center_x': 0.2, 'top': 0.54}, color=(1, 1, 1, 1), font_size='15sp')
        self.setup_param_label = Label(text=f'Sätze die Parameter nach Wunsch', size_hint=(None, None), size=(int(window_width*.25), int(window_height*.05)), pos_hint={'center_x': 0.2, 'top': 0.96}, color=(1, 1, 1, 1), font_size='20sp', font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.start_sig = Label(text=f'     Signal \ngenerieren', size_hint=(None, None), size=(int(window_width*.15), int(window_height*.1)), pos_hint={'center_x': 0.25, 'top': 0.3}, color=(1, 1, 1, 1), font_size='20sp',  font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.layout.add_widget(self.start_sig)
        self.layout.add_widget(self.setup_param_label)
        self.layout.add_widget(self.amplitude_label)
        self.layout.add_widget(self.frequency_label)
        # self.layout.add_widget(self.offset_label)
        # self.layout.add_widget(self.phase_shift_label)

        # Add a Combobox for signal type
        signal_types = ['Batterie', 'Lichtmaschine']
        self.signal_type_spinner = Spinner(text='Lichtmaschine', values=signal_types, size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.2, 'top': 0.4}, background_color=(0, 0.2745, 0.9412, 1), outline_color=(0, 0.2745, 0.9412, 1), disabled_outline_color=(0, 0.2745, 0.9412, 1), color='white', font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.layout.add_widget(self.signal_type_spinner)

        # Load the Play button
        self.play_button2 = Button(background_normal='KIVYG/images/play.png', size_hint=(None, None), size=(150, 150), pos_hint={'center_x': 0.25, 'top': 0.2}, border=(0, 0, 0, 0))
        self.play_button2.bind(on_press=self.on_play_button_click2)
        self.layout.add_widget(self.play_button2)
        # Animation
        # Animation for the new background image
        new_animation = Animation(x=0, duration=1)
        new_animation.start(self.new_background)
        Clock.schedule_once(self.delayed_appearance, 1.5)
        # Set the opacity of all widgets to 0
        for widget in [self.start_sig_box, self.start_sig, self.play_button2, self.signal_type_spinner, self.setup_param_label,
                        self.amplitude_label, self.frequency_label, self.amplitude_label_box,
                        self.frequency_label_box,
                        self.setup_param_box, self.amplitude_slider, self.frequency_slider]:
            widget.opacity = 0

        return self.layout

    def delayed_appearance(self, dt):
        # Start the animation to change the opacity from 0 to 1
        for widget in [self.start_sig_box, self.start_sig, self.play_button2, self.signal_type_spinner, self.setup_param_label,
                    self.amplitude_label, self.frequency_label, self.amplitude_label_box,
                    self.frequency_label_box, self.setup_param_box, self.amplitude_slider, self.frequency_slider]:
            Animation(opacity=1, duration=1).start(widget)
    

    def on_play_button_click2(self, instance):
        # Read parameters
        amplitude = self.amplitude_slider.value
        frequency = self.frequency_slider.value
        offset = self.offset_slider.value
        phase_shift = self.phase_shift_slider.value
        signal_type = self.signal_type_spinner.text
        duration = 3
        def start_test(dt):
            test=1
            if test == 1:
                test = genSigPNG(signal_type, duration, amplitude, frequency, offset, phase_shift)
            else:
                print("Test beendet, KIVYG wird aktualisiert.")
                Clock.unschedule(start_test)    # Hier können Sie Ihre KIVYG-Update-Logik einfügen
        test=1        
        Clock.schedule_interval(start_test, 5)  # Überprüfen Sie jede 0,1 Sekunde, ob 'test'
        self.replay_button = Button(background_normal='KIVYG/images/wiederholen.png', size_hint=(None, None), size=(150, 150), pos_hint={'center_x': 0.09, 'top': 0.2}, border=(0, 0, 0, 0))
        self.replay_button.bind(on_press=self.on_replay_button_click)
        self.layout.add_widget(self.replay_button)
        self.restart_sig_box = CustomLabel(text=f'Signal gererieren', size_hint=(None, None), size=(300, 70), pos_hint={'center_x': 0.09, 'top': 0.3}, color=(1, 1, 1, 1) )
        self.layout.add_widget(self.restart_sig_box)
        self.restart_sig = Label(text=f'Neues Signal \n gererieren', size_hint=(None, None), size=(300, 70), pos_hint={'center_x': 0.09, 'top': 0.3}, color=(1, 1, 1, 1), font_size='20sp')
        self.layout.add_widget(self.restart_sig)
        self.signal_win= Image(source='KIVYG/images/animation.gif',size_hint=(.55, .55), allow_stretch=True, pos_hint={'center_x': 0.7, 'top': 0.85})
        self.layout.add_widget(self.signal_win)
        # Function to generate the animation in a separate thread
        #generate_custom_waveform_and_plot(signal_type, duration, amplitude, frequency, offset, phase_shift)
        # Perform the animation based on the read parameters
        print(f'Amplitude: {amplitude}, Frequenz: {frequency}, Offset: {offset}, Phasenverschiebung: {phase_shift}, Signaltyp: {signal_type}')
        
        return self.layout
    
    def on_replay_button_click(self, instanze):
        # Read parameters
        self.layout.remove_widget(self.signal_win)
        amplitude = self.amplitude_slider.value
        frequency = self.frequency_slider.value
        offset = self.offset_slider.value
        phase_shift = self.phase_shift_slider.value
        signal_type = self.signal_type_spinner.text
        duration = 3
        def start_test(dt):
            test=1
            if test == 1:
                test = genSigPNG(signal_type, duration, amplitude, frequency, offset, phase_shift)
                print("Test beendet, KIVYG wird aktualisiert.")
                Clock.unschedule(start_test)
            else:
                pass
        test= 1
        Clock.schedule_interval(start_test, 5)
        self.signal_win= Image(source='KIVYG/images/animation.gif',size_hint=(.55, .55), allow_stretch=True, pos_hint={'center_x': 0.7, 'top': 0.85})
        self.layout.add_widget(self.signal_win)
        # Function to generate the animation in a separate thread
        #
        #generate_custom_waveform_and_plot(signal_type, duration, amplitude, frequency, offset, phase_shift)
        # Perform the animation based on the read parameters
        print(f'Amplitude: {amplitude}, Frequenz: {frequency}, Offset: {offset}, Phasenverschiebung: {phase_shift}, Signaltyp: {signal_type}')
        return self.layout
    
    
        

if __name__ == '__main__':
    SignalclassifierApp().run()

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
from kivy.properties import StringProperty, ObjectProperty
# Create a font context containing system fonts + one custom TTF

class SignalclassifierLayout(RelativeLayout):
    def refreshWindow(self):
        # Pfad zum alten GIF
        old_gif_path = 'GUI/images/animation.gif'
        # Löschen des alten GIF
        if os.path.exists(old_gif_path):
            os.remove(old_gif_path)

        
        # Aktualisieren der Bildquelle im Kivy-Layout
        self.ids.gif.source = old_gif_path

        # Neuzeichnen des Bildes
        self.ids.gif.reload()


        
class CustomLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Initialize the rectangle with graphics instructions
        with self.canvas:
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
    value_track=True

    def create_graphics_instructions(self, dt):
        
        # Initialize the rectangle with graphics instructions
        with self.canvas.before:
            Color(255,255,255)  # Set the color to blue
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
        self.signal_type = StringProperty('')

        # Load the background image
        self.background = Image(source='GUI/images/BG.png', allow_stretch=True, keep_ratio=False)

        # Add the image to the layout
        self.layout.add_widget(self.background)


        # Add a text label before the image
        win_w, win_h = Window.size

        # Load the image for the logo (with transparent background)
        self.logo = Image(source='GUI/images/Autowerkstatt_Logo_White-768x179.png', allow_stretch=True, keep_ratio=True, size_hint=(.75, .75),  pos_hint={'center_x': .4, 'top': .986})
        self.layout.add_widget(self.logo)
        self.prolab = Image(source='GUI/images/prolab.png', size_hint=(None, None), size=(win_h*.98, win_h*.98), allow_stretch=True, keep_ratio=True, pos_hint={'center_x': 0.159, 'top': .37})
        self.layout.add_widget(self.prolab)

        # Load the image for the Play button
        self.play_button = Button(background_normal='GUI/images/play1.png', size_hint=(None, None), size=(win_h*.58, win_h*.58), pos_hint={'center_x': .5, 'top': .5}, border=(0, 0, 0, 0))
        self.play_button.bind(on_press=self.on_play_button_click)
        self.layout.add_widget(self.play_button)
        self.esxit_button = Button(background_normal='GUI/images/schaltflache-abbrechen.png', size_hint=(None, None), size=(win_h*.2, win_h*.2),  pos_hint={'center_x': .96, 'top': .991}, border=(0, 0, 0, 0) )
        self.esxit_button.bind(on_press = self.on_exit_click)
        self.layout.add_widget(self.esxit_button)

        return self.layout
    
    def on_exit_click(self, instance):
        App.get_running_app().stop()
        quit()
         
    def on_play_button_click(self, instance):
        
        # Remove the Play button and Label3
        self.layout.remove_widget(self.play_button)
        self.layout.remove_widget(self.logo)
        self.layout.remove_widget(self.esxit_button)

        # Load the new background image
        
        self.new_background = Image(source='GUI/images/BGWeis.png', allow_stretch=True, keep_ratio=False, size_hint_x=0.2,  pos_hint={'right': 1})
        self.new_background.x=Window.width - self.new_background.texture_size[0]
        self.layout.add_widget(self.new_background)
        self.logo = Image(source='GUI/images/lmis-ag-gf-logo-autowerkstatt-vierpunktnull-cmyk-de.png', size_hint=(None, None), size=(int(Window.width*.4), int(Window.width*.4)), pos_hint={'right':1.125, 'top': 0.9})
        self.layout.add_widget(self.logo)
        
        
        # Add Sliders for the parameters
        self.amplitude_slider = CustomSlider(min=3, max=5, step=.25,  orientation='horizontal', value=4,size_hint=(None, None), size=(int(Window.width*.53), int(Window.height*.065)), pos_hint={'center_x': 0.425, 'top': 0.535}, value_track_color=utils.get_color_from_hex('#0046F0'))
        self.frequency_slider = CustomSlider(min=159, max=165, step=1, orientation='horizontal', value=162, size_hint=(None, None), size=(int(Window.width*.53), int(Window.height*.065)), pos_hint={'center_x': 0.425, 'top': 0.405}, value_track_color=utils.get_color_from_hex('#0046F0'))
        self.amplitude_label = Label(text=f'Amplitude: {self.amplitude_slider.value}', size_hint=(None, None), size=(int(Window.width*.55), int(Window.height*.045)), pos_hint={'center_x': 0.425, 'top': 0.59}, color=utils.get_color_from_hex('#0046F0'), font_size='27sp',  font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.frequency_label = Label(text=f'Frequency: {self.frequency_slider.value}', size_hint=(None, None), size=(int(Window.width*.55), int(Window.height*.045)), pos_hint={'center_x': 0.425, 'top': 0.46}, color=utils.get_color_from_hex('#0046F0'), font_size='27sp',  font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        
        def OnamplitudeValueChange(instance, value):
            self.amplitude_label.text = f"Amplitude: {value}"

    # Define the OnfrequencyValueChange function outside of the on_play_button_click method
        def OnfrequencyValueChange(instance,  value): 
            self.frequency_label.text = f"Frequency: {value}"


        self.frequency_slider.bind(value=OnfrequencyValueChange)
        self.amplitude_slider.bind(value=OnamplitudeValueChange)
        self.layout.add_widget(self.amplitude_slider)
        self.layout.add_widget(self.frequency_slider)
       
        # Add Labels for the Slider values
        self.amplitude_label_box = CustomLabel(size_hint=(None, None), size=(int(Window.width*.53), int(Window.height*.045)), pos_hint={'center_x': 0.425, 'top': 0.59}, color=utils.get_color_from_hex('#0046F0'))
        self.frequency_label_box = CustomLabel(size_hint=(None, None), size=(int(Window.width*.53), int(Window.height*.045)), pos_hint={'center_x': 0.425, 'top': 0.46}, color=utils.get_color_from_hex('#0046F0'))
        self.layout.add_widget(self.amplitude_label_box)
        self.layout.add_widget(self.frequency_label_box)
        self.setup_param_box = CustomLabel(text=f'Komp', size_hint=(None, None), size=(int(Window.width*.625), int(Window.height*.06)), pos_hint={'center_x': 0.425, 'top': .98})
        self.setup_param_label = Label(text=f'Select a vehicle component', size_hint=(None, None), size=(int(Window.width*.625), int(Window.height*.05)), pos_hint={'center_x': 0.425, 'top': 0.98}, color=utils.get_color_from_hex('#0046F0'), font_size='27sp', font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.setup_param_label.bind(on_press=self.on_but_button_click)
        self.setup_param_label.bind(on_press=self.on_Lichtmaschine_button_click)
        self.layout.add_widget(self.setup_param_box)
        self.layout.add_widget(self.setup_param_label)
        self.start_sig_box = CustomLabel(text=f'Gererieren', size_hint=(None, None), size=(int(Window.height*.4), int(Window.height*.12)), pos_hint={'center_x': 0.6, 'top': 0.208}, color=(1, 1, 1, 1))
        self.start_sig = Label(text=f'Generate custom signal', size_hint=(None, None), size=(int(Window.height*.4), int(Window.height*.12)), pos_hint={'center_x': 0.6, 'top': 0.208}, color=utils.get_color_from_hex('#0046F0'), font_size='30sp',  font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.play_button2_image = Image(source='GUI/images/play.png', size_hint=(None, None), size=(int(Window.height*.16), int(Window.height*.16)), pos_hint={'center_x': 0.52, 'top': 0.288})
        self.play_button2 = Button( background_color= (0, 0, 0, 0), size_hint=(None, None), size=(int(Window.height*.5), (Window.height*.19)), pos_hint={'center_x': 0.59, 'top': 0.288}, border=(0, 0, 0, 0))
        self.play_button2.bind(on_press=self.on_play_button_click2)
        self.layout.add_widget(self.start_sig_box)
        self.layout.add_widget(self.start_sig)
        self.layout.add_widget(self.play_button2_image)
        self.layout.add_widget(self.play_button2)

        self.setup_param_box1 = CustomLabel(text=f'Gen', size_hint=(None, None), size=(int(Window.width*.15), int(Window.height*.06)), pos_hint={'center_x': 0.425, 'top': .85})
        self.setup_param_label1 = Label(text=f'Generate: ', size_hint=(None, None), size=(int(Window.width*.15), int(Window.height*.05)), pos_hint={'center_x': 0.425, 'top': 0.85}, color=utils.get_color_from_hex('#0046F0'), font_size='27sp', font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.layout.add_widget(self.setup_param_box1)
        self.layout.add_widget(self.setup_param_label1)

        self.setup_param_box2 = CustomLabel(text=f'Or', size_hint=(None, None), size=(int(Window.width*.05), int(Window.height*.06)), pos_hint={'center_x': 0.425, 'top': .79})
        self.setup_param_label2 = Label(text=f'or', size_hint=(None, None), size=(int(Window.width*.05), int(Window.height*.05)), pos_hint={'center_x': 0.425, 'top': 0.79}, color=utils.get_color_from_hex('#0046F0'), font_size='27sp', font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.layout.add_widget(self.setup_param_box2)
        self.layout.add_widget(self.setup_param_label2)



               
        self.layout.add_widget(self.amplitude_label)
        self.layout.add_widget(self.frequency_label)

        # self.setup_sig_label = Label(text=f'Komponente wählen', size_hint=(None, None), size=(int(Window.width*.25), int(Window.height*.05)), pos_hint={'center_x': 0.2, 'top': 0.63}, color=(1, 1, 1, 1), font_size='13sp', font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        # self.setup_sig_box = CustomLabel(text=f'sig', size_hint=(None, None), size=(int(Window.width*.25), int(Window.height*.05)), pos_hint={'center_x': 0.2, 'top': .635}, color=(1, 1, 1, 1))
        # self.layout.add_widget(self.setup_sig_box)
        # self.layout.add_widget(self.setup_sig_label)
        # #Zufals Signal
        self.rem_sig_label = Label(text=f'Random signal', size_hint=(None, None), size=(int(Window.height*.4),int(Window.height*.12)), pos_hint={'center_x': 0.25, 'top': 0.908-.2}, color=utils.get_color_from_hex('#0046F0'), font_size='30sp',  font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.rem_sig_box = CustomLabel(text=f'zu sig', size_hint=(None, None), size=(int(Window.height*.4),int(Window.height*.12)), pos_hint={'center_x': 0.25, 'top': 0.908-.2}, color=(1, 1, 1, 1))
        self.layout.add_widget(self.rem_sig_box)
        self.layout.add_widget(self.rem_sig_label)
        self.rem_button_image = Image(source='GUI/images/rem.png', size_hint=(None, None), size=(Window.height*.14, Window.height*.14), pos_hint={'center_x': 0.36, 'top': 0.99-.2})
        self.layout.add_widget(self.rem_button_image)
        self.rem_button = Button(background_color= (0, 0, 0, 0), size_hint=(None, None), size=(int(Window.height*.4),int(Window.height*.22)), pos_hint={'center_x': 0.25, 'top': 0.99-.2}, border=(0, 0, 0, 0))
        self.rem_button.bind(on_press=self.on_rem_button_click)
        self.layout.add_widget(self.rem_button)
        #Richtiges Signal
        self.rig_sig_label = Label(text=f'Reference signal', size_hint=(None, None), size=(int(Window.height*.4),int(Window.height*.12)), pos_hint={'center_x': 0.6, 'top': 0.9089-.2}, color=utils.get_color_from_hex('#0046F0'), font_size='30sp',  font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.rig_sig_box = CustomLabel(text=f'sig', size_hint=(None, None), size=(int(Window.height*.4),int(Window.height*.12)), pos_hint={'center_x': 0.6, 'top': 0.908-.2}, color=(1, 1, 1, 1))
        self.layout.add_widget(self.rig_sig_box)
        self.layout.add_widget(self.rig_sig_label)
        self.ok_button_image = Image(source='GUI/images/uberprufen.png', size_hint=(None, None), size=(Window.height*.12, Window.height*.12), pos_hint={'center_x': 0.648, 'top': 0.99-.2})
        self.layout.add_widget(self.ok_button_image)
        self.ok_button = Button(background_color= (0, 0, 0, 0), size_hint=(None, None), size=(int(Window.height*.4),int(Window.height*.22)), pos_hint={'center_x': 0.61, 'top': 0.99-.2}, border=(0, 0, 0, 0))
        self.ok_button.bind(on_press=self.on_ok_button_click)
        self.layout.add_widget(self.ok_button)

        
        self.bat_button_label = Label(text=f'Battery', size_hint=(None, None), size=(int(Window.height*.4),int(Window.height*.092)), pos_hint={'center_x': 0.25, 'top': .94}, color=utils.get_color_from_hex('#0046F0'), font_size='25sp',  font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.bat_button_box = CustomLabel(text=f'sig', size_hint=(None, None), size=(int(Window.height*.4),int(Window.height*.092)), pos_hint={'center_x': 0.25, 'top': .94})
        self.layout.add_widget(self.bat_button_box)
        self.layout.add_widget(self.bat_button_label)
        self.bat_button = Button(background_color=(0,0,0,0), size_hint=(None, None), size=(Window.height*.4, Window.height*.092), pos_hint={'center_x': 0.25, 'top': .94}, color=utils.get_color_from_hex('#0046F0'))
        self.bat_button.bind(on_press=self.on_but_button_click)
        self.layout.add_widget(self.bat_button)
        
        self.Lichtmaschine_button_label = Label(text=f'Alternator', size_hint=(None, None), size=(int(Window.height*.4),int(Window.height*.092)), pos_hint={'center_x': 0.6, 'top': .94}, color=utils.get_color_from_hex('#0046F0'), font_size='25sp',  font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        self.Lichtmaschine_button_box = CustomLabel(text=f'sig', size_hint=(None, None), size=(int(Window.height*.4),int(Window.height*.092)), pos_hint={'center_x': 0.6, 'top': .94}, color=(1, 1, 1, 1))
        self.layout.add_widget(self.Lichtmaschine_button_box)
        self.layout.add_widget(self.Lichtmaschine_button_label)
        self.Lichtmaschine_button = Button(background_color=(0,0,0,0), size_hint=(None, None), size=(int(Window.height*.4),int(Window.height*.092)), pos_hint={'center_x': 0.6, 'top': .94}, color=utils.get_color_from_hex('#0046F0'))
        self.Lichtmaschine_button.bind(on_press=self.on_Lichtmaschine_button_click)
        self.layout.add_widget(self.Lichtmaschine_button)
        
        # Add a Combobox for signal type
        # signal_types = ['Batterie', 'Lichtmaschine']
        # self.signal_type_spinner = Spinner(text='Lichtmaschine', values=signal_types, size_hint=(None, None), size=(int(Window.width*.2), int(Window.width*.04)), pos_hint={'center_x': 0.2, 'top': 0.583}, background_color=utils.get_color_from_hex('#0046F0'), outline_color=(0, 0.2745, 0.9412, 1), disabled_outline_color=(0, 0.2745, 0.9412, 1), color='white', font_context='system://myapp', font_name='OpenSans-Bold.ttf')
        # self.layout.add_widget(self.signal_type_spinner)

        #self.boby= Image(source='GUI/images/boby.png',size_hint=(.45, .45), allow_stretch=True, pos_hint={'center_x': 0.67, 'top': 0.8})
        #self.layout.add_widget(self.boby)
        

        self.car= Image(source='GUI/images/car.png',size_hint=(None, None), size=(int(Window.width*.09), int(Window.width*.09)), pos_hint={'center_x': 0.265+.1, 'top': 0.23})
        #self.layout.add_widget(self.car)
        self.sig= Image(source='GUI/images/skp.png',size_hint=(None, None), size=(int(Window.width*.06), int(Window.width*.06)), pos_hint={'center_x': 0.265+.1, 'top': 0.289})
        #self.layout.add_widget(self.sig)
        Clock.schedule_interval(self.toggle_image_visibility, 2)
        self.esxit_button2 = Button(background_normal='GUI/images/schaltflache-abbrechen.png', size_hint=(None, None), size=(Window.height*.05, Window.height*.05), pos_hint={'center_x': .05, 'top': .991}, border=(0, 0, 0, 0) )
        self.esxit_button2.bind(on_press = self.on_exit_click)
        #self.layout.add_widget(self.esxit_button2)
    

        # Animation
        # Animation for the new background image
        new_animation = Animation(x=0, duration=1)
        new_animation.start(self.new_background)
        Clock.schedule_once(self.delayed_appearance, 1.5)
        # Set the opacity of all widgets to 0
        for widget in [self.sig,
                       self.car,  self.ok_button_image,self.ok_button, self.rig_sig_box, self.rig_sig_label, self.rem_button, self.rem_button_image, self.rem_sig_box,
                        self.rem_sig_label, self.start_sig_box, self.start_sig, 
                        self.play_button2, self.play_button2_image, self.setup_param_label,
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

    def on_but_button_click(self,instance):
        self.signal_type = 'Batterie'
        self.setup_param_label.text = f'The {self.bat_button_label.text.lower()} is selected'

    def on_Lichtmaschine_button_click(self, instance):
        self.signal_type = 'Lichtmaschine'
        self.setup_param_label.text = f'The {self.Lichtmaschine_button_label.text.lower()} is selected'


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
        
        signal_type = self.signal_type
        old_gif_path = 'GUI/images/animation.gif'
        
        # Delete the old GIF
        if self.signal_win is not None:
            self.layout.remove_widget(self.signal_win)
            self.signal_win = None  
        generate_custom_waveform_and_plot(signal_type, amplitude, frequency)
        
        # Wait for the new GIF to be generated

        # Remove the placeholder image and display the new GIF
        # if os.path.exists(old_gif_path):
        #     # if self.boby is not None:
        #     #     self.layout.remove_widget(self.boby)
        #     self.signal_win = Image(source='GUI/images/animation.gif', size_hint=(.5, .5), allow_stretch=True, pos_hint={'center_x': 0.7, 'top': 0.77})
        #     self.layout.add_widget(self.signal_win)
        # self.signal_win.reload()
        # self.sig.source='GUI/images/sg.png'
        # self.sig.reload()
        
    
    def on_ok_button_click(self, instnce):
        # Ok Signals are [positive Signal in beiden Fällen bei einer Amplitude von 4 und einer Frequenz von 164]
        amplitude = 4
        frequency = 164
        signal_type = self.signal_type
        old_gif_path = 'GUI/images/animation.gif'
        # Löschen des alten GIF
        if self.signal_win is not None:
            self.layout.remove_widget(self.signal_win)
            self.signal_win =None
        
        generate_custom_waveform_and_plot(signal_type, amplitude, frequency)
        # if os.path.exists(old_gif_path):
        #     # if self.boby is not None:
        #     #     self.layout.remove_widget(self.boby)
        #     self.signal_win= Image(source='GUI/images/animation.gif',size_hint=(.5, .5), allow_stretch=True, pos_hint={'center_x': 0.7, 'top': 0.77})
        #     self.layout.add_widget(self.signal_win)
        # self.signal_win.reload()
        # self.sig.source='GUI/images/sg.png'
        # self.sig.reload()
        
    def delayed_appearance(self, dt):
        # Start the animation to change the opacity from 0 to 1
        for widget in [self.car,  self.ok_button, self.ok_button_image, self.rig_sig_box, self.rig_sig_label, self.rem_button, self.rem_button_image, self.rem_sig_box, 
                        self.rem_sig_label, self.start_sig_box, self.start_sig, 
                        self.play_button2, self.play_button2_image, self.setup_param_label,
                        self.amplitude_label, self.frequency_label, self.amplitude_label_box,
                        self.frequency_label_box,
                        self.setup_param_box, self.amplitude_slider, self.frequency_slider]:
            Animation(opacity=1, duration=1).start(widget)


    def on_play_button_click2(self, instance):
        
        # Read parameters
        amplitude = self.amplitude_slider.value
        frequency = self.frequency_slider.value
        signal_type = self.signal_type
        old_gif_path = 'GUI/images/animation.gif'
        if self.signal_win is not None:
            self.layout.remove_widget(self.signal_win)
            self.signal_win =None
        
        generate_custom_waveform_and_plot(signal_type, amplitude, frequency)
        # if os.path.exists(old_gif_path):
        #     # if self.boby is not None:
        #     #     self.layout.remove_widget(self.boby)
        #     self.signal_win= Image(source='GUI/images/animation.gif',size_hint=(.5, .5), allow_stretch=True, pos_hint={'center_x': 0.7, 'top': 0.77})
        #     self.layout.add_widget(self.signal_win)
        # self.signal_win.reload()
        
        # Function to generate the animation in a separate thread
        # Perform the animation based on the read parameters
        print(f'Amplitude: {amplitude}, Frequenz: {frequency}, Signaltyp: {signal_type}')
        self.sig.source='GUI/images/sg.png'
        self.sig.reload()
        return self.layout


        

if __name__ == '__main__':
    SignalclassifierApp().run()

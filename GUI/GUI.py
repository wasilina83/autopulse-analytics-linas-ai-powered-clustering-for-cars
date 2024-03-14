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
import sys
sys.path.insert(0, r'Code\DataMaker')
from SignalGenerator import signal_functions, noise_beta, genSigPNG
import math

class SignalclassifierApp(App):
    def build(self):
        # Erstelle ein RelativeLayout als Hauptlayout
        self.layout = RelativeLayout()

        # Lade das Hintergrundbild
        self.background = Image(source='GUI/images/BG.png', allow_stretch=True, keep_ratio=False)

        # Füge das Bild zum Layout hinzu
        self.layout.add_widget(self.background)

        # Füge einen Text (Label) hinzu, der vor dem Bild liegt
        window_width, window_height = Window.size
        text_size = int(min(window_width, window_height * .1))
        text_pos_x = window_width * .5
        text_pos_y = window_height * .75
        # Lade das Bild für das Logo (mit transparentem Hintergrund)
        logo_size = int(window_width*1.6)  # 20% der kleineren Dimension
        prolab_size = int(window_width*0.7)
        logo_pos_x = window_width * 0.1
        logo_pos_y = window_height * 0.5  # 50% der Höhe
        self.logo = Image(source='GUI/images/logo.png', size_hint=(None, None), size=(logo_size, logo_size), pos_hint={'center_x': 0.49, 'top': 1.4})
        self.layout.add_widget(self.logo)
        self.prolab = Image(source='GUI/images/prolab.png', size_hint=(None, None), size=(prolab_size, prolab_size), allow_stretch=True, keep_ratio=True, pos_hint={'center_x': 0.8, 'top': .45})
        self.layout.add_widget(self.prolab)

        # Füge andere Widgets oder Elemente hinzu, falls benötigt
        self.text_label3 = Label(text='Analyse starten', font_size=text_size*.8, pos_hint={'center_x': text_pos_x / window_width -.15, 'top':  1})
        self.layout.add_widget(self.text_label3)

        # Lade das Bild für den Play-Button
        play_button_size = int(min(window_width, window_height)*.4)  # 10% der kleineren Dimension
        play_button_pos_x = window_width * 0.9
        self.play_button = Button(background_normal='GUI/images/play.png', size_hint=(None, None), size=(play_button_size, play_button_size), pos_hint={'center_x': text_pos_x / window_width -.15, 'top':  .35}, border=(0, 0, 0, 0))
        self.play_button.bind(on_press=self.on_play_button_click)
        self.layout.add_widget(self.play_button)

        return self.layout

    def on_play_button_click(self, instance):

        # Entferne den Play-Button und das Label3
        self.layout.remove_widget(self.play_button)
        self.layout.remove_widget(self.text_label3)
        self.layout.remove_widget(self.logo)

        # Lade das neue Hintergrundbild
        window_width, window_height = Window.size
        logo_size = int(window_width*.39)
        self.new_background = Image(source='GUI/images/BGWeis.png', allow_stretch=True, keep_ratio=False, x=-Window.width, size_hint_x=0.5)
        self.layout.add_widget(self.new_background)
        self.logo = Image(source='GUI/images/logo.png', size_hint=(None, None), size=(logo_size, logo_size), pos_hint={'center_x': .78, 'top': 1.199})
        self.layout.add_widget(self.logo)

        # Animation für das neue Hintergrundbild
        new_animation = Animation(x=0, duration=1)
        new_animation.start(self.new_background)
        # Füge Slider für die Parameter hinzu
        self.amplitude_slider = Slider(min=0, max=5, step=.5, orientation='horizontal', size_hint=(None, None), size=(500, 200), pos_hint={'center_x': 0.2, 'top': 0.8}, value_track=True, value_track_color='blue')
        self.frequency_slider = Slider(min=0, max=10, step=.5, orientation='horizontal', size_hint=(None, None), size=(500, 200), pos_hint={'center_x': 0.2, 'top': 0.7}, value_track=True, value_track_color='blue')
        self.offset_slider = Slider(min=0, max=10, step=.1, orientation='horizontal', size_hint=(None, None), size=(500, 200), pos_hint={'center_x': 0.2, 'top': 0.6}, value_track_color= (0, 0.2745, 0.9412, 1), value_track=True)
        self.phase_shift_slider = Slider(min=0, max=2*math.pi, step=math.pi/8, orientation='horizontal', size_hint=(None, None), size=(500, 200), pos_hint={'center_x': 0.2, 'top': 0.5}, value_track=True, value_track_color='blue')
        # Beispiel für Ändern der Farbe der Slider
        self.amplitude_slider.background_color = (0, 0.2745, 0.9412, 1)  # Hintergrundfarbe
        self.amplitude_slider.foreground_color = (0, 0.2745, 0.9412, 1)  # Farbe der Leiste

        self.frequency_slider.background_color = (0, 0.2745, 0.9412, 1)
        self.frequency_slider.foreground_color = (0, 0.2745, 0.9412, 1)

        self.offset_slider.background_color = (0, 0.2745, 0.9412, 1)
        self.offset_slider.foreground_color = (0, 0.2745, 0.9412, 1)

        self.phase_shift_slider.background_color = (0, 0.2745, 0.9412, 1)
        self.phase_shift_slider.foreground_color = (0, 0.2745, 0.9412, 1)
        self.layout.add_widget(self.amplitude_slider)
        self.layout.add_widget(self.frequency_slider)
        self.layout.add_widget(self.offset_slider)
        self.layout.add_widget(self.phase_shift_slider)
        
        # Füge Labels für die Slider-Werte hinzu
        self.amplitude_label = Label(text=f'Amplitude: {self.amplitude_slider.value}', size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.2, 'top': 0.76}, color = (0, 0.2745, 0.9412, 1))
        self.frequency_label = Label(text=f'Frequenz: {self.frequency_slider.value}', size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.2, 'top': 0.66}, color = (0, 0.2745, 0.9412, 1))
        self.offset_label = Label(text=f'Offset: {self.offset_slider.value}', size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.2, 'top': 0.56}, color = (0, 0.2745, 0.9412, 1))
        self.phase_shift_label = Label(text=f'Phasenverschiebung: {self.phase_shift_slider.value}', size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.2, 'top': 0.46}, color = (0, 0.2745, 0.9412, 1))
        self.layout.add_widget(self.amplitude_label)
        self.layout.add_widget(self.frequency_label)
        self.layout.add_widget(self.offset_label)
        self.layout.add_widget(self.phase_shift_label)

        # Füge Combobox für Signaltyp hinzu
        signal_types = ['Schuhe', 'Huppe', 'Gepäck']
        self.signal_type_spinner = Spinner(text='Huppe', values=signal_types, size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.2, 'top': 0.3})
        self.layout.add_widget(self.signal_type_spinner)

        # Lade den Play-Button
        self.play_button2 = Button(background_normal='GUI/images/play.png', size_hint=(None, None), size=(150, 150), pos_hint={'center_x': 0.2, 'top': 0.2}, border=(0, 0, 0, 0))
        self.play_button2.bind(on_press=self.on_play_button_click2)
        self.layout.add_widget(self.play_button2)

        return self.layout

    def on_play_button_click2(self, instance):
        # Parameter lesen
        amplitude = self.amplitude_slider.value
        frequency = self.frequency_slider.value
        offset = self.offset_slider.value
        phase_shift = self.phase_shift_slider.value
        signal_type = self.signal_type_spinner.text
        duration=10
        sigTest=genSigPNG(signal_type, duration, amplitude, frequency, offset, phase_shift)
        if sigTest == 0:
            self.sigpicture = Image(source=r'C:\Users\Engelmann\OneDrive\Dokumente\arbeit\autopulse-analytics-linas-ai-powered-clustering-for-cars\test-1.png', size_hint=(None, None),  allow_stretch=True, size=(800, 800), pos_hint={'center_x': .69, 'top': 0.9})
            self.layout.add_widget(self.sigpicture)

        # Hier können Sie die Animation basierend auf den gelesenen Parametern durchführen
        print(f'Amplitude: {amplitude}, Frequenz: {frequency}, Offset: {offset}, Phasenverschiebung: {phase_shift}, Signaltyp: {signal_type}')
      

if __name__ == '__main__':
    SignalclassifierApp().run()

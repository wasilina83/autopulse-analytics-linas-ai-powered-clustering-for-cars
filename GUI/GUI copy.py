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

class SignalclassifierApp(App):
    def build(self):
        # Erstelle ein RelativeLayout als Hauptlayout
        self.layout = RelativeLayout()

        # Lade das Hintergrundbild
        self.background = Image(source='GUI/images/BG.png', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background)

        # Füge Slider für die Parameter hinzu
        self.amplitude_slider = Slider(min=0, max=100, value=50, step=1, orientation='vertical', size_hint=(None, None), size=(50, 200), pos_hint={'center_x': 0.1, 'top': 0.8})
        self.frequency_slider = Slider(min=0, max=100, value=50, step=1, orientation='vertical', size_hint=(None, None), size=(50, 200), pos_hint={'center_x': 0.2, 'top': 0.8})
        self.offset_slider = Slider(min=0, max=100, value=50, step=1, orientation='vertical', size_hint=(None, None), size=(50, 200), pos_hint={'center_x': 0.3, 'top': 0.8})
        self.phase_shift_slider = Slider(min=0, max=100, value=50, step=1, orientation='vertical', size_hint=(None, None), size=(50, 200), pos_hint={'center_x': 0.4, 'top': 0.8})
        self.layout.add_widget(self.amplitude_slider)
        self.layout.add_widget(self.frequency_slider)
        self.layout.add_widget(self.offset_slider)
        self.layout.add_widget(self.phase_shift_slider)

        # Füge Combobox für Signaltyp hinzu
        signal_types = ['Schuhe', 'Huppe', 'Gepäck']
        self.signal_type_spinner = Spinner(text='Huppe', values=signal_types, size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.6, 'top': 0.8})
        self.layout.add_widget(self.signal_type_spinner)

        # Lade den Play-Button
        self.play_button = Button(background_normal='GUI/images/play.png', size_hint=(None, None), size=(50, 50), pos_hint={'center_x': 0.8, 'top': 0.8}, border=(0, 0, 0, 0))
        self.play_button.bind(on_press=self.on_play_button_click)
        self.layout.add_widget(self.play_button)

        return self.layout

    def on_play_button_click(self, instance):
        # Parameter lesen
        amplitude = self.amplitude_slider.value
        frequency = self.frequency_slider.value
        offset = self.offset_slider.value
        phase_shift = self.phase_shift_slider.value
        signal_type = self.signal_type_spinner.text

        # Hier können Sie die Animation basierend auf den gelesenen Parametern durchführen
        print(f'Amplitude: {amplitude}, Frequenz: {frequency}, Offset: {offset}, Phasenverschiebung: {phase_shift}, Signaltyp: {signal_type}')

if __name__ == '__main__':
    SignalclassifierApp().run()

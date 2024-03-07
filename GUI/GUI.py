import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window

class SignalclassifierApp(App):
    def build(self):
        # Erstelle ein RelativeLayout als Hauptlayout
        layout = RelativeLayout()

        # Lade das Hintergrundbild
        background = Image(source='GUI/images/BG.png', allow_stretch=True, keep_ratio=False)

        # Füge das Bild zum Layout hinzu
        layout.add_widget(background)

        # Füge einen Text (Label) hinzu, der vor dem Bild liegt
        window_width, window_height = Window.size
        text_size = int(min(window_width, window_height * .1))
        text_pos_x = window_width * .5
        text_pos_y = window_height * .75
        text_label1 = Label(text='Willkommen zum', font_size=text_size, pos_hint={'center_x': text_pos_x / window_width -.2, 'top': text_pos_y / window_height+ .5})
        layout.add_widget(text_label1)
        text_label2 = Label(text='Signal-Classifier', font_size=text_size, pos_hint={'center_x': text_pos_x / window_width -.21, 'top':  (text_pos_y - text_size) / window_height +.5})
        layout.add_widget(text_label2)

        # Lade das Bild für das Logo (mit transparentem Hintergrund)
        logo_size = int(text_size * 10)  # 20% der kleineren Dimension
        logo_pos_x = window_width * 0.1
        logo_pos_y = window_height * 0.5  # 50% der Höhe
        logo = Image(source='GUI/images/Autowerkstatt_Logo_White-768x179.png', size_hint=(None, None), size=(logo_size, logo_size), pos_hint={'center_x': 2*(text_pos_x / window_width)-.3, 'top': text_pos_y / window_height+.25})
        layout.add_widget(logo)

        # Füge andere Widgets oder Elemente hinzu, falls benötigt
        text_label3 = Label(text='Analyse Starten', font_size=text_size*.5, pos_hint={'center_x': text_pos_x / window_width -.21, 'top':  (text_pos_y - text_size) / window_height+.2})
        layout.add_widget(text_label3)
        
         # Lade das Bild für den Play-Button
        play_button_size = int(min(window_width, window_height) * 0.4)  # 10% der kleineren Dimension
        play_button_pos_x = window_width * 0.9
        play_button = Button(background_normal='GUI/images/play.png', size_hint=(None, None), size=(play_button_size, play_button_size), pos_hint={'center_x': 2*(text_pos_x / window_width)-.3, 'top':  (text_pos_y - text_size) / window_height-.2})
        layout.add_widget(play_button)
        

        return layout

if __name__ == '__main__':
    SignalclassifierApp().run()

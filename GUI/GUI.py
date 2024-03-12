import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.animation import Animation

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
        logo_size = int(window_width*1.4)  # 20% der kleineren Dimension
        logo_pos_x = window_width * 0.1
        logo_pos_y = window_height * 0.5  # 50% der Höhe
        self.logo = Image(source='GUI/images/logo.png', size_hint=(None, None), size=(logo_size, logo_size), pos_hint={'center_x': 0.5, 'top': 1.3})
        self.layout.add_widget(self.logo)

        # Füge andere Widgets oder Elemente hinzu, falls benötigt
        self.text_label3 = Label(text='Analyse Starten', font_size=text_size*.5, pos_hint={'center_x': text_pos_x / window_width -.21, 'top':  (text_pos_y - text_size) / window_height+.2})
        self.layout.add_widget(self.text_label3)

        # Lade das Bild für den Play-Button
        play_button_size = int(min(window_width, window_height)*.5)  # 10% der kleineren Dimension
        play_button_pos_x = window_width * 0.9
        self.play_button = Button(background_normal='GUI/images/play.png', size_hint=(None, None), size=(play_button_size, play_button_size), pos_hint={'center_x': 2*(text_pos_x / window_width)-.3, 'top':  (text_pos_y - text_size) / window_height-.2}, border=(0, 0, 0, 0))
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
        logo_size = int(window_width*.3)
        self.new_background = Image(source='GUI/images/BGWeis.png', allow_stretch=True, keep_ratio=False, x=-Window.width, size_hint_x=0.5)
        self.layout.add_widget(self.new_background)
        self.logo = Image(source='GUI/images/logo.png', size_hint=(None, None), size=(logo_size, logo_size), pos_hint={'center_x': .8, 'top': 1.15})
        self.layout.add_widget(self.logo)

        # Animation für das neue Hintergrundbild
        new_animation = Animation(x=0, duration=1)
        new_animation.start(self.new_background)
        # Animation für das Hintergrundbild
        # animation = Animation(x=Window.width / 3, duration=1)
        # animation.start(self.background)
        print(f'Window width: {Window.width}, Window height: {Window.height}')
      

if __name__ == '__main__':
    SignalclassifierApp().run()

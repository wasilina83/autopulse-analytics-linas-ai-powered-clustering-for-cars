
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder


from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
# Laden der KV-Datei
Builder.load_file('KIVYG/widgets.kv')

class SignalclassifierLayout(BoxLayout):
    # Methoden und Attribute Ihrer Klasse
    
    def on_play_button_click2(self):
        # Hier können Sie Aktionen für den Button 'play_button2' ausführen
        pass

    def access_bg_image(self):
        bg_image = self.ids.BG
        # Hier können Sie auf das Image-Widget mit der ID 'BG' zugreifen und entsprechende Aktionen ausführen
    
# Erstellen Sie eine Instanz Ihrer Layoutklasse und fügen Sie sie Ihrer App hinzu
layout = SignalclassifierLayout()

# Fügen Sie das Widget zur App hinzu und führen Sie die App aus
# Hier ist ein einfaches Beispiel, wie Sie es zu einer App hinzufügen können:
from kivy.app import App

class MyApp(App):
    def build(self):
        return layout

if __name__ == '__main__':
    MyApp().run()

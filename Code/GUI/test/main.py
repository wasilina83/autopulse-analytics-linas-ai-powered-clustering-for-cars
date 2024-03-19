from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder

class SignalclassifierLayout(RelativeLayout):
    pass

class SignalclassifierApp(App):
    def build(self):
        return SignalclassifierLayout()

if __name__ == '__main__':
    SignalclassifierApp().run()

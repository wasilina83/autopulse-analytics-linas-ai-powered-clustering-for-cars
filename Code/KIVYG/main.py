from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics import Canvas
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.config import Config
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout






class MyScreenManager(ScreenManager):
    pass

class SignalclassifierLayout(RelativeLayout):
    
    pass

root_widget = Builder.load_string('''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

''')

class SIgnalgenApp(App):
    def build(self):
        self.title = 'AW 4.0 Signalgenerator'
        root_widget= SignalclassifierLayout(RelativeLayout)
        return root_widget

SIgnalgenApp().run() 
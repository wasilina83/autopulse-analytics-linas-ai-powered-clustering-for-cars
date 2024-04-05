from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics import Canvas
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.config import Config
from kivy.app import App


class StartScreen(Screen):

    def Mute_Audio(self):
        pass


    def new_g(self):
        pass




    def l_g(self):
        pass


    def Settings(self):
        pass  



class SelectionScreen(Screen):
    pass


class MyScreenManager(ScreenManager):
    pass


root_widget = Builder.load_string('''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
MyScreenManager:
    transition: FadeTransition()
    StartScreen:
    SelectionScreen:

<StartScreen>:
    name: 'start_screen'
    canvas:
        Rectangle:
            pos: self.pos
            size: self.size



    Button:
        id: b_1
        pos: 330,350
        size_hint:  0.2, 0.1
        text: 'button 1'
        font_size: 18
        on_press: root.new_g()
        on_release: app.root.current = 'selection_screen'


    Button:
        id: b_2
        pos: 330, 280
        size_hint:  0.2, 0.1
        text: 'button_2'
        font_size: 18


    Button:
        id: settings
        pos: 330, 210
        size_hint: 0.2, 0.1
        text: 'Settings'
        font_size: 18


    Button:
        id: mute_button
        pos:658, 495     
        size_hint: 0.2, 0.2







<SelectionScreen>:
    name: 'selection_screen'
    canvas:
        Rectangle:
            pos: self.pos

''')

class ExampleApp(App):
    def build(self):
        self.title = 'Save me Stack Overflow'
        return root_widget

ExampleApp().run() 
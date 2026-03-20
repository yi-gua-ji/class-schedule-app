# -*- coding: utf-8 -*-
import os
os.environ['KIVY_NO_ARGS'] = '1'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

print("Setting window size...")
Window.size = (400, 700)

class TestApp(App):
    def build(self):
        print("Building app...")
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text='Hello World', font_size=24, color=(0, 0, 0, 1)))
        box.add_widget(Label(text='Schedule App Test', font_size=16, color=(0.5, 0.5, 0.5, 1)))
        return box

if __name__ == '__main__':
    print("Starting test app...")
    TestApp().run()
    print("App finished")

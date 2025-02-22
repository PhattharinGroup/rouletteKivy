from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
import games.roulette.wheel as wheel

class SpinButton(Button):
    wheel = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'SPIN!'
        self.size_hint = (1, 0.2)
        self.background_color = (0, 1, 0, 1)
        self.bind(on_press=self.on_spin)
        
    def on_spin(self, instance):
        if self.wheel:
            self.wheel.spin()
        else:
            print("Error: Wheel not connected")
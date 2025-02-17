from kivy.app import App
import components.wheel as wheel
import components.spinButton as spinButton
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

class GameLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

class MyApp(App):
    def build(self):
        Window.size = (1280, 720)
        
        layout = GameLayout()
        
        self.wheel = wheel.PieWheel()
        layout.add_widget(self.wheel)
        
        self.spin_button = spinButton.SpinButton()
        self.spin_button.wheel = self.wheel
        layout.add_widget(self.spin_button)
        
        return layout

if __name__ == '__main__':
    MyApp().run()
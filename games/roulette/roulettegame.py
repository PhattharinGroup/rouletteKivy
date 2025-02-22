from kivy.uix.boxlayout import BoxLayout
import games.roulette.wheel as wheel
import games.roulette.spinButton as spinButton

class GameLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

    def setup(self):
        self.wheel = wheel.PieWheel()
        self.wheel.set_speed(10)  # Set the desired speed here
        self.add_widget(self.wheel)
        
        self.spin_button = spinButton.SpinButton()
        self.spin_button.wheel = self.wheel
        self.add_widget(self.spin_button)
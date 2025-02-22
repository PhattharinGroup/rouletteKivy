from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import games.roulette.wheel as wheel

class GameLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10
        
        # Create the wheel
        self.roulette_wheel = wheel.RouletteWheel()
        self.add_widget(self.roulette_wheel)
        
        # Create and add spin button
        self.spin_button = Button(
            text='SPIN!',
            size_hint=(1, 0.2),  # Full width, 20% height
            background_color=(0, 0.7, 0, 1)  # Green color
        )
        self.spin_button.bind(on_press=self.on_spin)
        self.add_widget(self.spin_button)
    
    def on_spin(self, instance):
        """Handle spin button press"""
        self.roulette_wheel.spin()

    def setup(self):
        pass

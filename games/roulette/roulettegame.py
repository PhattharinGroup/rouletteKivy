from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import games.roulette.wheel as wheel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock

class RouletteGameLayout(Screen):
    manager = ObjectProperty(None, allownone=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_called = False
        self.layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=10
        )
        
        self.roulette_wheel = wheel.RouletteWheel()
        self.layout.add_widget(self.roulette_wheel)
        
        buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.2),
            spacing=10
        )
        
        self.spin_button = Button(
            text='SPIN!',
            size_hint=(0.7, 1),
            background_color=(0, 0.7, 0, 1)
        )
        self.spin_button.bind(on_press=self.on_spin)
        
        exit_button = Button(
            text='EXIT',
            size_hint=(0.3, 1),
            background_color=(0.7, 0, 0, 1)
        )
        exit_button.bind(on_press=lambda x: self.exit_game())
        
        buttons_layout.add_widget(self.spin_button)
        buttons_layout.add_widget(exit_button)
        self.layout.add_widget(buttons_layout)
        
        self.add_widget(self.layout)

    def exit_game(self):
        if not self.manager:
            self.manager = self.parent
        
        if self.manager:
            self.manager.transition.direction = 'right'
            self.manager.current = 'menu'
        self.setup_called = False

    def on_enter(self):
        self.setup()

    def setup(self):
        if not self.setup_called:
            self.roulette_wheel.speed = 0
            self.roulette_wheel.result = None
            self.spin_button.disabled = False
            self.setup_called = True

    def on_spin(self, instance):
        self.spin_button.disabled = True
        self.roulette_wheel.spin()
        Clock.schedule_once(self.enable_spin_button, 5)  # Enable after 5 seconds

    def enable_spin_button(self, dt):
        self.spin_button.disabled = False



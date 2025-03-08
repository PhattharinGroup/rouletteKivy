from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

import games.roulette.wheel as wheel
from games.roulette.bettingTable import BettingTable

class RouletteGameLayout(Screen):
    manager = ObjectProperty(None, allownone=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_called = False
        self.bind(parent=self._on_parent)
        self._init_layout()
        self._init_background()
        self._init_roulette()
        self._init_buttons()

    def _on_parent(self, instance, value):
        if value and isinstance(value, ScreenManager):
            self.manager = value

    def _init_background(self):
        with self.canvas.before:
            Color(0.1, 0.3, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)
        
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _init_layout(self):
        self.layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(20),
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.layout)
        
    def _init_roulette(self):
        roulett_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.8),
            spacing=dp(0)
        )
        
        self.roulette_wheel = wheel.RouletteWheel(
            size_hint=(1.4, 1.2),
            pos_hint={'center_x': 0.3, 'center_y': 0.5}\
        )
        
        betting_container = BoxLayout(
            orientation='vertical',
            size_hint=(0.65, 1),
            padding=[dp(20), dp(10), dp(5), dp(10)]
        )
        self.betting_table = BettingTable(
            roulette_wheel=self.roulette_wheel,
            size_hint=(1, 1)
        )
        betting_container.add_widget(self.betting_table)
        roulett_container.add_widget(betting_container)
        
        wheel_container = BoxLayout(
            orientation='vertical',
            size_hint=(0.35, 1),
            padding=[dp(0), dp(2), dp(20), dp(2)]
        )
        wheel_container.add_widget(self.roulette_wheel)
        roulett_container.add_widget(wheel_container)
        
        self.layout.add_widget(roulett_container)
        
    def _init_buttons(self):
        buttons_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.2),
            spacing=dp(20),
            padding=[dp(20), 0, dp(20), dp(20)]  
        )
        self.spin_button = Button(
            text='SPIN!',
            size_hint=(1, 1),
            background_color=(0, 0, 0, 1),
            bold=True,
            font_size=dp(24)
        )
        self.spin_button.bind(on_press=self.on_spin)
        
        exit_button = Button(
            text='EXIT',
            size_hint=(1, 1),
            background_color=(0.7, 0, 0, 1),
            bold=True,
            font_size=dp(20)
        )
        exit_button.bind(on_press=lambda x: self.exit_game())
        
        buttons_layout.add_widget(self.spin_button)
        buttons_layout.add_widget(exit_button)
        self.layout.add_widget(buttons_layout)

    def _init_betting_table(self):
        self.betting_table = BettingTable()
        self.layout.add_widget(self.betting_table)

    def exit_game(self):
        if not self.manager:
            parent = self.parent
            while parent:
                if isinstance(parent, ScreenManager):
                    self.manager = parent
                    break
                parent = parent.parent
        
        if self.manager:
            self.manager.transition.direction = 'up'
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
        if self.betting_table.current_bet_button == None:
            self.spin_button.disabled = True
            self.spin_button.text = 'PLEASE PLACE A BET!'
            Clock.schedule_once(self.on_spin_complete, 2)
        else:
            self.spin_button.disabled = True
            self.roulette_wheel.spin()
            self.spin_button.text = 'SPINNING...'
            Clock.schedule_once(self.on_spin_complete, 5)

    def on_spin_complete(self, dt):
        self.spin_button.disabled = False
        self.spin_button.text = 'SPIN!'




from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.animation import Animation
from games.roulette.roulettegame import RouletteGameLayout as RouletteGame
from games.blackjack.blackjackgame import BlackjackGameLayout as BlackjackGame
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

class CustomRaisedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scale = 1
        self.original_bg_color = self.background_color 
        self.bind(size=self.update_rect, pos=self.update_rect)
        with self.canvas.before:
            Color(0.2, 0.6, 0.86, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_press(self):
        self.anim = Animation(scale=1.5, background_color=(1, 0.8, 0, 1), duration=0.5)
        self.anim.repeat = True
        self.anim.start(self)

    def on_release(self):
        self.anim = Animation(scale=1, background_color=(0.2, 0.6, 0.86, 1), duration=0.5)
        self.anim.repeat = False
        self.anim.start(self)

class MenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anim_button = Animation(scale=1.1, duration=0.5)
        self.anim_button.start(self.ids.roulette_button)  
        self.anim_button.start(self.ids.blackjack_button) 
        self.anim_button.start(self.ids.exit_button)  

class RouletteScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(
            orientation='vertical', 
            size_hint=(1, 1), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.game = RouletteGame()
        layout.add_widget(self.game)
        self.add_widget(layout)

class BlackjackScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.game = BlackjackGame()
        layout.add_widget(self.game)
        self.add_widget(layout)

class GameScreenManager(MDScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MenuScreen(name='menu'))
        self.add_widget(RouletteScreen(name='roulette'))
        self.add_widget(BlackjackScreen(name='blackjack'))

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"  
        self.theme_cls.accent_palette = "Orange" 
        Builder.load_file('main.kv')  # Ensure main.kv is loaded
        Window.size = (1200, 800) 
        Window.left = 300
        Window.top = 100
        return GameScreenManager()

    def on_start(self):
        self.anim_screen = Animation(opacity=1, duration=1)
        self.anim_screen.start(self.root)
        self.root.current = 'menu'

if __name__ == '__main__':
    MainApp().run()

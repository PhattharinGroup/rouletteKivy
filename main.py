from kivy.app import App
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from games.roulette.roulettegame import RouletteGameLayout as RouletteGame
from games.blackjack.blackjackgame import BlackjackGameLayout as BlackjackGame


class MenuScreen(MDScreen):
    # main menu screen
    pass

class RouletteScreen(MDScreen):
    # roulette game
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        self.game = RouletteGame()
        self.game.setup()
        layout.add_widget(self.game)
        self.add_widget(layout)

class BlackjackScreen(MDScreen):
    # blackjack game
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file('games/blackjack/blackjackscreen.kv')
        layout = MDBoxLayout(orientation='vertical')
        self.game = BlackjackGame()
        layout.add_widget(self.game)
        self.add_widget(layout)

class GameScreenManager(MDScreenManager):
    # transitions
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.add_widget(MenuScreen(name='menu'))
        self.add_widget(RouletteScreen(name='roulette'))
        self.add_widget(BlackjackScreen(name='blackjack'))

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"  # ตั้งธีมหลักเป็นสีฟ้า
        self.theme_cls.accent_palette = "Orange"  # ตั้งธีมเสริมเป็นสีส้ม
        Builder.load_file('main.kv')
        return GameScreenManager()

if __name__ == '__main__':
    MainApp().run()

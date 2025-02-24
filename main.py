from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from games.roulette.roulettegame import RouletteGameLayout as RouletteGame
from games.blackjack.blackjackgame import BlackjackGameLayout as BlackjackGame


class MenuScreen(Screen):
    # main menu screen
    pass

class RouletteScreen(Screen):
    # roulette game
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.game = RouletteGame()
        self.game.setup()
        layout.add_widget(self.game)
        self.add_widget(layout)

class BlackjackScreen(Screen):
    # blackjack game
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file('games/blackjack/blackjackscreen.kv')
        layout = BoxLayout(orientation='vertical')
        self.game = BlackjackGame()
        layout.add_widget(self.game)
        self.add_widget(layout)

class GameScreenManager(ScreenManager):
    # transitions
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        menu_screen = MenuScreen(name='menu')
        roulette_screen = RouletteScreen(name='roulette')
        roulette_screen.game.manager = self
        blackjack_screen = BlackjackScreen(name='blackjack')
        blackjack_screen.game.manager = self

        self.add_widget(menu_screen)
        self.add_widget(roulette_screen)
        self.add_widget(blackjack_screen)

class MainApp(App):
    def build(self):
        return GameScreenManager()

if __name__ == '__main__':
    MainApp().run()
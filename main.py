from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from games.roulette.roulettegame import RouletteGameLayout as RouletteGame
from games.blackjack.blackjackgame import BlackjackGameLayout as BlackjackGame

class MenuScreen(Screen):
    """Screen for the main menu."""
    pass

class RouletteScreen(Screen):
    """Screen for the Roulette game."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.game = RouletteGame()
        self.game.setup()
        layout.add_widget(self.game)
        self.add_widget(layout)

class BlackjackScreen(Screen):
    """Screen for the Blackjack game."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.game = BlackjackGame()
        layout.add_widget(self.game)
        self.add_widget(layout)

class GameScreenManager(ScreenManager):
    """Manages different game screens."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        menu_screen = MenuScreen(name='menu')
        roulette_screen = RouletteScreen(name='roulette')
        blackjack_screen = BlackjackScreen(name='blackjack')
        
        self.add_widget(menu_screen)
        self.add_widget(roulette_screen)
        self.add_widget(blackjack_screen)

class MainApp(App):
    """Main application class."""
    def build(self):
        return GameScreenManager()

if __name__ == '__main__':
    MainApp().run()
from kivy.app import App
from kivy.core.window import Window
from games.roulette.roulettegame import GameLayout

class MyApp(App):
    def build(self):
        Window.size = (1280, 720)
        
        layout = GameLayout()
        layout.setup()
        
        return layout

if __name__ == '__main__':
    MyApp().run()
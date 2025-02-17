from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from components.wheel import PieWheel  # Import PieWheel from wheel.py

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.wheel = PieWheel()
        
        button = Button(text="Spin", size_hint=(1, 0.2))
        button.bind(on_press=lambda x: self.wheel.spin())

        layout.add_widget(self.wheel)
        layout.add_widget(button)
        return layout

if __name__ == '__main__':
    MyApp().run()
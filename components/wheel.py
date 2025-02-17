import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rotate, Color, Line, PushMatrix, PopMatrix
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class Wheel(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.angle = 0
        self.segments = ["Apple", "Banana", "Cherry", "Grape", "Orange"]
        self.target_angle = 0
        self.speed = 0
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.draw_wheel()

    def draw_wheel(self):
        self.canvas.clear()
        with self.canvas:
            PushMatrix()
            self.rotation = Rotate(angle=self.angle, origin=self.center)
            Color(1, 0, 0, 1)
            self.line = Line(circle=(self.center_x, self.center_y, 100), width=3)
            PopMatrix()

    def update_canvas(self, *args):
        self.draw_wheel()

    def spin(self):
        self.target_angle = random.randint(360, 1080)  # Random spin range
        self.speed = 15
        Clock.schedule_interval(self.update_spin, 1 / 60)

    def update_spin(self, dt):
        if self.target_angle > 0:
            self.angle += self.speed
            self.target_angle -= self.speed
            self.speed = max(self.speed * 0.98, 0.5)  # Smooth deceleration
            self.rotation.angle = self.angle
            self.canvas.ask_update()
        else:
            Clock.unschedule(self.update_spin)
            self.determine_result()

    def determine_result(self):
        segment_size = 360 / len(self.segments)
        selected_index = int((self.angle % 360) / segment_size)
        print(f"Result: {self.segments[selected_index]}")

class RandomizerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.wheel = Wheel()
        button = Button(text="Spin", size_hint=(1, 0.2))
        button.bind(on_press=lambda x: self.wheel.spin())
        layout.add_widget(self.wheel)
        layout.add_widget(button)
        return layout

if __name__ == "__main__":
    RandomizerApp().run()
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rotate, Color, Ellipse, Line, Triangle, PushMatrix, PopMatrix
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class PieWheel(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.angle = 0
        self.segments = ["Red", "Yellow", "Orange", "Purple", "Green"]
        self.colors = [
            (1, 0, 0, 1),  # Red
            (1, 1, 0, 1),  # Yellow
            (1, 0.5, 0, 1),  # Orange
            (0.5, 0, 0.5, 1),  # Purple
            (0, 1, 0, 1)  # Green
        ]
        self.radius = 150
        self.target_angle = 0
        self.speed = 0

        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.draw_wheel()

    def draw_wheel(self):
        self.canvas.clear()
        with self.canvas:
            PushMatrix()
            self.rotation = Rotate(angle=self.angle, origin=self.center)

            for i, color in enumerate(self.colors):
                Color(*color)
                start_angle = (360 / len(self.segments)) * i
                Ellipse(pos=(self.center_x - self.radius, self.center_y - self.radius), 
                        size=(self.radius * 2, self.radius * 2), 
                        angle_start=start_angle, 
                        angle_end=start_angle + (360 / len(self.segments)))
                
            # Outline for the wheel
            Color(1, 1, 1, 1)
            Line(circle=(self.center_x, self.center_y, self.radius), width=3)

            PopMatrix()

            # Arrow (Pointer)
            Color(1, 1, 1, 1)  # White arrow
            Triangle(points=[
                self.center_x - 10, self.center_y + self.radius + 15,  # Left point
                self.center_x + 10, self.center_y + self.radius + 15,  # Right point
                self.center_x, self.center_y + self.radius  # Tip of arrow
            ])

    def update_canvas(self, *args):
        self.draw_wheel()

    def spin(self):
        self.target_angle = random.randint(360, 1080)
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
        self.wheel = PieWheel()
        button = Button(text="Spin", size_hint=(1, 0.2))
        button.bind(on_press=lambda x: self.wheel.spin())
        layout.add_widget(self.wheel)
        layout.add_widget(button)
        return layout

if __name__ == "__main__":
    RandomizerApp().run()
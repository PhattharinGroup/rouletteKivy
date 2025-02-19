import random
import math
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rotate, Color, Ellipse, Line, Triangle, PushMatrix, PopMatrix, Rectangle
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.text import Label as CoreLabel


class PieWheel(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.angle = 0
        # Standard roulette numbers in order
        self.numbers = [
            0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
            5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
        ]
        # Colors for each number (0 is green, others alternate between red and black)
        self.colors = []
        for num in self.numbers:
            if num == 0:
                self.colors.append((0, 0.5, 0, 1))  # Green for 0
            elif num in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
                self.colors.append((0.8, 0, 0, 1))  # Red
            else:
                self.colors.append((0.2, 0.2, 0.2, 1))  # Black
        
        self.target_angle = 0
        self.speed = 0
        self.result = None

        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.draw_wheel()

    def draw_wheel(self):
        self.canvas.clear()
        self.radius = min(self.width, self.height) / 2 - 20  # Adjust radius to fit within the window
        with self.canvas:
            PushMatrix()
            self.rotation = Rotate(angle=self.angle, origin=self.center)

            # Draw segments
            for i, (number, color) in enumerate(zip(self.numbers, self.colors)):
                segment_angle = 360 / len(self.numbers)
                start_angle = segment_angle * i

                # Draw segment
                Color(*color)
                Ellipse(pos=(self.center_x - self.radius, self.center_y - self.radius), 
                        size=(self.radius * 2, self.radius * 2), 
                        angle_start=start_angle, 
                        angle_end=start_angle + segment_angle)

                # Draw number text
                angle_rad = math.radians(start_angle + segment_angle / 2)
                text_x = self.center_x + (self.radius - 30) * 0.9 * math.cos(angle_rad)
                text_y = self.center_y + (self.radius - 30) * 0.9 * math.sin(angle_rad)
                label = CoreLabel(text=str(number), font_size=20)
                label.refresh()
                texture = label.texture
                Color(1, 1, 1, 1)  # White text
                self.canvas.add(Rectangle(texture=texture, pos=(text_x - texture.width / 2, text_y - texture.height / 2), size=texture.size))

            # Draw outer circle
            Color(0.8, 0.8, 0.8, 1)  # Silver
            Line(circle=(self.center_x, self.center_y, self.radius), width=3)

            PopMatrix()

            # Draw pointer
            Color(1, 0.8, 0, 1)  # Gold
            Triangle(points=[
                self.center_x - 10, self.center_y + self.radius + 15,  
                self.center_x + 10, self.center_y + self.radius + 15,
                self.center_x, self.center_y + self.radius
            ])

    def update_canvas(self, *args):
        self.draw_wheel()

    def spin(self):
        self.target_angle = random.randint(720, 1440)  # 2-4 full rotations
        self.speed = 20
        Clock.schedule_interval(self.update_spin, 1/60)

    def update_spin(self, dt):
        if self.target_angle > 0:
            rotation_amount = min(self.speed, self.target_angle)
            self.angle += rotation_amount
            self.target_angle -= rotation_amount
            self.speed = max(self.speed * 0.98, 0.5)
            self.rotation.angle = self.angle
            self.canvas.ask_update()
        else:
            Clock.unschedule(self.update_spin)
            self.determine_result()

    def determine_result(self):
        segment_size = 360 / len(self.numbers)
        # Calculate the final position considering multiple rotations
        final_angle = self.angle % 360
        selected_index = int(final_angle / segment_size)
        self.result = self.numbers[selected_index]
        print(f"Ball landed on: {self.result}")
        return self.result
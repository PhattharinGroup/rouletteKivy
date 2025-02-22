import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rotate, Color, Ellipse, Line, Triangle, PushMatrix, PopMatrix
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.popup import Popup

class PieWheel(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.angle = 0
        self.numbers = self._initialize_numbers()
        self.colors = self._initialize_colors()
        self.target_angle = 0
        self.speed = 0
        self.result = None
        self.default_speed = 15  # Default speed value
        self.acceleration = 0.5  # Acceleration factor
        self.friction = 0.98  # Friction factor

        # Bind the position and size changes to update the canvas
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.draw_wheel()

    def _initialize_numbers(self):
        """Initialize the numbers on the roulette wheel."""
        return [
            0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
            5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
        ]

    def _initialize_colors(self):
        """Initialize the colors for each number on the wheel."""
        colors = []
        for num in self.numbers:
            if num == 0:
                colors.append((0, 0.5, 0, 1))  # Green for 0
            elif num in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
                colors.append((0.8, 0, 0, 1))  # Red
            else:
                colors.append((0.2, 0.2, 0.2, 1))  # Black
        return colors

    def draw_wheel(self):
        """Draw the roulette wheel with segments and colors."""
        self.canvas.clear()
        self.radius = min(self.width, self.height) / 2 - 20
        with self.canvas:
            PushMatrix()
            self.rotation = Rotate(angle=self.angle, origin=self.center)

            for i, color in enumerate(self.colors):
                segment_angle = 360 / len(self.numbers)
                start_angle = segment_angle * i

                Color(*color)
                Ellipse(pos=(self.center_x - self.radius, self.center_y - self.radius), 
                        size=(self.radius * 2, self.radius * 2), 
                        angle_start=start_angle, 
                        angle_end=start_angle + segment_angle)

            Color(0.8, 0.8, 0.8, 1)
            Line(circle=(self.center_x, self.center_y, self.radius), width=3)

            PopMatrix()

            Color(1, 0.8, 0, 1)
            Triangle(points=[
                self.center_x - 10, self.center_y + self.radius + 15,  
                self.center_x + 10, self.center_y + self.radius + 15,
                self.center_x, self.center_y + self.radius
            ])

    def update_canvas(self, *args):
        """Update the canvas when the widget's size or position changes."""
        self.draw_wheel()

    def set_speed(self, speed):
        """Set the speed of the wheel spin."""
        self.default_speed = speed

    def spin(self):
        """Start spinning the wheel with acceleration and friction."""
        self.speed = 0  # Start from rest
        self.target_speed = self.default_speed
        self.accelerating = True
        Clock.schedule_interval(self.update_spin, 1/60)

    def update_spin(self, dt):
        """Update the wheel's spin, considering acceleration and friction."""
        if self.accelerating:
            # Accelerate until reaching target speed
            self.speed += self.acceleration
            if self.speed >= self.target_speed:
                self.accelerating = False
        else:
            # Apply friction to gradually slow down
            self.speed *= self.friction

        if self.speed > 0.1:  # Continue spinning until speed is very low
            self.angle += self.speed
            if self.angle >= 360:
                self.angle -= 360
            self.update_canvas()
        else:
            Clock.unschedule(self.update_spin)
            self.result = self.determine_result()
            self.show_result_popup()

    def show_result_popup(self):
        """Display a popup with the result of the spin."""
        popup = Popup(title='Spin Result',
                      content=Label(text=f'The ball landed on: {self.result}'),
                      size_hint=(0.6, 0.4))
        popup.open()
    def determine_result(self):
        """Determine the result based on the final angle of the wheel."""
        segment_size = 360 / len(self.numbers)
        final_angle = self.angle % 360
        selected_index = int(final_angle / segment_size)
        result = self.numbers[selected_index]
        print(f"Ball landed on: {result}")
        return result
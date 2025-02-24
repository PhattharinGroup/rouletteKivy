import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rotate, Color, Ellipse, Line, Triangle, PushMatrix, PopMatrix
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

class StatusDisplay(BoxLayout):
    """Handles the display of game status and results"""
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', size_hint=(1, 0.3))
        self.spin_status_label = Label(
            text='Status: Waiting to spin',
            size_hint=(1, 0.33),
            font_size='16sp'
        )
        self.number_label = Label(
            text='Number: ---',
            size_hint=(1, 0.33),
            font_size='16sp'
        )
        self.color_label = Label(
            text='Color: ---',
            size_hint=(1, 0.33),
            font_size='16sp'
        )
        
        self.add_widget(self.spin_status_label)
        self.add_widget(self.number_label)
        self.add_widget(self.color_label)

    def update_labels(self, number, color):
        self.number_label.text = f'Number: {number}'
        self.color_label.text = f'Color: {color}'
        
    def set_status(self, status):
        self.spin_status_label.text = f'Status: {status}'

class WheelDisplay(Widget):
    """Handles the visual representation of the wheel"""
    def __init__(self, numbers, colors, **kwargs):
        super().__init__(**kwargs)
        self.numbers = numbers
        self.colors = colors
        self.angle = random.randint(0, 359)
        self.radius = 0
        self.rotation = None
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def draw_wheel(self):
        self.canvas.clear()
        self.radius = min(self.width, self.height) / 2.5 - 10
        wheel_center_x = self.center_x
        wheel_center_y = self.center_y

        with self.canvas:
            PushMatrix()
            self.rotation = Rotate(angle=self.angle, origin=(wheel_center_x, wheel_center_y))
            self._draw_segments(wheel_center_x, wheel_center_y)
            self._draw_border(wheel_center_x, wheel_center_y)
            PopMatrix()
            self._draw_pointer(wheel_center_x, wheel_center_y)

    def _draw_segments(self, center_x, center_y):
        for i, color in enumerate(self.colors):
            segment_angle = 360 / len(self.numbers)
            start_angle = segment_angle * i
            Color(*color)
            Ellipse(
                pos=(center_x - self.radius, center_y - self.radius),
                size=(self.radius * 2, self.radius * 2),
                angle_start=start_angle,
                angle_end=start_angle + segment_angle
            )

    def _draw_border(self, center_x, center_y):
        Color(0.8, 0.8, 0.8, 1)
        Line(circle=(center_x, center_y, self.radius), width=3)

    def _draw_pointer(self, center_x, center_y):
        Color(1, 0.8, 0, 1)
        Triangle(points=[
            center_x - 10, center_y + self.radius + 15,
            center_x + 10, center_y + self.radius + 15,
            center_x, center_y + self.radius
        ])

    def update_canvas(self, *args):
        self.draw_wheel()

    def set_angle(self, angle):
        self.angle = angle
        self.draw_wheel()

class RouletteWheel(BoxLayout):
    """Main class that coordinates the wheel game"""
    def __init__(self, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.numbers = self._initialize_numbers()
        self.colors = self._initialize_colors()
        self.speed = 0
        self.default_speed = 15
        self.friction = 0.98
        self.color_text = "None"
        self.result = None
        
        left_container = Widget(size_hint=(0.5, 1))
        right_container = BoxLayout(orientation='vertical', size_hint=(0.5, 1))
        
        self.wheel_display = WheelDisplay(
            self.numbers, 
            self.colors, 
            size_hint=(1, 0.7)
        )
        self.status_display = StatusDisplay()
        
        right_container.add_widget(self.wheel_display)
        right_container.add_widget(self.status_display)
        
        self.add_widget(left_container)
        self.add_widget(right_container)

    def _initialize_numbers(self):
        """Initialize the numbers on the roulette wheel."""
        return [
        0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1,
        00, 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2
        ]

    def _initialize_colors(self):
        """Initialize the colors for each number on the wheel."""
        colors = []
        for num in self.numbers:
            if num in [0, 00]:
                colors.append((0, 0.5, 0, 1))  # Green
            elif num in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
                colors.append((0.8, 0, 0, 1))  # Red
            else:
                colors.append((0.2, 0.2, 0.2, 1))  # Black
        return colors

    def spin(self):
        self.speed = self.default_speed
        self.target_speed = self.default_speed
        self.accelerating = True
        #log the status
        self.status_display.set_status('Spinning')
        print("\n---------Result---------")
        print(self.status_display.spin_status_label.text)
        Clock.schedule_interval(self.update_spin, 1/60)

    def update_spin(self, dt):
        if self.speed > 0.1:
            self.speed *= self.friction
            self.wheel_display.set_angle(self.wheel_display.angle + self.speed)
            self.update_status_label()
            return True
        else:
            self.status_display.set_status('Finished')
            self.determine_result()
            self.update_status_label()
            return False

    def start_spin(self):
        #When press restart spin
        self.spin()

    def update_status_label(self):
        segment_size = 360 / len(self.numbers)
        current_index = int((self.wheel_display.angle % 360) / segment_size)
        current_number = self.numbers[current_index]
        
        if current_number in [0, 00]:
            self.color_text = "Green"
        elif current_number in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
            self.color_text = "Red"
        else:
            self.color_text = "Black"
        
        # Update individual labels
        self.status_display.update_labels(current_number, self.color_text)

    def determine_result(self):
        """Determine the result based on the final angle of the wheel."""
        segment_size = 360 / len(self.numbers)
        final_angle = self.wheel_display.angle % 360
        selected_index = int(final_angle / segment_size)
        self.result = self.numbers[selected_index]
        #log the result
        print(f"Number: {self.result}")
        print(f"Color: {self.color_text}")
        print(self.status_display.spin_status_label.text)
        print("-------End Result-------")
        return self.result
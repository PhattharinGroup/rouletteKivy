import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rotate, Color, Ellipse, Line, Triangle, PushMatrix, PopMatrix
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty

class StatusDisplay(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', size_hint=(1, 0.3))
        # Add bet and result labels
        self.spin_status_label = Label(
            text='Status: Waiting to spin',
            size_hint=(1, 0.2),
            font_size='16sp'
        )
        self.bet_label = Label(
            text='Current Bet: None',
            size_hint=(1, 0.2),
            font_size='16sp'
        )
        self.result_label = Label(
            text='Result: ---',
            size_hint=(1, 0.2),
            font_size='16sp',
            color=(1, 0.8, 0, 1)  # Gold color
        )
        self.number_label = Label(
            text='Number: ---',
            size_hint=(1, 0.2),
            font_size='16sp'
        )
        self.color_label = Label(
            text='Color: ---',
            size_hint=(1, 0.2),
            font_size='16sp'
        )
        
        # Add all labels to display
        self.add_widget(self.spin_status_label)
        self.add_widget(self.bet_label)
        self.add_widget(self.result_label)
        self.add_widget(self.number_label)
        self.add_widget(self.color_label)

    def update_bet(self, bet_type, amount):
        """Update the current bet display"""
        self.bet_label.text = f'Current Bet: {bet_type} (${amount})'
        
    def update_result(self, won, amount):
        """Update the result display"""
        if won:
            self.result_label.text = f'Won: ${amount}'
            self.result_label.color = (0, 1, 0, 1)  # Green for win
        else:
            self.result_label.text = f'Lost: ${amount}'
            self.result_label.color = (1, 0, 0, 1)  # Red for loss

    def update_labels(self, number, color):
        self.number_label.text = f'Number: {number}'
        self.color_label.text = f'Color: {color}'
        
    def set_status(self, status):
        self.spin_status_label.text = f'Status: {status}'

class WheelDisplay(Widget):
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
    on_spin_complete = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.register_event_type('on_spin_complete')
        self._init_properties()
        self._setup_layout()
        self.current_bet = None
        self.bet_amount = 0

    def set_bet(self, bet_type, amount):
        self.current_bet = bet_type
        self.bet_amount = amount
        self.status_display.update_bet(bet_type, amount)

    def _check_win(self, result):
        """Check if the bet won based on the result"""
        print(f"\nChecking win condition for bet: {self.current_bet}, result: {result}")

        if not self.current_bet:
            return False

        try:
            result_str = str(result)
            if result_str == '00':
                return self.current_bet == '00'
            if result_str == '0':
                return self.current_bet == '0'

            result_num = int(result_str)
            print(f"Converted result number: {result_num}")

            bet_conditions = {
                'RED': lambda x: x in {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36},
                'BLACK': lambda x: x in {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35},
                'EVEN': lambda x: x % 2 == 0,
                'ODD': lambda x: x % 2 == 1,
                '1st 12': lambda x: 1 <= x <= 12,
                '2nd 12': lambda x: 13 <= x <= 24,
                '3rd 12': lambda x: 25 <= x <= 36,
                '1-18': lambda x: 1 <= x <= 18,
                '19-36': lambda x: 19 <= x <= 36,
            }

            if isinstance(self.current_bet, (int, str)) and str(self.current_bet) == result_str:
                return True

            return bet_conditions.get(self.current_bet, lambda x: False)(result_num)

        except Exception as e:
            print(f"Error checking win: {e}")
            return False

    def _init_properties(self):
        self.numbers = self._initialize_numbers()
        self.colors = self._initialize_colors()
        self.speed = 0
        self.default_speed = 15 + random.randint(5, 10) / random.randint(5, 10)
        self.friction = 0.98
        self.color_text = "None"
        self.result = None

    def _setup_layout(self):
        left_container = Widget(size_hint=(0.4, 1))
        
        right_container = BoxLayout(
            orientation='vertical',
            size_hint=(0.6, 1),
            spacing='10dp',
            padding='10dp'
        )
        
        self.wheel_display = WheelDisplay(
            self.numbers, 
            self.colors, 
            size_hint=(1, 0.75)
        )
        
        self.status_display = StatusDisplay(size_hint=(1, 0.25))
        
        right_container.add_widget(self.wheel_display)
        right_container.add_widget(self.status_display)
        
        self.add_widget(left_container)
        self.add_widget(right_container)

    def _initialize_numbers(self):
        return [
        0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1,
        00, 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2
        ]

    def _initialize_colors(self):
        colors = []
        for num in self.numbers:
            if num in [0, 00]:
                colors.append((0, 0.5, 0, 1))
            elif num in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
                colors.append((0.8, 0, 0, 1))
            else:
                colors.append((0.2, 0.2, 0.2, 1))
        return colors

    def spin(self):
        self.speed = self.default_speed
        self.status_display.set_status('Spinning')
        print("\n---------Result---------")
        Clock.schedule_interval(self.update_spin, 1/45)

    def update_spin(self, dt):
        if self.speed > 0.1:
            self.speed *= self.friction
            self.wheel_display.set_angle(self.wheel_display.angle + self.speed)
            self.update_status_label()
            return True
        else:
            self._handle_spin_end()
            return False

    def _handle_spin_end(self):
        self.status_display.set_status('Finished')
        result = self.determine_result()
        self.update_status_label()
        
        if self.current_bet is not None:
            won = self._check_win(result)
            winnings = self.bet_amount * 2 if won else self.bet_amount
            self.status_display.update_result(won, winnings)
            print(f"\nBet: {self.current_bet} (${self.bet_amount})")
            print(f"{'Won' if won else 'Lost'}: ${winnings}")
        
        self.current_bet = None
        self.bet_amount = 0
        self.status_display.update_bet('None', 0)
        print("Bet reset for next spin")
        print("-------End Result-------")
        
        self.dispatch('on_spin_complete')
        return result

    def start_spin(self):
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
        
        self.status_display.update_labels(current_number, self.color_text)

    def determine_result(self):
        segment_size = 360 / len(self.numbers)
        final_angle = self.wheel_display.angle % 360
        selected_index = int(final_angle / segment_size)
        self.result = self.numbers[selected_index]
        print(f"Number: {self.result}")
        print(f"Color: {self.color_text}")
        print(self.status_display.spin_status_label.text)
        return self.result

    def on_spin_complete(self, *args):
        pass
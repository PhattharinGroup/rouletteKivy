from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Line

class BettingTable(BoxLayout):
    def __init__(self, roulette_wheel=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.roulette_wheel = roulette_wheel
        self.current_bet_button = None
        self.numbers = [
            [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
            [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
            [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
        ]
        self.special_bets = {
            '1st 12': range(1, 13),
            '2nd 12': range(13, 25),
            '3rd 12': range(25, 37),
            '1-18': range(1, 19),
            'EVEN': [n for n in range(1, 37) if n % 2 == 0],
            'RED': [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
            'BLACK': [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35],
            'ODD': [n for n in range(1, 37) if n % 2 == 1],
            '19-36': range(19, 37)
        }
        self._init_table()
        if roulette_wheel:
            roulette_wheel.bind(on_spin_complete=self._on_spin_complete)

    def _init_table(self):
        self.layout = BoxLayout(orientation='vertical')
        
        zero_layout = GridLayout(cols=2, size_hint=(1, 0.1))
        zero_layout.add_widget(self._create_number_button('0', background_color=(0, 0.5, 0, 1)))
        zero_layout.add_widget(self._create_number_button('00', background_color=(0, 0.5, 0, 1)))
        self.layout.add_widget(zero_layout)
        
        numbers_layout = GridLayout(cols=12, rows=3, size_hint=(1, 0.6))
        for row in self.numbers:
            for num in row:
                color = (0.8, 0, 0, 1) if num in self.special_bets['RED'] else (0, 0, 0, 1)
                numbers_layout.add_widget(self._create_number_button(str(num), background_color=color))
        self.layout.add_widget(numbers_layout)
        
        bottom_layout = GridLayout(cols=3, rows=1, size_hint=(1, 0.3))
        bottom_layout.add_widget(self._create_bet_button('1st 12'))
        bottom_layout.add_widget(self._create_bet_button('2nd 12'))
        bottom_layout.add_widget(self._create_bet_button('3rd 12'))

        special_layout = GridLayout(cols=6, rows=1, size_hint=(1, 0.3))
        special_layout.add_widget(self._create_bet_button('ODD'))
        special_layout.add_widget(self._create_bet_button('EVEN'))
        special_layout.add_widget(self._create_bet_button('RED'))
        special_layout.add_widget(self._create_bet_button('BLACK'))
        special_layout.add_widget(self._create_bet_button('1-18'))
        special_layout.add_widget(self._create_bet_button('19-36'))
        
        self.layout.add_widget(bottom_layout)
        self.layout.add_widget(special_layout)
        
        self.add_widget(self.layout)

    def _create_number_button(self, text, background_color=(0, 0, 0, 1)):
        btn = Button(
            text=text,
            background_color=background_color,
            color=(1, 1, 1, 1),
            bold=True,
            font_size=dp(20)
        )
        btn.bind(on_press=self.on_number_press)
        return btn

    def _create_bet_button(self, text):
        if text == 'RED':
            bg_color = (0.8, 0, 0, 1)
        elif text == 'BLACK':
            bg_color = (0, 0, 0, 1)
        elif text in ['0', '00']:
            bg_color = (0, 0.5, 0, 1)
        else:
            bg_color = (0.1, 0.1, 0.1, 1)

        btn = Button(
            text=text,
            background_color=bg_color,
            color=(1, 1, 1, 1),
            bold=True,
            font_size=dp(16)
        )
        btn.bind(on_press=self.on_special_bet_press)
        return btn

    def _reset_buttons(self):
        if self.current_bet_button:
            text = self.current_bet_button.text
            if text == 'RED':
                original_color = (0.8, 0, 0, 1)
            elif text == 'BLACK':
                original_color = (0, 0, 0, 1)
            elif text in ['0', '00']:
                original_color = (0, 0.5, 0, 1)
            elif text.isdigit():
                num = int(text)
                if num in self.special_bets['RED']:
                    original_color = (0.8, 0, 0, 1)
                else:
                    original_color = (0, 0, 0, 1)
            else:
                original_color = (0.1, 0.1, 0.1, 1)

            self.current_bet_button.background_color = original_color

    def on_number_press(self, instance):
        try:
            bet_type = instance.text
            bet_amount = 100

            if self.current_bet_button == instance:
                self._reset_buttons()
                self.current_bet_button = None
                
                if self.roulette_wheel:
                    self.roulette_wheel.set_bet(None, 0)
                return
            
            self._reset_buttons()
            
            instance.background_color = (0.5, 0.5, 0.5, 1)
            self.current_bet_button = instance

            if bet_type == '00':
                bet_value = bet_type
            else:
                bet_value = int(bet_type)
            
            if self.roulette_wheel:
                self.roulette_wheel.set_bet(bet_value, bet_amount)
        except Exception as e:
            print(f"Error handling bet: {e}")

    def on_special_bet_press(self, instance):
        try:
            bet_type = instance.text
            bet_amount = 100

            if self.current_bet_button == instance:
                self._reset_buttons()
                self.current_bet_button = None
                
                if self.roulette_wheel:
                    self.roulette_wheel.set_bet(None, 0)
                return

            self._reset_buttons()
            
            instance.background_color = (0.5, 0.5, 0.5, 1)
            self.current_bet_button = instance
            
            if self.roulette_wheel:
                self.roulette_wheel.set_bet(bet_type, bet_amount)
        except Exception as e:
            print(f"Error handling bet: {e}")

    def _on_spin_complete(self, *args):
        if self.current_bet_button:
            text = self.current_bet_button.text
            if text == 'RED':
                original_color = (0.8, 0, 0, 1)
            elif text == 'BLACK':
                original_color = (0, 0, 0, 1)
            elif text in ['0', '00']:
                original_color = (0, 0.5, 0, 1)
            elif text.isdigit():
                num = int(text)
                if num in self.special_bets['RED']:
                    original_color = (0.8, 0, 0, 1)
                else:
                    original_color = (0, 0, 0, 1)
            else:
                original_color = (0.1, 0.1, 0.1, 1)
            
            self.current_bet_button.background_color = original_color
            self.current_bet_button = None
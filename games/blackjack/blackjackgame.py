import os
import random
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.graphics import Color, Rectangle


class BlackjackGame:

    def __init__(self):
        self.deck = self.create_deck()
        self.money = 100000
        self.bet = 5000
        self.player_hand = []
        self.dealer_hand = []

    def create_deck(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        deck = [{'suit': suit, 'rank': rank, 'image': f"assets/PlayingCards/{rank}_of_{suit}.png"} for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def deal_cards(self):
        """ แจกไพ่ให้ผู้เล่นและเจ้ามือ """
        if len(self.deck) < 4:
            self.deck = self.create_deck()
        
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

    def hit(self):
        """ ผู้เล่นขอไพ่เพิ่ม """
        if self.deck:
            self.player_hand.append(self.deck.pop())

    def dealer_play(self):
        """ ให้เจ้ามือเล่นไพ่ตามกติกา """
        while self.calculate_score(self.dealer_hand) < 17:
            if self.deck:
                self.dealer_hand.append(self.deck.pop())

    def calculate_score(self, hand):
        """ คำนวณแต้มของผู้เล่นหรือเจ้ามือ """
        score = 0
        ace_count = sum(1 for card in hand if card['rank'] == 'ace')
        for card in hand:
            if card['rank'] in ['jack', 'queen', 'king']:
                score += 10
            elif card['rank'] == 'ace':
                score += 11
            else:
                score += int(card['rank'])
        
        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1

        return score

    def check_winner(self):
        """ ตรวจสอบผลลัพธ์ของเกม """
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)

        if player_score > 21:
            return "Dealer wins!", "red", -self.bet
        elif dealer_score > 21 or player_score > dealer_score:
            return "You win!", "green", self.bet
        elif player_score < dealer_score:
            return "Dealer wins!", "red", -self.bet
        else:
            return "It's a tie!", "yellow", 0


class BlackjackGameUI(MDBoxLayout):
    """ คลาสนี้จัดการ UI และการโต้ตอบของผู้ใช้ """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_logic = BlackjackGame()  
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(20)
        self.size_hint = (1, 1)
        
        with self.canvas.before:
            Color(0, 0, 0, 1)  # Set the background color to black
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.setup_ui()
        self.setup_game()

        Window.bind(on_resize=self.resize_window)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def setup_ui(self):
        """ ตั้งค่า UI เริ่มต้น """

        self.money_label = MDLabel(
            font_style="H6", 
            halign="center", 
            theme_text_color="Custom", 
            text_color=(1, 1, 1, 1)
        )
        self.bet_label = MDLabel(
            font_style="H6", 
            halign="center", 
            theme_text_color="Custom", 
            text_color=(1, 1, 1, 1)
        )

        self.money_bet_box = MDBoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height=dp(40), 
            spacing=dp(10)
        )
        self.money_bet_box.add_widget(self.money_label)
        self.money_bet_box.add_widget(self.bet_label)
        self.add_widget(self.money_bet_box)

        self.info_label = MDLabel(
            font_style="H4", 
            halign="center", 
            size_hint_y=None, 
            height=dp(50), 
            text="Welcome to Blackjack!", 
            theme_text_color="Custom", 
            text_color=(1, 1, 1, 1)
        )
        self.add_widget(self.info_label)

        self.dealer_cards = MDBoxLayout(
            orientation='horizontal', 
            size_hint_x=None, 
            width=dp(400), 
            height=dp(120), 
            spacing=dp(10), 
            pos_hint={"center_x": 0.5}
        )
        self.player_cards = MDBoxLayout(
            orientation='horizontal', 
            size_hint_x=None, 
            width=dp(400), 
            height=dp(120), 
            spacing=dp(10), 
            pos_hint={"center_x": 0.5}
        )

        self.add_widget(self.dealer_cards)
        self.add_widget(self.player_cards)

        self.control_buttons_box = MDBoxLayout(
            orientation='horizontal', 
            spacing=dp(20), 
            size_hint_y=None, 
            height=dp(60)
        )
        self.deal_button = MDRaisedButton(text='Deal', on_press=self.deal)
        self.hit_button = MDRaisedButton(text='Hit', on_press=self.hit)
        self.stand_button = MDRaisedButton(text='Stand', on_press=self.stand)
        self.back_to_menu_button = MDRaisedButton(text='Back to Menu', on_press=self.back_to_menu)

        self.control_buttons_box.add_widget(self.deal_button)
        self.control_buttons_box.add_widget(self.hit_button)
        self.control_buttons_box.add_widget(self.stand_button)
        self.control_buttons_box.add_widget(self.back_to_menu_button)
        self.add_widget(self.control_buttons_box)

    def setup_game(self):
        """ รีเซ็ตเกมใหม่ """
        self.game_logic = BlackjackGame()  # Use BlackjackGame instead of BlackjackGameLogic
        self.update_money_display()
        self.clear_cards()
        self.info_label.text = "Welcome to Blackjack!"

    def update_money_display(self):
        """ อัปเดตเงินและเดิมพัน """
        self.money_label.text = f"Money: ${self.game_logic.money}"
        self.bet_label.text = f"Bet: ${self.game_logic.bet}"

    def deal(self, instance):
        """ แจกไพ่ให้ผู้เล่นและเจ้ามือ """
        self.game_logic.deal_cards()
        self.update_cards()
        self.info_label.text = "Game Started!"

    def hit(self, instance):
        """ ผู้เล่นขอไพ่เพิ่ม """
        self.game_logic.hit()
        self.update_cards()
        if self.game_logic.calculate_score(self.game_logic.player_hand) > 21:
            self.check_winner()

    def stand(self, instance):
        """ ผู้เล่นหยุดและให้เจ้ามือเล่น """
        self.game_logic.dealer_play()
        self.update_cards()
        self.check_winner()

    def check_winner(self):
        """ ตรวจสอบผลลัพธ์ของเกม """
        result, color, money_change = self.game_logic.check_winner()
        self.info_label.text = f"[color={color}]{result}[/color]"
        self.game_logic.money += money_change
        self.update_money_display()

    def update_cards(self):
        """ แสดงไพ่ที่ผู้เล่นและเจ้ามือมี """
        self.clear_cards()
        for card in self.game_logic.player_hand:
            self.player_cards.add_widget(self.create_card(card))
        for card in self.game_logic.dealer_hand:
            self.dealer_cards.add_widget(self.create_card(card))

    def create_card(self, card):
        return AsyncImage(source=card['image'], allow_stretch=True, keep_ratio=True)

    def clear_cards(self):
        self.player_cards.clear_widgets()
        self.dealer_cards.clear_widgets()

    def back_to_menu(self, instance):
        app = MDApp.get_running_app()
        app.root.current = 'menu'

    def resize_window(self, instance, width, height):
        self.size = (width, height)


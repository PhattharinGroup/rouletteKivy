from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, Rectangle
import random
import os

class BlackjackGameLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup()  # เรียกใช้เมธอด setup เพื่อเริ่มต้นเกม

    def on_kv_post(self, base_widget):
        # เก็บการอ้างอิงถึงวิดเจ็ตต่าง ๆ หลังจากที่ KV โหลดเสร็จ
        self.info_label = self.ids.info_label
        self.click_to_continue = self.ids.click_to_continue
        self.player_cards = self.ids.player_cards
        self.dealer_cards = self.ids.dealer_cards

    def create_deck(self):
        # สร้างสำรับไพ่ 52 ใบ
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        deck = []
        for suit in suits:
            for rank in ranks:
                image_name = f"{rank}_of_{suit}.png"
                image_path = os.path.join('assets', 'CartPNG', image_name)
                card = {'suit': suit.title(), 'rank': rank.title(), 'image': image_path}
                deck.append(card)
        random.shuffle(deck)
        return deck

    def setup(self):
        # รีเซ็ตสถานะเกม
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.game_started = False
        if hasattr(self, 'info_label'):
            self.info_label.text = "Welcome to Blackjack!"
        if hasattr(self, 'click_to_continue'):
            self.click_to_continue.opacity = 1
        if hasattr(self, 'player_cards'):
            self.player_cards.clear_widgets()
        if hasattr(self, 'dealer_cards'):
            self.dealer_cards.clear_widgets()

    def deal(self, instance):
        if not self.game_started:
            self.game_started = True
            self.info_label.text = ""
            self.click_to_continue.opacity = 0
            # ตรวจสอบว่าเด็คมีไพ่อย่างน้อย 4 ใบ ถ้าไม่พอ ให้รีเซ็ตเด็ค
            if len(self.deck) < 4:
                self.deck = self.create_deck()
            self.player_hand = [self.deck.pop(), self.deck.pop()]
            self.dealer_hand = [self.deck.pop(), self.deck.pop()]
            self.update_cards()

    def hit(self, instance):
        if self.game_started:
            if not self.deck:
                # ถ้าไพ่หมด ให้รีเซ็ตเด็ค
                self.deck = self.create_deck()
            self.player_hand.append(self.deck.pop())
            self.update_cards()
            if self.calculate_score(self.player_hand) > 21:
                self.check_winner()

    def stand(self, instance):
        if self.game_started:
            while self.calculate_score(self.dealer_hand) < 17:
                if not self.deck:
                    # ถ้าไพ่หมด ให้รีเซ็ตเด็ค
                    self.deck = self.create_deck()
                self.dealer_hand.append(self.deck.pop())
            self.update_cards(reveal_dealer=True)
            self.check_winner()

    def calculate_score(self, hand):
        # คำนวณคะแนนของมือ (player หรือ dealer)
        score = 0
        ace_count = 0
        for card in hand:
            rank = card['rank']
            if rank in ['Jack', 'Queen', 'King']:
                score += 10
            elif rank == 'Ace':
                ace_count += 1
                score += 11
            else:
                score += int(rank)
        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1
        return score

    def update_cards(self, reveal_dealer=False):
        # อัปเดตการแสดงผลไพ่บนหน้าจอ
        self.player_cards.clear_widgets()
        self.dealer_cards.clear_widgets()

        for card in self.player_hand:
            self.player_cards.add_widget(self.create_card(card))

        for idx, card in enumerate(self.dealer_hand):
            if idx == 0 or reveal_dealer:
                self.dealer_cards.add_widget(self.create_card(card))
            else:
                back_card = {'rank': '?', 'suit': '', 'image': 'assets/CartPNG/red_joker.png'}
                self.dealer_cards.add_widget(self.create_card(back_card))

    def create_card(self, card):
        # สร้างวิดเจ็ตการ์ดพร้อมรูปภาพ
        card_widget = MDBoxLayout(size_hint=(None, None), size=("80dp", "120dp"))
        image = card['image']
        card_image = AsyncImage(source=image, allow_stretch=True, keep_ratio=True)
        card_widget.add_widget(card_image)
        return card_widget

    def check_winner(self):
        # ตรวจสอบผู้ชนะและอัปเดตข้อความ
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        self.update_cards(reveal_dealer=True)
        if player_score > 21:
            self.info_label.text = "[color=#ff0000]You busted! Dealer wins.[/color]"
        elif dealer_score > 21 or player_score > dealer_score:
            self.info_label.text = "[color=#00ff00]You win![/color]"
        elif player_score < dealer_score:
            self.info_label.text = "[color=#ff0000]Dealer wins.[/color]"
        else:
            self.info_label.text = "[color=#ffff00]It's a tie![/color]"
        self.game_started = False

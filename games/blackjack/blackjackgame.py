from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
import random

class BlackjackGameLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

    def on_kv_post(self, base_widget):
        self.info_label = self.ids.info_label
        self.player_cards = self.ids.player_cards
        self.dealer_cards = self.ids.dealer_cards

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def setup(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

    def deal(self, instance):
        if not self.deck:
            self.setup()
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.update_cards()

    def hit(self, instance):
        if not self.deck:
            self.setup()
        self.player_hand.append(self.deck.pop())
        self.update_cards()
        if self.calculate_score(self.player_hand) > 21:
            self.check_winner()

    def stand(self, instance):
        while self.calculate_score(self.dealer_hand) < 17:
            if not self.deck:
                self.setup()
            self.dealer_hand.append(self.deck.pop())
        self.update_cards()
        self.check_winner()

    def calculate_score(self, hand):
        score = 0
        ace_count = 0
        for card in hand:
            rank = card['rank']
            if rank in ['J', 'Q', 'K']:
                score += 10
            elif rank == 'A':
                ace_count += 1
                score += 11
            else:
                score += int(rank)
        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1
        return score

    def update_cards(self):
        self.player_cards.clear_widgets()
        self.dealer_cards.clear_widgets()

        for card in self.player_hand:
            self.player_cards.add_widget(self.create_card(card))
            
        self.dealer_cards.add_widget(self.create_card(self.dealer_hand[0]))
        self.dealer_cards.add_widget(self.create_card({'rank': '?', 'suit': ''}))  # ซ่อนใบที่สอง

    def create_card(self, card):
        card_widget = MDCard(
            size_hint=(None, None),
            size=("80dp", "120dp"),
            padding="8dp",
            radius=[8, 8, 8, 8],
            md_bg_color=(1, 1, 1, 1) if card['rank'] != '?' else (0.5, 0.5, 0.5, 1),
            elevation=8
        )
        card_widget.add_widget(MDLabel(
            text=f"{card['rank']} {card['suit']}" if card['rank'] != '?' else "?",
            font_style="H6",
            halign="center",
            theme_text_color="Primary"
        ))
        return card_widget

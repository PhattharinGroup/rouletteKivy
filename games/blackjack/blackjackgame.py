from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import random

class GameLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

        self.info_label = Label(text='Welcome to Blackjack!')
        self.add_widget(self.info_label)

        self.start_button = Button(text='Start Game', on_press=self.start_game)
        self.add_widget(self.start_button)

    def create_deck(self):
        """Create a standard deck of cards."""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def start_game(self, instance):
        """Start a new game of Blackjack."""
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.update_info()

    def update_info(self):
        """Update the game information displayed to the player."""
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        self.info_label.text = (
            f"Player's Hand: {self.hand_to_string(self.player_hand)} (Score: {player_score})\n"
            f"Dealer's Hand: {self.hand_to_string(self.dealer_hand)} (Score: {dealer_score})"
        )

    def calculate_score(self, hand):
        """Calculate the score of a hand."""
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

    def hand_to_string(self, hand):
        """Convert a hand to a string representation."""
        return ', '.join([f'{card["rank"]} of {card["suit"]}' for card in hand])

    def hit(self, instance):
        """Handle the player hitting (drawing a card)."""
        self.player_hand.append(self.deck.pop())
        self.update_info()
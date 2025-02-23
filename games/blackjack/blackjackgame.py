from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import random

class BlackjackGameLayout(BoxLayout):
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

        # Add Hit and Stand buttons
        self.hit_button = Button(text='Hit', on_press=self.hit)
        self.add_widget(self.hit_button)

        self.stand_button = Button(text='Stand', on_press=self.stand)
        self.add_widget(self.stand_button)

        self.setup_called = False  # ตัวแปรตรวจสอบว่า setup ถูกเรียกหรือยัง

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

    def setup(self):
        """Set up the game (e.g., create a new deck, shuffle, etc.)."""
        if not self.setup_called:
            print("Setting up the game...")
            self.deck = self.create_deck()  # สร้างสำรับใหม่
            self.setup_called = True  # ตั้งค่าเรียบร้อยแล้ว

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

    def stand(self, instance):
        """Handle the player standing."""
        self.update_info()
        # Implement dealer's actions and compare scores
        dealer_score = self.calculate_score(self.dealer_hand)
        if dealer_score < 17:
            self.dealer_hand.append(self.deck.pop())
            self.update_info()

        self.check_winner()

    def check_winner(self):
        """Check who wins the game."""
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        if player_score > 21:
            result = "Player Busts! Dealer Wins!"
        elif dealer_score > 21:
            result = "Dealer Busts! Player Wins!"
        elif player_score > dealer_score:
            result = "Player Wins!"
        elif dealer_score > player_score:
            result = "Dealer Wins!"
        else:
            result = "It's a Tie!"
        
        # Show result in a popup
        popup = Popup(title="Game Over", content=Label(text=result), size_hint=(0.6, 0.4))
        popup.open()

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.metrics import dp
import random
import os
from kivy.core.window import Window

class BlackjackGameLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(20)
        self.size_hint = (1, 1)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Background image
        self.background = Image(
            source='assets/PlayingCards/back6.jpeg',
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=False,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.add_widget(self.background)

        # Display money and bet amount centered
        self.money_bet_box = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10),
            pos_hint={"center_x": 0.5}
        )
        self.money_label = MDLabel(
            id='money_label',
            text="Money: $100000",
            font_style="H6",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        self.bet_label = MDLabel(
            id='bet_label',
            text="Bet: $5000",
            font_style="H6",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        self.money_bet_box.add_widget(self.money_label)
        self.money_bet_box.add_widget(self.bet_label)
        self.add_widget(self.money_bet_box)

        # Buttons to increase/decrease bet amount
        self.bet_buttons_box = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10),
            pos_hint={"center_x": 0.5}
        )
        self.increase_bet_button = MDRaisedButton(
            text="+5000",
            size_hint_x=None,
            width=dp(80),
            on_release=self.increase_bet
        )
        self.decrease_bet_button = MDRaisedButton(
            text="-5000",
            size_hint_x=None,
            width=dp(80),
            on_release=self.decrease_bet
        )
        self.bet_buttons_box.add_widget(self.increase_bet_button)
        self.bet_buttons_box.add_widget(self.decrease_bet_button)
        self.add_widget(self.bet_buttons_box)

        # Display game status message
        self.info_label = MDLabel(
            id='info_label',
            text="Welcome to Blackjack!",
            font_style="H4",
            halign="center",
            markup=True,
            size_hint_y=None,
            height=dp(50),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        self.add_widget(self.info_label)

        self.click_to_continue = MDLabel(
            id='click_to_continue',
            text="Click to Continue",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(50),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        self.click_to_continue.bind(on_touch_down=self.start_game)
        self.add_widget(self.click_to_continue)

        # Area to display dealer's cards
        self.dealer_cards_box = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(200),
            spacing=dp(10),
            padding=dp(10),
            pos_hint={"center_x": 0.5}
        )
        self.dealer_label = MDLabel(
            text="Dealer's Cards",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=self.dealer_label.texture_size[1],
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        self.dealer_cards = MDBoxLayout(
            id='dealer_cards',
            orientation='horizontal',
            size_hint_x=None,
            width=dp(400),
            height=dp(120),
            spacing=dp(10),
            pos_hint={"center_x": 0.5}
        )
        self.dealer_cards_box.add_widget(self.dealer_label)
        self.dealer_cards_box.add_widget(self.dealer_cards)
        self.add_widget(self.dealer_cards_box)

        # Area to display player's cards
        self.player_cards_box = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(200),
            spacing=dp(10),
            padding=dp(10),
            pos_hint={"center_x": 0.5}
        )
        self.player_label = MDLabel(
            text="Player's Cards",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=self.player_label.texture_size[1],
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        self.player_cards = MDBoxLayout(
            id='player_cards',
            orientation='horizontal',
            size_hint_x=None,
            width=dp(400),
            height=dp(120),
            spacing=dp(10),
            pos_hint={"center_x": 0.5}
        )
        self.player_cards_box.add_widget(self.player_label)
        self.player_cards_box.add_widget(self.player_cards)
        self.add_widget(self.player_cards_box)

        # Game control buttons
        self.control_buttons_box = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(20),
            size_hint_y=None,
            height=dp(60),
            pos_hint={"center_x": 0.5}
        )
        self.deal_button = MDRaisedButton(
            text='Deal',
            font_size=dp(18),
            size_hint_x=None,
            width=dp(100),
            height=dp(50),
            md_bg_color=(0, 0, 1, 1),
            on_press=self.deal
        )
        self.hit_button = MDRaisedButton(
            text='Hit',
            font_size=dp(18),
            size_hint_x=None,
            width=dp(100),
            height=dp(50),
            md_bg_color=(1, 0, 0, 1),
            on_press=self.hit
        )
        self.stand_button = MDRaisedButton(
            text='Stand',
            font_size=dp(18),
            size_hint_x=None,
            width=dp(100),
            height=dp(50),
            md_bg_color=(0, 0.6, 0, 1),
            on_press=self.stand
        )
        self.back_to_menu_button = MDRaisedButton(
            text='Back to Menu',
            font_size=dp(18),
            size_hint_x=None,
            width=dp(120),
            height=dp(50),
            md_bg_color=(0.3, 0.3, 0.3, 1),
            on_press=self.back_to_menu
        )
        self.control_buttons_box.add_widget(self.deal_button)
        self.control_buttons_box.add_widget(self.hit_button)
        self.control_buttons_box.add_widget(self.stand_button)
        self.control_buttons_box.add_widget(self.back_to_menu_button)
        self.add_widget(self.control_buttons_box)

        self.money = 100000
        self.bet = 5000
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.game_started = False
        self.deal_button_enabled = True  # Flag to track the state of the "Deal" button

        # ✅ ตรวจจับการเปลี่ยนขนาดหน้าต่าง
        Window.bind(on_resize=self.resize_window)

    def resize_window(self, instance, width, height):
        # ✅ อัปเดต UI ให้เต็มหน้าจอเมื่อขนาดหน้าต่างเปลี่ยน
        self.size = (width, height)
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)  
            Rectangle(size=(width, height), pos=self.pos, source='assets/PlayingCards/back6.jpeg')

    def on_kv_post(self, base_widget):
        self.info_label = self.ids.get("info_label", None)
        self.click_to_continue = self.ids.get("click_to_continue", None)
        self.player_cards = self.ids.get("player_cards", None)
        self.dealer_cards = self.ids.get("dealer_cards", None)
        self.money_label = self.ids.get("money_label", None)
        self.bet_label = self.ids.get("bet_label", None)
        self.deal_button = self.ids.get("deal_button", None)  # Reference to the "Deal" button
        
        if self.money_label and self.bet_label:
            self.update_money_display()
        else:
            print("Error: ไม่พบ money_label หรือ bet_label")

    def create_deck(self):
        # สร้างสำรับไพ่ 52 ใบ
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        deck = [{'suit': suit, 'rank': rank, 'image': f"assets/PlayingCards/{rank}_of_{suit}.png"} for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def setup(self):
        # รีเซ็ตสถานะเกม
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.game_started = False
        self.deal_button_enabled = True  # Enable the "Deal" button
        if hasattr(self, 'info_label'):
            self.info_label.text = "Welcome to Blackjack!"
        if hasattr(self, 'click_to_continue'):
            self.click_to_continue.opacity = 1
        self.update_money_display()
        self.clear_cards()

    def clear_cards(self):
        if hasattr(self, 'player_cards'):
            self.player_cards.clear_widgets()
        if hasattr(self, 'dealer_cards'):
            self.dealer_cards.clear_widgets()

    def update_money_display(self):
        print(f"Debug: money = {getattr(self, 'money', 'ไม่พบ')}, bet = {getattr(self, 'bet', 'ไม่พบ')}")  # Debugging
        if hasattr(self, 'money') and hasattr(self, 'bet'):
            self.money_label.text = f"Money: ${self.money}"
            self.bet_label.text = f"Bet: ${self.bet}"
        else:
            print("Error: money หรือ bet ไม่ถูกกำหนด")

    def increase_bet(self, instance):
        if self.bet + 5000 <= self.money:
            self.bet += 5000
            self.update_money_display()

    def decrease_bet(self, instance):
        if self.bet - 5000 >= 0:
            self.bet -= 5000
            self.update_money_display()

    def deal(self, instance):
        if self.bet > 0 and self.deal_button_enabled:
            if len(self.deck) < 4:  # ✅ ถ้าไพ่ไม่พอแจก 4 ใบ ให้รีเซ็ตเด็คใหม่
                print("Deck is empty! Resetting deck...")
                self.deck = self.create_deck()  

            self.game_started = True
            self.info_label.text = ""
            self.click_to_continue.opacity = 0
            self.clear_cards()
            self.deal_button_enabled = False  # Disable the "Deal" button

            # ✅ ตรวจสอบว่ามีไพ่อยู่ก่อนดึงไพ่
            if len(self.deck) >= 4:
                self.player_hand = [self.deck.pop(), self.deck.pop()]
                self.dealer_hand = [self.deck.pop(), self.deck.pop()]
                self.update_cards()
            else:
                print("Error: Not enough cards to deal!")

    def hit(self, instance):
        if self.game_started:
            self.player_hand.append(self.deck.pop())
            self.update_cards()
            if self.calculate_score(self.player_hand) > 21:
                self.check_winner()

    def stand(self, instance):
        if self.game_started:
            while self.calculate_score(self.dealer_hand) < 17:
                self.dealer_hand.append(self.deck.pop())
            self.update_cards(reveal_dealer=True)
            self.check_winner()

    def calculate_score(self, hand):
        # คำนวณคะแนนของมือ (player หรือ dealer)
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

    def update_cards(self, reveal_dealer=False):
        # อัปเดตการแสดงผลไพ่บนหน้าจอ
        self.clear_cards()
        for card in self.player_hand:
            self.player_cards.add_widget(self.create_card(card))

        for idx, card in enumerate(self.dealer_hand):
            if idx == 0 and not reveal_dealer:
                back_card = {'image': 'assets/PlayingCards/back.png'}
                self.dealer_cards.add_widget(self.create_card(back_card))
            else:
                self.dealer_cards.add_widget(self.create_card(card))

    def create_card(self, card):
        # สร้างวิดเจ็ตการ์ดพร้อมรูปภาพ
        card_image = AsyncImage(source=card['image'], allow_stretch=True, keep_ratio=True)
        return card_image

    def check_winner(self):
        # ตรวจสอบผู้ชนะและอัปเดตข้อความ
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        self.update_cards(reveal_dealer=True)
        if player_score > 21:
            self.info_label.text = "[color=#ff0000]You busted! Dealer wins.[/color]"
            self.money -= self.bet
        elif dealer_score > 21 or player_score > dealer_score:
            self.info_label.text = "[color=#00ff00]You win![/color]"
            self.money += self.bet
        elif player_score < dealer_score:
            self.info_label.text = "[color=#ff0000]Dealer wins.[/color]"
            self.money -= self.bet
        else:
            self.info_label.text = "[color=#ffff00]It's a tie![/color]"
        self.update_money_display()
        self.game_started = False
        self.deal_button_enabled = True  # Re-enable the "Deal" button

    def start_game(self, instance, touch):
        if not self.game_started:
            self.game_started = True
            self.info_label.text = ""
            self.click_to_continue.opacity = 0
            self.clear_cards()
            self.player_hand = [self.deck.pop(), self.deck.pop()]
            self.dealer_hand = [self.deck.pop(), self.deck.pop()]
            self.update_cards()

    def back_to_menu(self, instance):
        app = MDApp.get_running_app()
        app.root.current = 'menu'
        app.root.transition.direction = "up"
        self.setup()

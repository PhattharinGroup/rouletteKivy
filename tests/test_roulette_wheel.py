import unittest
from unittest.mock import Mock, patch
from games.roulette.wheel import RouletteWheel

class TestRouletteWheel(unittest.TestCase):
    def setUp(self):
        self.wheel = RouletteWheel()
        self.wheel.status_display = Mock()

    def test_number_bets(self):
        # Test regular numbers (1-36)
        for num in range(1, 37):
            self.wheel.set_bet(num, 100)
            self.assertTrue(self.wheel._check_win(num))
            self.assertFalse(self.wheel._check_win(num + 1 if num < 36 else 1))

        # Test zero and double zero
        self.wheel.set_bet('0', 100)
        self.assertTrue(self.wheel._check_win('0'))
        self.assertFalse(self.wheel._check_win('00'))

        self.wheel.set_bet('00', 100)
        self.assertTrue(self.wheel._check_win('00'))
        self.assertFalse(self.wheel._check_win('0'))

    def test_dozen_bets(self):
        # First dozen (1-12)
        self.wheel.set_bet('1st 12', 100)
        for num in range(1, 13):
            self.assertTrue(self.wheel._check_win(num))
        self.assertFalse(self.wheel._check_win(13))
        self.assertFalse(self.wheel._check_win('00'))

        # Second dozen (13-24)
        self.wheel.set_bet('2nd 12', 100)
        for num in range(13, 25):
            self.assertTrue(self.wheel._check_win(num))
        self.assertFalse(self.wheel._check_win(12))
        self.assertFalse(self.wheel._check_win(25))

        # Third dozen (25-36)
        self.wheel.set_bet('3rd 12', 100)
        for num in range(25, 37):
            self.assertTrue(self.wheel._check_win(num))
        self.assertFalse(self.wheel._check_win(24))
        self.assertFalse(self.wheel._check_win('00'))

    def test_color_bets(self):
        red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

        # Test RED bets
        self.wheel.set_bet('RED', 100)
        for num in red_numbers:
            self.assertTrue(self.wheel._check_win(num))
        for num in black_numbers:
            self.assertFalse(self.wheel._check_win(num))
        self.assertFalse(self.wheel._check_win('0'))
        self.assertFalse(self.wheel._check_win('00'))

        # Test BLACK bets
        self.wheel.set_bet('BLACK', 100)
        for num in black_numbers:
            self.assertTrue(self.wheel._check_win(num))
        for num in red_numbers:
            self.assertFalse(self.wheel._check_win(num))
        self.assertFalse(self.wheel._check_win('0'))
        self.assertFalse(self.wheel._check_win('00'))

    def test_even_odd_bets(self):
        self.wheel.set_bet('EVEN', 100)
        for num in range(2, 37, 2):
            self.assertTrue(self.wheel._check_win(num))
        for num in range(1, 36, 2):
            self.assertFalse(self.wheel._check_win(num))

        self.wheel.set_bet('ODD', 100)
        for num in range(1, 36, 2):
            self.assertTrue(self.wheel._check_win(num))
        for num in range(2, 37, 2):
            self.assertFalse(self.wheel._check_win(num))

    def test_range_bets(self):
        self.wheel.set_bet('1-18', 100)
        for num in range(1, 19):
            self.assertTrue(self.wheel._check_win(num))
        for num in range(19, 37):
            self.assertFalse(self.wheel._check_win(num))

        self.wheel.set_bet('19-36', 100)
        for num in range(19, 37):
            self.assertTrue(self.wheel._check_win(num))
        for num in range(1, 19):
            self.assertFalse(self.wheel._check_win(num))

if __name__ == '__main__':
    unittest.main()
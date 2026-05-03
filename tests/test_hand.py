import unittest

from models.hand import Hand
from models.card import Card

class TestHand(unittest.TestCase):
    def setUp(self):
        self.hand = Hand()

    def test_simple_score(self):
        """Test the score calculation for a simple hand."""
        self.hand.add_card(Card('♠', '10'))
        self.hand.add_card(Card('♥', '7'))
        self.assertEqual(self.hand.score, 17)

    def test_ace_as_11(self):
        """Test the score calculation with an Ace counted as 11."""
        self.hand.add_card(Card('♠', 'A'))
        self.hand.add_card(Card('♥', '10'))
        self.assertEqual(self.hand.score, 21)

    def test_ace_as_1(self):
        """Test the score calculation with an Ace counted as 1."""
        self.hand.add_card(Card('♠', 'A'))
        self.hand.add_card(Card('♥', '9'))
        self.hand.add_card(Card('♦', '5'))
        self.assertEqual(self.hand.score, 15)

    def test_is_busted(self):
        """Test if the hand is busted."""
        self.hand.add_card(Card('♠', 'A'))
        self.hand.add_card(Card('♥', '9'))
        self.hand.add_card(Card('♦', '5'))
        self.assertFalse(self.hand.is_busted)
        self.hand.add_card(Card('♣', '10'))
        self.assertTrue(self.hand.is_busted)
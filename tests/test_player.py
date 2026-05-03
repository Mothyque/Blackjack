import unittest
from models.player import Player
from models.entities import PlayerEntity
from models.card import Card
from models.hand import Hand

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.entity = PlayerEntity(id=1, username="Tester", balance=1000.0)
        self.player = Player(self.entity)

    def test_place_bet_valid(self):
        """Test if a valid bet decreases the balance."""
        result = self.player.place_bet(100)
        self.assertTrue(result)
        self.assertEqual(self.player.balance, 900.0)
        self.assertEqual(self.player.current_bet, 100)

    def test_place_bet_invalid_amount(self):
        """Test if an invalid bet amount is rejected."""
        result = self.player.place_bet(33) 
        self.assertFalse(result)
        self.assertEqual(self.player.balance, 1000.0)

    def test_place_bet_insufficient_funds(self):
        """Test if the bet is rejected when insufficient funds are available."""
        self.player.balance = 5.0
        result = self.player.place_bet(10)
        self.assertFalse(result)

    def test_split_logic(self):
        """Test if the split creates a new hand and deducts the bet."""
        self.player.place_bet(100)

        self.player.hands[0].add_card(Card('♠', '8'))
        self.player.hands[0].add_card(Card('♥', '8'))
        
        self.assertTrue(self.player.can_split(0))
        
        self.player.split_hand(0)
        
        self.assertEqual(len(self.player.hands), 2)
        self.assertEqual(self.player.balance, 800.0)
        self.assertEqual(len(self.player.bets), 2)
        self.assertEqual(self.player.bets[1], 100)
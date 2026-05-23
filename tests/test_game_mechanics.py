import unittest
from unittest.mock import MagicMock

from models.card import Card
from models.entities import PlayerEntity
from models.player import Player
from utils.blackjackgame import BlackjackGame


class TestGameMechanics(unittest.TestCase):
    def setUp(self):
        self.game = BlackjackGame()
        self.entity = PlayerEntity(id=1, username="testuser", password="hashedpassword", balance=1000.0)
        self.player = Player(self.entity)
        self.game.set_player(self.player)

    def test_initial_deal(self):
        """ Test that the initial deal gives two cards to both player and dealer."""
        self.game.shoe.draw_card = MagicMock(side_effect=[
            Card('♠', '10'),  
            Card('♥', '7'),   
            Card('♦', 'K'),   
            Card('♣', '9')    
        ])

        self.game._deal_initial_cards()

        self.assertEqual(len(self.game.player.hands[0].cards), 2)
        self.assertEqual(len(self.game.dealer.hand.cards), 2)

        self.assertEqual(self.game.player.hands[0].score, 20)
        self.assertEqual(self.game.dealer.hand.score, 16)
    
    def test_dealer_stands_on_17(self):
        """ Test that the dealer stands on a soft 17 or higher."""
        self.game.dealer.hand.add_card(Card('♠', '10'))
        self.game.dealer.hand.add_card(Card('♥', '7'))
        
        self.game.shoe.draw_card = MagicMock(return_value=Card('♦', '2'))
        
        self.game._dealer_turn()
        
        self.game.shoe.draw_card.assert_not_called()
        self.assertEqual(self.game.dealer.hand.score, 17)

    def test_double_down(self):
        """ Test that double down correctly doubles the bet and gives one card."""
        self.player.balance = 500.0
        self.player.place_bet(100.0)

        self.player.hands[0].add_card(Card('♠', '5'))
        self.player.hands[0].add_card(Card('♥', '6'))

        self.game.shoe.draw_card = MagicMock(return_value=Card('♦', '10')) 

        self.assertTrue(self.player.can_double_down(0))

        self.player.double_down(0)
        self.player.receive_card(self.game.shoe.draw_card(), 0)

        self.assertEqual(self.player.balance, 300.0)
        self.assertEqual(self.player.bets[0], 200.0)
        self.assertEqual(self.player.hands[0].score, 21)
        self.assertEqual(len(self.player.hands[0].cards), 3)

    def test_resolve_winner_player_wins(self):

        self.player.place_bet(100.0)
        initial_balance = self.player.balance
        
        self.player.hands[0].add_card(Card('♠', '10'))
        self.player.hands[0].add_card(Card('♥', 'K'))
        
        self.game.dealer.hand.add_card(Card('♦', '10'))
        self.game.dealer.hand.add_card(Card('♣', '8'))
        
        self.game._resolve_winner()
        
        self.assertEqual(self.player.balance, initial_balance + 200.0)
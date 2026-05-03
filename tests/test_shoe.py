import unittest
from models.shoe import Shoe

class TestShoe(unittest.TestCase):
    def test_shoe_initial_size(self):
        """Test the initial size of the shoe."""
        shoe = Shoe(num_decks=6)
        self.assertEqual(shoe.cards_left, 312)

    def test_draw_card(self):
        """Test drawing a card from the shoe."""
        shoe = Shoe(num_decks=1)
        initial_count = shoe.cards_left
        shoe.draw_card()
        self.assertEqual(shoe.cards_left, initial_count - 1)

    def test_needs_reshuffle(self):
        """Test if the shoe needs reshuffling."""
        shoe = Shoe(num_decks=1)
        while shoe.cards_left > shoe.cut_card_position:
            shoe.draw_card()
        
        shoe.draw_card()
        self.assertTrue(shoe.needs_reshuffle)
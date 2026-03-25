import random
from typing import List
from models.card import Card

class Shoe:
    """ Represents a shoe of cards used in Blackjack. A shoe typically contains multiple decks of cards."""

    def __init__(self, num_decks: int = 6):
        self.num_decks = num_decks
        self.cards: List[Card] = []
        self.cut_card_position: int = 0
        self.needs_reshuffle: bool = False

        self.suits = ['♠', '♥', '♦', '♣']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

        self.build_and_shuffle()

    def build_and_shuffle(self):
        """ Generates the shoe, shuffles it and sets the cut card position. """
        self.cards = [Card(suit, rank) for _ in range(self.num_decks) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)
        self.needs_reshuffle = False

        min_cards_left = 52
        max_cards_left = int(52 * 1.5)
        self.cut_card_position = random.randint(min_cards_left, max_cards_left)
    
    def draw_card(self) -> Card:
        """ Draws a card from the shoe. If the cut card is reached, marks that a reshuffle is needed. """
        if not self.cards:
            raise ValueError("The shoe is empty. Cannot draw a card.")
        
        card = self.cards.pop(0)
        if len(self.cards) <= self.cut_card_position:
            self.needs_reshuffle = True
        

        return card
    
    @property
    def cards_left(self) -> int:
        """ Returns the number of cards left in the shoe. """
        return len(self.cards)


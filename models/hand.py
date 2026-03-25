from typing import List, Tuple
from models.card import Card

class Hand:
    """ Represents a player's or dealer's hand in Blackjack. """

    def __init__(self):
        self.cards: List[Card] = []

    def add_card(self, card: Card):
        """ Adds a card to the hand. """
        self.cards.append(card)

    def get_score_details(self) -> Tuple[int, bool]:
        """ Calculates the total score of the hand and whether the hand is soft.
            Returns:
                Tuple[int, bool]: (best_score, is_soft)
        """

        total = 0
        aces_as_11 = 0

        for card in self.cards:
            total += card.value
            if card.rank == 'A':
                aces_as_11 += 1

        while total > 21 and aces_as_11 > 0:
            total -= 10
            aces_as_11 -= 1
        
        is_soft = aces_as_11 > 0

        return total, is_soft
    
    @property
    def score(self) -> int:
        """ Returns the best score of the hand. """
        total, _ = self.get_score_details()
        return total

    @property
    def display_score(self) -> str:
        """ Returns a string formatted for UI. Shows alternative values for soft hands. (e.g. '8/18' or '13')."""
        total, is_soft = self.get_score_details()
        if is_soft and total < 21:
            return f"{total-10}/{total}"
        else:
            return str(total)
        
    @property
    def is_busted(self) -> bool:
        """ Returns True if the hand's score exceeds 21. """
        return self.score > 21
    
    def __str__(self):
        """Retunrs the visual representation of the hand's cards."""
        cards_str = ", ".join(str(card) for card in self.cards)
        return f"[{cards_str}]"
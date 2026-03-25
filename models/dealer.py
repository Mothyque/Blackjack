from models.hand import Hand
from models.card import Card

class Dealer:
    """ Represents the dealer in the Blackjack game. The dealer has a hand and follows specific rules for drawing cards. """

    def __init__(self):
        self.name = "Dealer"
        self.hand = Hand()

    def receive_card(self, card: Card):
        """ Adds a card to the dealer's hand. """
        self.hand.add_card(card)

    def clear_hand(self):
        """ Clears the dealer's hand for a new round. """
        self.hand = Hand()

    @property
    def upcard(self) -> Card:
        """ Returns the first card of the dealer that sits face up """
        if len(self.hand.cards) > 0:
            return self.hand.cards[0]
        return None

    @property
    def should_hit(self) -> bool:
        """ The rule of thumb for the dealer: hit if the score is less than 17, otherwise stand. """
        return self.hand.score < 17
    
    def display_partial_hand(self) -> str:
        """ Shows only the upcard of the dealer's hand for UI purposes. """
        if len(self.hand.cards) > 0:
            return f"[{self.upcard}, 🂠]"
        else:
            return str(self.hand)
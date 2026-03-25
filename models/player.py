from models.hand import Hand
from models.card import Card

class Player:
    """ Represents a player in the Blackjack game. """

    def __init__(self, name: str, initial_balance: float = 1000.0):
        self.name = name
        self.balance = initial_balance
        self.current_bet = 0.0
        self.hand = Hand()

    def place_bet(self, amount: float) -> bool:
        """ Places a bet for the current round. Returns True if the bet is successfully placed, False otherwise. """
        available_bets = [10, 20, 50, 100, 200]
        if amount > self.balance or amount <= 0 or amount not in available_bets:
            return False
        
        self.current_bet = amount
        self.balance -= amount
        return True
    
    def double_down(self):
        """ Places another bet of the same value of the current bet and draws a new card. Returns True if the double down is successful, False otherwise. """
        if not self.can_double_down():
            return
        self.balance -= self.current_bet
        self.current_bet *= 2
    
    def can_double_down(self) -> bool:
        return self.current_bet > 0 and self.current_bet * 2 <= self.balance + self.current_bet and len(self.hand.cards) == 2
    
    def win_bet(self, payout_ratio: float = 1.0):
        """ The player wins the hand. The payout is 1:1 for a normal win and 3:2 for a Blackjack"""
        profit = self.current_bet * payout_ratio
        self.balance += (self.current_bet + profit)
        self.current_bet = 0.0

    def lose_bet(self):
        """ The player loses the hand. The bet is already deducted from the balance when placed, so we just reset the current bet."""
        self.current_bet = 0.0

    def push_bet(self):
        """ The hand is a push (tie). The player's bet is returned to their balance."""
        self.balance += self.current_bet
        self.current_bet = 0.0

    def receive_card(self, card: Card):
        """Adds a card to the player's hand."""
        self.hand.add_card(card)

    def clear_hand(self):
        """ Clears the player's hand for a new round."""
        self.hand = Hand()
    
    def __str__(self):
        """ Returns a string representation of the player, including their name, balance, current bet and hand."""
        return f"Player: {self.name} | Balance: ${self.balance:.2f} | Current Bet: ${self.current_bet:.2f} | Hand: {self.hand}"
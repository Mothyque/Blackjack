from models.hand import Hand
from models.card import Card

class Player:
    """ Represents a player in the Blackjack game. """

    def __init__(self, name: str, initial_balance: float = 1000.0):
        self.name = name
        self.balance = initial_balance
        self.current_bet = 0.0

        self.hands = [Hand()]
        self.bets = []

    def set_current_bet(self, bet: float):
        self.current_bet = bet

    def place_bet(self, amount: float) -> bool:
        """ Places a bet for the current round. Returns True if the bet is successfully placed, False otherwise. """
        available_bets = [10, 20, 50, 100, 200]
        if amount > self.balance or amount <= 0 or amount not in available_bets:
            return False
        
        self.current_bet = amount
        self.balance -= amount

        self.hands = [Hand()]
        self.bets = [amount]
        return True
    
    def can_double_down(self, hand_index: int = 0) -> bool:
        bet = self.bets[hand_index]
        hand = self.hands[hand_index]
        return bet > 0 and bet <= self.balance and len(hand.cards) == 2

    def double_down(self, hand_index: int = 0):
        """ Places another bet of the same value of the current bet and draws a new card. Returns True if the double down is successful, False otherwise. """
        if not self.can_double_down(hand_index):
            return False
        
        self.balance -= self.bets[hand_index]
        self.bets[hand_index] *= 2
    
    def can_split(self, hand_index: int = 0) -> bool:
        hand = self.hands[hand_index]
        bet = self.bets[hand_index]
        if len(hand.cards) == 2 and hand.cards[0].value == hand.cards[1].value and bet <= self.balance:
            return True
        return False

    def split_hand(self, hand_index: int = 0):
        if not self.can_split(hand_index):
            return 
        original_hand = self.hands[hand_index]
        bet = self.bets[hand_index]

        split_card = original_hand.cards.pop()
        new_hand = Hand()
        new_hand.add_card(split_card)

        self.hands.append(new_hand)
        self.bets.append(bet)
        self.balance -= bet
    
    def win_bet(self, hand_index: int = 0, payout_ratio: float = 1.0):
        """ The player wins the hand. The payout is 1:1 for a normal win and 3:2 for a Blackjack"""
        profit = self.bets[hand_index] * payout_ratio
        self.balance += (self.bets[hand_index] + profit)
        

    def lose_bet(self, hand_index: int = 0):
        """ The player loses the hand. The bet is already deducted from the balance when placed, so we just reset the current bet."""

    def push_bet(self, hand_index: int = 0):
        """ The hand is a push (tie). The player's bet is returned to their balance."""
        self.balance += self.bets[hand_index]

    def receive_card(self, card: Card, hand_index: int = 0):
        """Adds a card to the player's hand."""
        self.hands[hand_index].add_card(card)

    def clear_hand(self):
        """ Clears the player's hand for a new round."""
        self.hands = [Hand()]
        self.bets = []
    
    def __str__(self):
        """ Returns a string representation of the player, including their name, balance, current bet and hand."""
        return f"Player: {self.name} | Balance: ${self.balance:.2f} | Current Bet: ${self.current_bet:.2f} | Hand: {self.hand}"
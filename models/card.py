class Card:
    """ Represents a single playing card with a suit and rank. """

    def __init__(self, suit : str, rank : str):
        self.suit = suit
        self.rank = rank

    @property
    def value(self) -> int:
        """ Returns the Blackjack value of the card. """
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  
        else:
            return int(self.rank) 
        
    @property
    def get_rank(self) -> str:
        """ Returns the rank of the card. """
        return self.rank
        
    def __str__(self):
        """ Returns a string representation of the card. """
        return f"{self.rank} {self.suit}"
    
    def __repr__(self):
        return self.__str__()
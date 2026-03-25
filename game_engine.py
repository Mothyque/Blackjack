from models.shoe import Shoe
from models.player import Player
from models.dealer import Dealer

class BlackJackGame:
    def __init__(self):
        self.player = ""
        self.dealer = Dealer()
        self.shoe = Shoe(num_decks=6)

    def set_player_name(self, name: str):
        """ Sets the player's name. """
        self.player = Player(name)

    def play_round(self):
        print(f"{'-' * 30}")
        print("User: " + self.player.name)
        print(f"Balance: ${self.player.balance:.2f}" + "$")

        self._handle_betting()
        self._check_and_reshuffle()
        self._deal_initial_cards() 
        self._display_hands(initial=True)
        self._handle_insurance()
        if self._check_initial_blackjacks():
            return

        while not self.player.hand.is_busted:
            if self.player.can_double_down():
                action = input("(H)it | (S)tand | (D)ouble \n>>>> ").strip().lower()
            else:
                action = input("(H)it | (S)tand \n>>>> ").strip().lower()
            if action == 'h':
                self.player.receive_card(self.shoe.draw_card())
                print(f"You have: {self.player.hand} - Score: {self.player.hand.display_score}")
            elif action == 's':
                break
            elif action == 'd':
                if self.player.can_double_down():
                    self.player.double_down()
                    self.player.receive_card(self.shoe.draw_card())
                    print(f"You have: {self.player.hand} - Score: {self.player.hand.display_score}")
                    break
                else:
                    print("Invalid choice. You cannot double down.")
            else:
                print("Invalid choice. Press 'H', 'S', or 'D'.")

        if self.player.hand.is_busted:
            print("Bust! Dealer wins.")
            self.player.lose_bet()
            self._cleanup()
            return 
        
        print(f"\nDealer's turn.\nDealer has: {self.dealer.hand} - Score: {self.dealer.hand.score}")

        while self.dealer.should_hit:
            self.dealer.receive_card(self.shoe.draw_card())
            print("Dealer draws.")
            print(f"Dealer has: {self.dealer.hand} - Score: {self.dealer.hand.score}")

        player_score = self.player.hand.score
        dealer_score = self.dealer.hand.score

        if self.dealer.hand.is_busted:
            print("Dealer busts! You win 1:1.")
            self.player.win_bet(1.0)
        elif player_score > dealer_score:
            print("You win 1:1!")
            self.player.win_bet(1.0)
        elif player_score < dealer_score:
            print("Dealer wins.")
            self.player.lose_bet()
        else:
            print("Push (Tie). Your bet is returned.")
            self.player.push_bet()

        self._cleanup()

    def _handle_betting(self):
        while True:
            try:
                print(f"Available bets: 10$, 20$, 50$, 100$, 200$")
                bet = float(input("Enter your bet: \n>"))
                if self.player.place_bet(bet):
                    break
                else:
                    print("Invalid bet. Please check your balance and available bets.")
            except ValueError:
                print("Please enter a valid number.")

    def _check_and_reshuffle(self):
        if self.shoe.needs_reshuffle:
            print("Reshuffling the shoe...")
            self.shoe.build_and_shuffle()

    def _deal_initial_cards(self):
        self.player.receive_card(self.shoe.draw_card())
        self.dealer.receive_card(self.shoe.draw_card())
        self.player.receive_card(self.shoe.draw_card())
        self.dealer.receive_card(self.shoe.draw_card())

    def _display_hands(self, initial = False):
        if initial:
            print(f"\nDealer shows: {self.dealer.display_partial_hand()}")
        else:
            print(f"\nDealer has: {self.dealer.hand} - Score: {self.dealer.hand.score}")
        print(f"You have: {self.player.hand} - Score: {self.player.hand.display_score}") 

    def _handle_insurance(self):
        if self.dealer.upcard.rank != 'A':
            return
        print("Do you want to take insurance? (Y/N)")
        insurance_choice = input("> ").strip().lower()
        if insurance_choice == 'y':
            insurance_bet = self.player.current_bet / 2
            if insurance_bet > self.player.balance:
                print("You don't have enough balance for insurance bet.")
            else:
                self.player.balance -= insurance_bet
                print(f"Insurance bet of ${insurance_bet:.2f} placed.")
                if self.dealer.hand.score == 21:
                    print("Dealer has Blackjack! Insurance bet wins 2:1.")
                    self.player.balance += insurance_bet * 3
                else:
                    print("Dealer does not have Blackjack. Insurance bet lost.")
        else:
            print("You chose not to take insurance.")
    
    def _check_initial_blackjacks(self) -> bool:
        player_bj = self.player.hand.score == 21
        dealer_bj = self.dealer.hand.score == 21

        if player_bj and not dealer_bj:
            print("Blackjack! You win 3:2 payout")
            self.player.win_bet(1.5)
            self._cleanup()
            return True
        elif not player_bj and dealer_bj:
            print("Dealer has Blackjack! Dealer wins.")
            self.player.lose_bet()
            self._cleanup()
            return True

        elif player_bj and dealer_bj:
            print("Both you and the dealer have Blackjack! Push (Tie). Your bet is returned.")
            self.player.push_bet()
            self._cleanup()
            return True
        
        return False

    def _cleanup(self):
        """ Cleans the hands at the end of the round. """
        self.player.clear_hand()
        self.dealer.clear_hand()

    def run(self):
        """ The main loop for running the game """
        while self.player.balance > 0:
            self.play_round()

            if self.player.balance <= 0:
                print("\nGame Over! You are out of money.")
                break
            while True:  
                play_again = input("\nPlay another round? (Y/N): ").strip().lower()
                if play_again == 'n':
                    print(f"Thanks for playing! You leave with ${self.player.balance:.2f}")
                    return
                elif play_again == 'y':
                    break
                else:
                    print("Invalid input. Please enter 'Y' or 'N'.")
    def menu(self):
        """ Displays the main menu and handles user input for starting the game or quitting. """
        while True:
            print("=== Welcome to Blackjack ===")
            print("1. Start Game")
            print("2. Quit")
            choice = input("> ").strip()
            if choice == '1':
                name = input("Enter your name: ")
                self.set_player_name(name)
                self.run()
                break
            elif choice == '2':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    game = BlackJackGame()
    game.menu()
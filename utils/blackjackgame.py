from models.dealer import Dealer
from models.player import Player
from models.shoe import Shoe


class BlackJackGame:
    def __init__(self):
        self.player = ""
        self.dealer = Dealer()
        self.shoe = Shoe(num_decks=6)
        self.change_bet = False
        self.insurnace_bet = 0.0

    def set_player_name(self, name: str):
        self.player = Player(name)

    def set_change_bet(self, change: bool):
        self.change_bet = change

    def set_player_bet(self, bet: float):
        self.player.set_current_bet(bet)

    def play_round(self):
        print(f"{'-' * 30}")
        print("User: " + self.player.name)
        print(f"Balance: ${self.player.balance:.2f}" + "$")
        print(f"Current bet: ${self.player.current_bet:.2f}")


        self._handle_betting()
        self._check_and_reshuffle()
        self._deal_initial_cards() 
        self._display_hands(initial=True)
        self._handle_insurance()

        if not self._player_turn():
            self._resolve_insurance()
            self._cleanup()
            return
        
        self._dealer_turn()
        self._resolve_insurance()
        self._resolve_winner()
        self._cleanup()

    def _handle_betting(self):
        while True:
            try:
                if self.player.current_bet <= 0 or self.change_bet:
                    print(f"Available bets: 10$, 20$, 50$, 100$, 200$")
                    self.player.current_bet = float(input("Enter your bet: ").strip())
                    self.set_change_bet(False)

                if self.player.place_bet(self.player.current_bet):
                    break
                else:
                    print("Invalid bet. Please check your balance and available bets.")
                    self.set_change_bet(True)

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
        hand = self.player.hands[0]
        print(f"You have: {hand} - Score: {hand.display_score}") 

    def _handle_insurance(self):
        if self.dealer.upcard.rank != 'A':
            return
        print("Do you want to take insurance? (Y/N)")
        insurance_choice = input("> ").strip().lower()
        if insurance_choice == 'y':
            self.insurnace_bet = self.player.bets[0] / 2
            if self.insurnace_bet > self.player.balance:
                print("You don't have enough balance for insurance bet.")
                self.insurnace_bet = 0.0
            else:
                self.player.balance -= self.insurnace_bet
                print(f"Insurance bet of ${self.insurnace_bet:.2f} placed.")
        else:
            print("You chose not to take insurance.")
    
    def _resolve_insurance(self):
        if self.insurnace_bet <= 0:
            return
        dealer_bj = self.dealer.hand.score == 21
        if dealer_bj:
            print("Dealer has Blackjack! Insurance bet pays 2:1.")
            self.player.balance += self.insurnace_bet * 3
        else:
            print("Dealer does not have Blackjack. You lose the insurance bet.")
        self.insurnace_bet = 0.0

    def _player_turn(self) -> bool:
        hand_index = 0
        all_busted = True
        while hand_index < len(self.player.hands):
            hand = self.player.hands[hand_index]
            total_hands = len(self.player.hands)

            if total_hands > 1:
                print(f"\n=== Playing hand {hand_index + 1} / {total_hands} ===")

            while not hand.is_busted:
                if hand.score == 21:
                    print(f"You have: {hand} - Blackjack!")
                    break

                options = ["(H)it", "(S)tand"]
                if self.player.can_double_down(hand_index):
                    options.append("(D)ouble Down")
                if self.player.can_split(hand_index):
                    options.append("S(p)lit")

                print("Options: " + ", ".join(options))
                choice = input("> ").strip().lower()

                if choice == 'h':
                    self.player.receive_card(self.shoe.draw_card(), hand_index)
                    print(f"You have: {hand} - Score: {hand.display_score}")
                
                elif choice == 's':
                    break

                elif choice == 'd' and self.player.can_double_down(hand_index):
                    self.player.double_down(hand_index)
                    self.player.receive_card(self.shoe.draw_card(), hand_index)
                    print(f"You have: {hand} - Score: {hand.display_score}")
                    break

                elif choice == 'p' and self.player.can_split(hand_index):
                    self.player.split_hand(hand_index)
                    self.player.receive_card(self.shoe.draw_card(), hand_index) 
                    self.player.receive_card(self.shoe.draw_card(), len(self.player.hands) - 1)
                    print(f"You have: {hand} - Score: {hand.display_score}")
                    
                else:
                    print("Invalid choice. Please select a valid option from the menu.")
            if hand.is_busted:
                if total_hands > 1:
                    print(f"Hand {hand_index + 1} busted. Dealer wins this hand.")
                else:
                    print("You busted! Dealer wins.")
            else:
                all_busted = False
            hand_index += 1
        return not all_busted
    
    def _dealer_turn(self):
        print(f"\nDealer's turn.\nDealer has: {self.dealer.hand} - Score: {self.dealer.hand.score}")

        while self.dealer.should_hit:
            self.dealer.receive_card(self.shoe.draw_card())
            print("Dealer draws.")
            print(f"Dealer has: {self.dealer.hand} - Score: {self.dealer.hand.score}")

    def _resolve_winner(self):
        dealer_score = self.dealer.hand.score
        total_hands = len(self.player.hands)
        dealer_bj = dealer_score == 21 and len(self.dealer.hand.cards) == 2
        if dealer_score > 21:
            print("\nDealer busts!")
        for i, hand in enumerate(self.player.hands):
            if hand.is_busted:
                continue 
            
            player_score = hand.score
            player_bj = player_score == 21 and len(hand.cards) == 2
            if total_hands > 1:
                print(f"\n=== Resolving hand {i + 1} / {total_hands} ===")
            if player_bj and not dealer_bj:
                print(f"You win with a Blackjack! Payout is 3:2.")
                self.player.win_bet(i, 1.5)
            elif dealer_bj and not player_bj:
                print("Dealer has Blackjack. You lose this hand.")
                self.player.lose_bet(i)
            elif player_score > dealer_score or dealer_score > 21:
                print("You win this hand!")
                self.player.win_bet(i)
            elif player_score < dealer_score:
                print("Dealer wins this hand.")
                self.player.lose_bet(i)
            else:
                print("Push. Your bet is returned.")
                self.player.push_bet(i)


    def _cleanup(self):
        """ Cleans the hands at the end of the round. """
        self.player.clear_hand()
        self.dealer.clear_hand()
        self.insurnace_bet = 0.0
from utils.blackjackgame import BlackJackGame


class GameMenu:
    def __init__(self):
        self.game = None

    def start(self):
        while True:
            print("\n==== Welcome to Blackjack! ====")
            print("1. Start New Game")
            print("2. Exit")
            choice = input(">>> ").strip()

            if choice == '1':
                name = input("Enter your name: ")
                self.game = BlackJackGame()
                self.game.set_player_name(name)
                self.run_game_loop()
            elif choice == '2':
                print("Thanks for playing! Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

    def run_game_loop(self):
        while self.game.player.balance > 0:
            self.game.play_round()

            if self.game.player.balance <= 0:
                print("You have run out of money! Game over.")
                break

            while True:
                print(30 * "-")
                print(f"Current balance: ${self.game.player.balance:.2f}")
                print("Change bet? (B)")
                print("Play again (Y/N)")
                play_again = input("> ").strip().lower()
                if play_again == 'y':
                    break
                elif play_again == 'n':
                    print("Thanks for playing! Goodbye!")
                    return
                elif play_again == 'b':
                    self.game.set_change_bet(True)
                    break
                else:
                    print("Invalid choice. Please enter Y or N.") 
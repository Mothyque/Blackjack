from services.player_service import PlayerService
from utils.blackjackgame import BlackJackGame


class GameMenu:
    def __init__(self, player_service: PlayerService):
        self.game = None
        self.player_service = player_service

    def start(self):
        while True:
            print("\n==== Welcome to Blackjack! ====")
            print("1. Start New Game")
            print("2. Exit")
            choice = input(">>> ").strip()

            if choice == '1':
                name = input("Enter your name: ")
                password = input("Enter your password: ")
                player = self.check_login(name, password)
                if player:
                    self.game = BlackJackGame()
                    self.game.set_player(player)
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
                    self.player_service.save_player_state(self.game.player)
                    return
                elif play_again == 'b':
                    self.game.set_change_bet(True)
                    break
                else:
                    print("Invalid choice. Please enter Y or N.") 

    def check_login(self, username: str, password: str):
        player = self.player_service.login_player(username, password)
        if player:
            print(f"Welcome back, {player.name}!")
            return player
        else:
            print("Invalid username or password. Please try again.")
            return None
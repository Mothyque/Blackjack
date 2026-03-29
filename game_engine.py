from database.db_context import DatabaseContext
from repositories.player_repository import PlayerRepository
from services.player_service import PlayerService
from utils.gamemenu import GameMenu

from werkzeug.security import generate_password_hash
from models.entities import PlayerEntity

def seed_initial_users(player_service):
    repo = player_service.repository
    
    test_users = [
        {"user": "andrei", "pass": "andrei123", "bal": 2500.0},
        {"user": "elena", "pass": "parola123", "bal": 5000.0},
        {"user": "jucator", "pass": "blackjack", "bal": 1000.0}
    ]

    for data in test_users:
        # Aici se producea eroarea dacă PlayerEntity nu era mapat
        if not repo.get_by_username(data["user"]):
            new_user = PlayerEntity(
                username=data["user"],
                password=generate_password_hash(data["pass"]),
                balance=data["bal"]
            )
            repo.save(new_user)
            print(f"[Database] Utilizatorul '{data['user']}' a fost creat.")

if __name__ == "__main__":
    db_context = DatabaseContext("sqlite:///blackjack.sqlite3")
    db_context.setup_database()
    session = db_context.get_session()
    try:
        repo = PlayerRepository(session)
        service = PlayerService(repo)

        seed_initial_users(service)

        menu = GameMenu(service)
        menu.start()
    finally:
        if menu.game.player:
            service.save_player_state(menu.game.player)
        session.close()
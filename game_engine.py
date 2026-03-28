from repositories.player_repository import PlayerRepository
from services.player_service import PlayerService
from utils.gamemenu import GameMenu

if __name__ == "__main__":
    PlayerRepository = PlayerRepository()
    PlayerService = PlayerService(PlayerRepository)
    menu = GameMenu(PlayerService)
    menu.start()
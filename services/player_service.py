from models.entities import PlayerEntity
from models.player import Player
from repositories.player_repository import PlayerRepository
from werkzeug.security import generate_password_hash, check_password_hash

class PlayerService:
    def __init__ (self, repository: PlayerRepository):
        self.repository = repository

    def login_player(self, username: str, password: str):
        entity = self.repository.get_by_username(username)
        if entity and check_password_hash(entity.password, password):
            return Player(entity)
        return None
    
    def save_player_state(self, player: Player):
        entity  = self.repository.get_by_username(player.name)
        if entity:
            entity.balance = player.balance
            self.repository.save(entity)
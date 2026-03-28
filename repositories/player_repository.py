from models.entities import PlayerEntity


class PlayerRepository:
    def __init__(self, session):
        self.session = session

    def get_by_username(self, username: str):
        return self.session.query(PlayerEntity).filter_by(username=username).first()

    def get_by_id(self, player_id: int):
        return self.session.query(PlayerEntity).filter_by(id=player_id).first()
    
    def save(self, player_entity: PlayerEntity):
        self.session.add(player_entity)
        self.session.commit()

    def get_all_players(self):
        return self.session.query(PlayerEntity).all()
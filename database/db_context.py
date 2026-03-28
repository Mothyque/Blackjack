from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, registry
from models.entities import User, PlayerEntity

class DatabaseContext:
    def __init__(self, db_url:str):
        self.engine = create_engine(db_url)
        self.metadata = MetaData()
        self.Session = sessionmaker(bind=self.engine)
        self.mapper_registry = registry()

        self.players_table = Table(
            'players', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('username', String, unique=True, nullable=False),
            Column('password', String, nullable=False),
            Column('balance', Float, default=1000.0)
            )
    
    def setup_database(self):
        if not self.mapper_registry.mappers:
            self.mapper_registry.map_imperatively(PlayerEntity, self.players_table)
        self.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()
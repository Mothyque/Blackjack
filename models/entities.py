from dataclasses import dataclass, field

@dataclass
class User:
    id: int  = None
    username: str = ""
    password: str = ""

@dataclass
class PlayerEntity(User):
    balance: float = 1000.0
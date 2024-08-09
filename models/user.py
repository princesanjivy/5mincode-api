from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: str
    user_name: str
    display_picture: str
    total_coins: int
    current_streak: int
    # joined_on: str # TODO: change to DateTime()


class Room(BaseModel):
    users: List[User]

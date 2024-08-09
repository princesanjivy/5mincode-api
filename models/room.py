from typing import Any, List

from pydantic import BaseModel, Field

from models.user import User


class GenRoomCodeReq(BaseModel):
    roomOwnerId: str


class RunCode(BaseModel):
    code: str
    userId: str


class CreateRoomReq(BaseModel):
    max_players: int
    duration: int
    room_name: str
    max_questions: int


class UserInfo(BaseModel):
    user: User
    is_completed: bool = Field(default=False)
    score: int = Field(default=10)
    # completed_at: str = Field(default=None)


class RoomInfo(BaseModel):
    user_info: List[UserInfo]
    owner_id: str
    is_started: bool = Field(default=False)
    start_time: str = Field(default="")  # be empty str
    is_custom_question: bool = Field(default=False)
    question_ids: List[str]
    points: int = Field(default=10)
    duration_in_seconds: int = Field(default=500)
    room_name: str
    description: str
    # created_at: str
    is_ended: bool = Field(default=False)

from typing import Any, Dict

from fastapi import WebSocket
from fastapi.websockets import WebSocketState
from pydantic import BaseModel

from db.memstore import Memstore
from models.room import RoomInfo, UserInfo
from models.user import User


class MyConnection(BaseModel):
    user: User


class WSConnectionManager:
    def __init__(self):
        self.memstore = Memstore()
        self.websockets: Dict[str, Dict[str, WebSocket]] = {}
        self.connection_key = "active_room_connections"

    async def connect(self, websocket: WebSocket, user: User, room_id: str):
        await websocket.accept()

        data = self.memstore.get(room_id)
        if data:
            # entry present
            print("user exist..")
            self.websockets.setdefault(room_id, {})[user.id] = websocket
            room_info = RoomInfo.parse_obj(data)
            # verify if current user is already there
            for u in room_info.user_info:
                if u.user.id == user.id:
                    print("skip")
                    break
            else:
                print("new user; add to existing room")
                user_info = UserInfo(user=user)
                room_info.user_info.append(user_info)
        else:
            print("very first new user")
            self.websockets[room_id] = {user.id: websocket}  # Store WebSocket in memory
            user_info = UserInfo(user=user)
            print(user_info.dict())
            room_info = RoomInfo(
                user_info=[user_info],
                owner_id=user.id,
                question_ids=["NAtMrXgsHbyGNthtw8GV"],
                room_name="testing",
                description="testing",
            )

        room_info_dict = room_info.dict()
        self.memstore.set(room_id, room_info_dict)
        print("saved", room_info_dict)
        await self.broadcast(
            room_id,
            "ROOMINFO",
            room_info_dict,
        )

    async def disconnect(self, room_id: str, client_id: str):
        data = self.memstore.get(room_id)
        room_info = RoomInfo.parse_obj(data)

        if room_id in self.websockets and client_id in self.websockets[room_id]:
            websocket = self.websockets[room_id][client_id]
            if websocket.application_state == WebSocketState.CONNECTED:
                del self.websockets[room_id][client_id]

                # remove user from redis memstore
                temp = [u for u in room_info.user_info if u.user.id != client_id]
                room_info.user_info = temp
                room_info_dict = room_info.dict()
                self.memstore.set(room_id, room_info_dict)

                # update other users in room
                await self.broadcast(
                    room_id,
                    "ROOMINFO",
                    room_info_dict,
                )

                if not self.websockets[room_id]:  # Remove the room entry if it's empty
                    del self.websockets[room_id]

        # await websocket.close()  # close connection

    async def broadcast(self, room_id: str, method: str, data: Any):
        print("broadcast called", room_id)
        if room_id in self.websockets:
            print(True)
            websockets = list(self.websockets[room_id].values())
            print(len(websockets))
            for websocket in websockets:
                if websocket.application_state == WebSocketState.CONNECTED:
                    print("sending to client...")
                    await websocket.send_json(
                        {"message": data, "method": method},
                    )

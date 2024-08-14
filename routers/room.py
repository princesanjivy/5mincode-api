import json
import random

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, status

from dao.user import get_user
from db.firestore import FirebaseFirestore
from db.memstore import Memstore
from models.room import CreateRoomReq, GenRoomCodeReq, RoomInfo
from utils.ws import WSConnectionManager

manager = WSConnectionManager()
router = APIRouter(prefix="/room")
firestore = FirebaseFirestore()


@router.post("/code", tags=["room"])
def gen_room_code(payload: GenRoomCodeReq):
    while True:
        roomId = random.randint(100000, 999999)
        doc_ref = firestore.instance.collection("rooms").document(str(roomId))
        doc = doc_ref.get()
        if not doc.exists:
            break
    doc_ref.set({"roomOwnerId": payload.roomOwnerId})
    return {"roomId": roomId}


@router.post("", tags=["room"])
def create(payload: CreateRoomReq):
    print(payload)
    return {"roomId": 123456}


@router.get("/exist/{room_code}", tags=["room"])
def exist(room_code: str):
    if room_code == "123456":
        return {"exists": True}
    room_ref = firestore.instance.collection("rooms").document(room_code)
    doc = room_ref.get()
    if doc.exists:
        return {"exists": True}
    return {"exists": False}


@router.websocket("/{room_id}/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, room_id: str):
    user = get_user(id=client_id)
    await manager.connect(websocket, user, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            incoming_data = json.loads(data)
            print(incoming_data)
            if incoming_data["message"] == "START":
                # set is_started to True
                # move below to room manager class
                memstore = Memstore()
                data = memstore.get(room_id)
                room_info = RoomInfo.parse_obj(data)
                room_info.is_started = True
                room_info_dict = room_info.dict()
                memstore.set(room_id, room_info_dict)
                
                await manager.broadcast(room_id, "ROOMINFO", room_info_dict)
    except WebSocketDisconnect:
        print("CALLING DISCONNECT")
        await manager.disconnect(room_id=room_id, client_id=client_id)

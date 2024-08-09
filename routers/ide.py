from fastapi import APIRouter, HTTPException, status

from db.firestore import FirebaseFirestore
from models.room import RunCode
from utils.exe_code import run

router = APIRouter(prefix="/ide")
firestore = FirebaseFirestore()


@router.post("/runCode", tags=["ide"])
async def run_code(payload: RunCode):
    with open("code.txt", "w") as f:
        f.write(payload.code)
    result = run()

    return {"message": result}


@router.get("/question/{id}", tags=["ide"])
def question(id: str):
    ref = firestore.instance.collection("questions").document(id)
    data = ref.get()
    if not data.exists:
        return {"message": "question not found"}

    return {"message": data.to_dict()}

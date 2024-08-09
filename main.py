from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import ide, room

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(room.router)
app.include_router(ide.router)


@app.get("/")
def index():
    return {"message": "5mincode-api"}

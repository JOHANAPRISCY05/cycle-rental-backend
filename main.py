from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, crud
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login/", response_model=schemas.User)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return db_user

@app.post("/book/", response_model=schemas.Booking)
def book_cycle(data: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db, data)

@app.get("/host/bookings/{host_id}", response_model=List[schemas.Booking])
def get_host_bookings(host_id: int, db: Session = Depends(get_db)):
    return crud.get_bookings_by_host(db, host_id)

connections = {}

@app.websocket("/ws/{booking_id}")
async def websocket_endpoint(websocket: WebSocket, booking_id: int):
    await websocket.accept()
    if booking_id not in connections:
        connections[booking_id] = []
    connections[booking_id].append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for conn in connections[booking_id]:
                if conn != websocket:
                    await conn.send_text(data)
    except WebSocketDisconnect:
        connections[booking_id].remove(websocket)
        if not connections[booking_id]:
            del connections[booking_id]
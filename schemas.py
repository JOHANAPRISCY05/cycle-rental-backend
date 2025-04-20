from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    is_host: bool

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    is_host: bool

    class Config:
        orm_mode = True

class BookingCreate(BaseModel):
    user_id: int
    host_id: int
    location: str
    cycle_id: str
    unique_code: str

class Booking(BaseModel):
    id: int
    user_id: int
    host_id: int
    location: str
    cycle_id: str
    unique_code: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    price: Optional[float] = None

    class Config:
        orm_mode = True
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_host = Column(Boolean, default=False)

    bookings = relationship("Booking", back_populates="user")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    host_id = Column(Integer, ForeignKey("users.id"))
    location = Column(String)
    cycle_id = Column(String)
    unique_code = Column(String)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    price = Column(Float, nullable=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="bookings")
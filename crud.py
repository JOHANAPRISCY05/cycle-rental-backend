from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, password=hashed_password, is_host=user.is_host)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not pwd_context.verify(password, user.password):
        return None
    return user

def create_booking(db: Session, data: schemas.BookingCreate):
    db_booking = models.Booking(
        user_id=data.user_id,
        host_id=data.host_id,
        location=data.location,
        cycle_id=data.cycle_id,
        unique_code=data.unique_code,
        start_time=None,
        end_time=None,
        price=None,
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_bookings_by_host(db: Session, host_id: int):
    return db.query(models.Booking).filter(models.Booking.host_id == host_id).all()
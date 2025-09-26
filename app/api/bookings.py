from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.booking import BookingCreate, BookingResponse
from app.db.database import get_db
from app.db import crud_booking

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    return crud_booking.create_booking(db, booking)

@router.get("/", response_model=list[BookingResponse])
def get_all_bookings(db: Session = Depends(get_db)):
    return crud_booking.get_all_bookings(db)
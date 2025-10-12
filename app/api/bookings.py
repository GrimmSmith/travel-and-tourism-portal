from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.booking import BookingCreate, BookingResponse, BookingUpdate
from app.db.database import get_db
from app.db import crud_booking
from app.core.security import get_current_user
from app.db.models import User

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create booking for another user",
        )
    try:
        created = crud_booking.create_booking(db, booking)
        if not created:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create booking",
            )
        return created
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[BookingResponse])
def get_all_bookings(db: Session = Depends(get_db)):
    return crud_booking.get_all_bookings(db)

@router.get("/me", response_model=List[BookingResponse])
def get_my_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_booking.get_bookings_by_user(db, current_user.id)

@router.patch("/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: int,
    booking_in: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = crud_booking.update_booking(db, booking_id, booking_in)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found or update failed")
    return booking

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = crud_booking.delete_booking(db, booking_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found or deletion failed")
    return None

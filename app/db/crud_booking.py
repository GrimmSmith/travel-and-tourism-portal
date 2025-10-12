from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from app.db import models
from app.schemas.booking import BookingCreate, BookingUpdate

def create_booking(db: Session, booking_in: BookingCreate) -> Optional[models.Booking]:
    """
    Create a new booking after validating dates and guest numbers.
    """
    # Validate date range
    if booking_in.date_to < booking_in.date_from:
        raise ValueError("End date must be after start date")
    # Validate guest number
    if booking_in.number_of_guests < 1:
        raise ValueError("Number of guests must be at least 1")
    # Prevent double booking: check if destination is already booked in this period
    conflict = db.query(models.Booking).filter(
        models.Booking.destination_id == booking_in.destination_id,
        models.Booking.date_from <= booking_in.date_to,
        models.Booking.date_to >= booking_in.date_from
    ).first()
    if conflict:
        raise ValueError("Destination already booked in the selected dates")

    try:
        booking = models.Booking(
            user_id=booking_in.user_id,
            destination_id=booking_in.destination_id,
            date_from=booking_in.date_from,
            date_to=booking_in.date_to,
            number_of_guests=booking_in.number_of_guests,
            status='active'
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Failed to create booking: {e}")
        return None

def get_all_bookings(db: Session) -> List[models.Booking]:
    """
    Retrieve all bookings with destination details.
    """
    return db.query(models.Booking).options(joinedload(models.Booking.destination)).all()

def get_bookings_by_user(db: Session, user_id: int) -> List[models.Booking]:
    """
    Retrieve bookings for a specific user.
    """
    return (
        db.query(models.Booking)
          .options(joinedload(models.Booking.destination))
          .filter(models.Booking.user_id == user_id)
          .order_by(models.Booking.date_from.desc())
          .all()
    )

def update_booking(db: Session, booking_id: int, update_data: BookingUpdate) -> Optional[models.Booking]:
    """
    Update booking details such as status or number of guests.
    """
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(booking, key, value)
    try:
        db.commit()
        db.refresh(booking)
        return booking
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Failed to update booking: {e}")
        return None

def delete_booking(db: Session, booking_id: int) -> bool:
    """
    Delete a booking record by its ID.
    """
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        return False
    try:
        db.delete(booking)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Failed to delete booking: {e}")
        return False

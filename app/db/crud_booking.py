from datetime import date
from typing import List
from sqlalchemy.orm import Session, joinedload
from app.db import models
from app.schemas.booking import BookingCreate

def create_booking(db: Session, booking_in: BookingCreate) -> models.Booking:
    booking = models.Booking(
        user_id=booking_in.user_id,
        destination_id=booking_in.destination_id,
        travel_date=booking_in.date_from,  # adjust if you have both date_from/date_to fields
        number_of_people=booking_in.guests
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def get_all_bookings(db: Session) -> List[models.Booking]:
    return db.query(models.Booking).options(joinedload(models.Booking.destination)).all()

def get_bookings_by_user(db: Session, user_id: int) -> List[models.Booking]:
    return (
        db.query(models.Booking)
          .options(joinedload(models.Booking.destination))
          .filter(models.Booking.user_id == user_id)
          .order_by(models.Booking.travel_date.desc())
          .all()
    )
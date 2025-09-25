from fastapi import APIRouter
from app.schemas.booking import Booking

router = APIRouter()

# Sample data
bookings = []

@router.post("/book", response_model=Booking)
def create_booking(booking: Booking):
    bookings.append(booking)
    return booking

@router.get("/bookings", response_model=list[Booking])
def get_bookings():
    return bookings
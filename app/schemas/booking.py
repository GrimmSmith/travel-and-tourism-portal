from pydantic import BaseModel
from datetime import date

# Used when creating a new booking
class BookingCreate(BaseModel):
    user_id: int
    destination_id: int
    travel_date: date
    number_of_people: int

# Used when returning booking data from the database
class BookingResponse(BaseModel):
    id: int
    user_id: int
    destination_id: int
    travel_date: date
    number_of_people: int

    class Config:
        orm_mode = True

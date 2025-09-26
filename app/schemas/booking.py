from pydantic import BaseModel
from datetime import date

<<<<<<< HEAD
# Used when creating a new booking
class BookingCreate(BaseModel):
    user_id: int
    destination_id: int
    travel_date: date
    number_of_people: int

# Used when returning booking data from the database
class BookingResponse(BaseModel):
=======
class Booking(BaseModel):
>>>>>>> 40d9bfc9aeac22f2b3aec6c540c529306958def8
    id: int
    user_id: int
    destination_id: int
    travel_date: date
    number_of_people: int

    class Config:
<<<<<<< HEAD
        orm_mode = True
=======
        orm_mode = True
>>>>>>> 40d9bfc9aeac22f2b3aec6c540c529306958def8

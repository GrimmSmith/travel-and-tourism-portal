from pydantic import BaseModel
from datetime import date

class Booking(BaseModel):
    id: int
    user_id: int
    destination_id: int
    travel_date: date
    number_of_people: int

    class Config:
        orm_mode = True
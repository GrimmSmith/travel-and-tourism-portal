from pydantic import BaseModel, EmailStr
from typing import Optional

class BookingCreate(BaseModel):
    user_id: int
    destination_id: int
    date_from: str
    date_to: str
    guests: int

class BookingResponse(BookingCreate):
    id: int
    status: Optional[str] = "confirmed"

    class Config:
        from_attributes = True
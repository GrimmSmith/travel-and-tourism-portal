from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date
from enum import Enum

class BookingStatus(str, Enum):
    confirmed = "confirmed"
    cancelled = "cancelled"
    pending = "pending"

class BookingCreate(BaseModel):
    user_id: int = Field(..., description="ID of the user making the booking")
    destination_id: int = Field(..., description="ID of the destination to book")
    date_from: date = Field(..., description="Start date of travel (YYYY-MM-DD)")
    date_to: date = Field(..., description="End date of travel (YYYY-MM-DD)")
    guests: int = Field(..., ge=1, description="Number of guests (at least 1)")

    @validator("date_to")
    def check_date_range(cls, v, values):
        start = values.get("date_from")
        if start and v < start:
            raise ValueError("date_to must be the same as or after date_from")
        return v

    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "destination_id": 2,
                "date_from": "2025-10-01",
                "date_to": "2025-10-07",
                "guests": 2
            }
        }

class DestinationOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class BookingResponse(BaseModel):
    id: int
    user_id: int
    destination_id: int
    date_from: date
    date_to: date
    guests: int
    status: BookingStatus = BookingStatus.confirmed
    destination: Optional[DestinationOut] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 10,
                "user_id": 1,
                "destination_id": 2,
                "date_from": "2025-10-01",
                "date_to": "2025-10-07",
                "guests": 2,
                "status": "confirmed",
                "destination": {"id": 2, "name": "Goa", "description": "Sunny beaches"}
            }
        }
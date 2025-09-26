from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    destination_id = Column(Integer, ForeignKey("destinations.id"))
    travel_date = Column(Date)
    number_of_people = Column(Integer)

    user = relationship("User", back_populates="bookings")
    destination = relationship("Destination", back_populates="bookings")

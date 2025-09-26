from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # 🔁 Reverse relationship to bookings
    bookings = relationship("Booking", back_populates="user", cascade="all, delete")

# Destination model
class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)

    # 🔁 Reverse relationship to bookings
    bookings = relationship("Booking", back_populates="destination", cascade="all, delete")

# Booking model
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False)
    travel_date = Column(Date, nullable=False)
    number_of_people = Column(Integer, nullable=False)

    # 🔁 Forward relationships
    user = relationship("User", back_populates="bookings")
    destination = relationship("Destination", back_populates="bookings")
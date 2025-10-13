from typing import List, Optional
from sqlalchemy.orm import Session
from app.db import models
from app.schemas.destination import Destination as DestinationSchema

def get_all_destinations(db: Session) -> List[models.Destination]:
    return db.query(models.Destination).all()

def get_destination_by_id(db: Session, destination_id: int) -> Optional[models.Destination]:
    return db.query(models.Destination).filter(models.Destination.id == destination_id).first()

def create_destination(db: Session, dest_in: DestinationSchema) -> models.Destination:
    destination = models.Destination(
        name=dest_in.name,
        description=dest_in.description,
        location=dest_in.location,
        image_url=dest_in.image_url
    )
    db.add(destination)
    db.commit()
    db.refresh(destination)
    return destination

def update_destination(db: Session, destination_id: int, dest_in: DestinationSchema) -> Optional[models.Destination]:
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        return None
    for field, value in dest_in.dict(exclude_unset=True).items():
        setattr(destination, field, value)
    db.commit()
    db.refresh(destination)
    return destination

def delete_destination(db: Session, destination_id: int) -> bool:
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        return False
    db.delete(destination)
    db.commit()
    return True

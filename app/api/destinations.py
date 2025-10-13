from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.db.crud_destinations import (
    get_all_destinations,
    get_destination_by_id,
    create_destination,
    update_destination,
    delete_destination
)
from app.db.database import get_db
from app.schemas.destination import Destination as DestinationSchema

router = APIRouter(prefix="/api/destinations", tags=["destinations"])

@router.get("/", response_model=List[DestinationSchema])
def read_destinations(db: Session = Depends(get_db)):
    return get_all_destinations(db)

@router.get("/{destination_id}", response_model=DestinationSchema)
def read_destination(destination_id: int, db: Session = Depends(get_db)):
    dest = get_destination_by_id(db, destination_id)
    if not dest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination not found")
    return dest

@router.post("/", response_model=DestinationSchema, status_code=status.HTTP_201_CREATED)
def create_dest(destination: DestinationSchema, db: Session = Depends(get_db)):
    return create_destination(db, destination)

@router.put("/{destination_id}", response_model=DestinationSchema)
def update_dest(destination_id: int, destination: DestinationSchema, db: Session = Depends(get_db)):
    updated = update_destination(db, destination_id, destination)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination not found")
    return updated

@router.delete("/{destination_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dest(destination_id: int, db: Session = Depends(get_db)):
    if not delete_destination(db, destination_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination not found")
    return None

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
from app.core.security import get_current_admin_user


router = APIRouter(prefix="/api/destinations", tags=["destinations"])


@router.get("/", response_model=List[DestinationSchema], summary="List all destinations")
def read_destinations(db: Session = Depends(get_db)):
    """
    Retrieve a list of all available destinations.
    """
    return get_all_destinations(db)


@router.get("/{destination_id}", response_model=DestinationSchema, summary="Get a destination by ID")
def read_destination(destination_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a destination by its ID.
    """
    dest = get_destination_by_id(db, destination_id)
    if not dest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination not found")
    return dest


@router.post("/", response_model=DestinationSchema, status_code=status.HTTP_201_CREATED,
             summary="Create a new destination",
             dependencies=[Depends(get_current_admin_user)])
def create_dest(destination: DestinationSchema, db: Session = Depends(get_db)):
    """
    Create a new destination. Requires admin privileges.
    """
    return create_destination(db, destination)


@router.put("/{destination_id}", response_model=DestinationSchema,
            summary="Update an existing destination",
            dependencies=[Depends(get_current_admin_user)])
def update_dest(destination_id: int, destination: DestinationSchema, db: Session = Depends(get_db)):
    """
    Update a destination's details by its ID. Requires admin privileges.
    """
    updated = update_destination(db, destination_id, destination)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination not found")
    return updated


@router.delete("/{destination_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a destination",
               dependencies=[Depends(get_current_admin_user)])
def delete_dest(destination_id: int, db: Session = Depends(get_db)):
    """
    Delete a destination by its ID. Requires admin privileges.
    """
    if not delete_destination(db, destination_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination not found")
    return None

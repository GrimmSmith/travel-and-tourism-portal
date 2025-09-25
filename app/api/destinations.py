from fastapi import APIRouter
from app.schemas.destination import Destination

router = APIRouter()

# Sample data
destinations = [
    Destination(id=1, name="Kerala", description="Backwaters and greenery", location="South India", image_url="/static/kerala.jpg"),
    Destination(id=2, name="Jaipur", description="Palaces and heritage", location="Rajasthan", image_url="/static/jaipur.jpg"),
]

@router.get("/destinations", response_model=list[Destination])
def get_destinations():
    return destinations
from pydantic import BaseModel

class Destination(BaseModel):
    id: int
    name: str
    description: str
    location: str
    image_url: str

    class Config:
        orm_mode = True
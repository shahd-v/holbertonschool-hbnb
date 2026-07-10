from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description

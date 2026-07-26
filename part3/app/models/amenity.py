from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description

    def create(self):
        type(self)._store().append(self)
        return self

    @classmethod
    def list(cls):
        return cls._store()

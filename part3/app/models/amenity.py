from flask_restx import abort
from app.models.base_model import BaseModel
from app.utils.validators import validate_empty_input


class Amenity(BaseModel):
    def __init__(self, name, description):
        super().__init__()
        try:
            validate_empty_input(name)
            validate_empty_input(description)
        except ValueError as e:
            abort(400, str(e))
        self.name = name
        self.description = description

    def create(self):
        type(self)._store().append(self)
        return self

    @classmethod
    def list(cls):
        return cls._store()

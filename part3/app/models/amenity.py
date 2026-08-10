from app import db
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    __tablename__ = 'amenity'
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1024), nullable=False)

    def create(self):
        type(self)._store().append(self)
        return self

    @classmethod
    def list(cls):
        return cls._store()

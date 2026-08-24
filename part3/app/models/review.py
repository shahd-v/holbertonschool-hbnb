from sqlalchemy import ForeignKey

from app import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    __tablename__ = 'reviews'
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1024), nullable=False)
    place_id = db.Column(db.String(36), ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), ForeignKey('users.id'), nullable=False)

    def update_rev(self, data):
        self.update(data)

    def create(self):
        type(self)._store().append(self)
        return self

    @classmethod
    def list_by_place(cls, place):
        return [rev for rev in cls._store() if rev.place == place]

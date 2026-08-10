from sqlalchemy import ForeignKey, Integer
from app.models.place import Place
from app.models.user import User

from app import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    __tablename__ = 'review'
    rating = db.Column(Integer, nullable=False)
    comment = db.Column(db.String(1024), nullable=False)
    place = db.Column(Integer, ForeignKey(Place.id), nullable=False)
    user = db.Column(Integer, ForeignKey(User.id), nullable=False)

    def update_rev(self, data):
        self.update(data)

    def create(self):
        type(self)._store().append(self)
        return self

    @classmethod
    def list_by_place(cls, place):
        return [rev for rev in cls._store() if rev.place == place]

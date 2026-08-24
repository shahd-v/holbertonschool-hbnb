from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db
from app.models.base_model import BaseModel
from app.models.owner import Owner


class Place(BaseModel):
    __tablename__ = 'places'

    place_amenities = db.Table('place_amenities',
                    db.Column('place_id', db.String(36), db.ForeignKey('places.id'),
                                primary_key=True),
                    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'),
                                primary_key=True)
                                            )
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.String(36), ForeignKey('owners.id'), nullable=False)
    reviews = relationship('Review', backref='Places', lazy=True)
    amenities = relationship('Amenity', secondary='place_amenities', backref='places', lazy=True)


    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def create(self):
        type(self)._store().append(self)
        return self

    @classmethod
    def list(cls):
        return cls._store()

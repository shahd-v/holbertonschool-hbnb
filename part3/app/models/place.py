from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship

from app import db
from app.models.base_model import BaseModel
from app.models.owner import Owner


class Place(BaseModel):
    __tablename__ = 'places'

    place_amenities = db.Table('place_amenities',
                               db.Column('place_id', db.Integer, db.ForeignKey('places.id'),
                                         primary_key=True),
                               db.Column('amenity_id', db.Integer, db.ForeignKey('amenity.id'),
                                         primary_key=True)
                                            )

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String, nullable=False)

        # if latitude is None or latitude < -90 or latitude > 90:
        #     return False
        # if longitude is None or longitude < -180 or longitude > 180:
        #     return False

    price = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, ForeignKey(Owner.id), nullable=False)
    reviews = relationship('Review', backref='Places', lazy=True)
    amenities = relationship('Amenity', secondary=place_amenities, backref='places', lazy=True)


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

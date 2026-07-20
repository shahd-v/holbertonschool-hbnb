from app.models.base_model import BaseModel
from app.utils.validators import validate_price

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities):

        super().__init__()
        self.title = title
        self.description = description
        validate_price(price)
        def validate_lat_and_long(latitude,longitude):
            
            if latitude is None or latitude < -90 or latitude > 90:
                return False
            if longitude is None or longitude < -180 or longitude > 180:
                return False
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []      # List to store related reviews
        self.amenities = []    # List to store related amenities
        

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


from sqlalchemy.orm import relationship

from app.models.user import User


class Owner(User):
    __tablename__ = 'owner'
    places = relationship('Place', backref='Owner', lazy=True)

    def add_place(self, place):
        if not place:
            raise ValueError('Invalid input data')
        if place not in self.places:
            place.owner = self
            self.places.append(place)

    def list_places(self):
        return self.places.copy()

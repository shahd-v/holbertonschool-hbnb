from app.models.user import User
from app.utils.validators import validate_email


class Owner(User):
    def __init__(self, first_name, last_name, email, password):
        super().__init__(first_name, last_name, email, password)
        try:
            validate_email(email)
        except ValueError as e:
            abort(400, str(e))
        self.email = email
        self.places = []

    def add_place(self, place):
        if not place:
            raise ValueError('Invalid input data')
        if place not in self.places:
            place.owner = self
            self.places.append(place)

    def list_places(self):
        return self.places.copy()

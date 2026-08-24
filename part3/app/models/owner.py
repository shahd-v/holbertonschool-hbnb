from flask_bcrypt import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship

from app import db
from app.models.base_model import BaseModel


class Owner(BaseModel):
    __tablename__ = 'owners'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    places = relationship('Place', backref='Owner', lazy=True)

    def register(self):
        type(self)._store().append(self)
        return self

    def update_profile(self, data):
        self.update(data)

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify a password against the stored hash."""
        return check_password_hash(self.password, password)

    def add_place(self, place):
        if not place:
            raise ValueError('Invalid input data')
        if place not in self.places:
            place.owner = self
            self.places.append(place)

    def list_places(self):
        return self.places.copy()

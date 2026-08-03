import bcrypt

from app.models.base_model import BaseModel
from app.utils.validators import validate_empty_input


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None):
        super().__init__()
        validate_empty_input(first_name)
        validate_empty_input(last_name)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password or ""

    def register(self):
        type(self)._store().append(self)
        return self

    def update_profile(self, data):
        self.update(data)

    def hash_password(self, password):
        # Hashes the password before storing it.
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        # Verifies if the provided password matches the hashed password.
        return bcrypt.check_password_hash(self.password, password)

from flask_bcrypt import generate_password_hash, check_password_hash
from app.models.base_model import BaseModel
from app.utils.validators import validate_empty_input


class User(BaseModel):
    is_admin = False
    def __init__(self, first_name, last_name, email, password):
        super().__init__()
        validate_empty_input(first_name)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)

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

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_restx import abort
from app.models.base_model import BaseModel
from app.utils.validators import validate_email, validate_empty_input



class User(BaseModel):
    is_admin = False
    def __init__(self, first_name, last_name, email, password):
        super().__init__()

        try:
            validate_empty_input(first_name)
            validate_empty_input(last_name)
            validate_empty_input(password)
        except ValueError as e:
            abort(400, str(e))
        self.first_name = first_name
        self.last_name = last_name

        try:
            validate_email(email)
            self.email = email
        except ValueError as e:
            abort(400, str(e))

        self.hash_password(password)

    def register(self):
        type(self)._store().append(self)
        return self

    def update_profile(self, data):
        fields_to_validate = ['first_name', 'last_name', 'password']

        try:
            for field in fields_to_validate:
                if field in data:
                    validate_empty_input(data[field])
        except ValueError as e:
            abort(400, str(e))

        try:
            if 'email' in data:
                validate_email(data['email'])
        except ValueError as e:
            abort(400, str(e))
        self.update(data)

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify a password against the stored hash."""
        return check_password_hash(self.password, password)

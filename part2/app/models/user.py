from app.models.base_model import BaseModel
from app.utils.validators import validate_email


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        if not validate_email(email):
            raise ValueError(f"Invalid email format: {email}")
        self.email = email
        self.password = password

    def register(self):
        type(self)._store().append(self)
        return self

    def update_profile(self, data):
        self.update(data)

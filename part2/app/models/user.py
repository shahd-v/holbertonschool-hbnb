from app.models.base_model import BaseModel
from app.utils.validators import validate_empty_input

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password):
        super().__init__()
        validate_empty_input(first_name)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def register(self):
        type(self)._store().append(self)
        return self

    def update_profile(self, data):
        self.update(data)

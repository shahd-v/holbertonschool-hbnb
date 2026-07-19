from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def register(self):
        type(self)._store().append(self)
        return self

    def update_profile(self, data):
        self.update(data)

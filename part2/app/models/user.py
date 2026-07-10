from app.models.base_model import BaseModel

class User(BaseModel):
    users = []
    def __init__(self, first_name, last_name, email, password):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.passwprd = password

    def register(self):
        User.users.append(self)
        return self
    
    def update_profile(self, data):
        self.update(data)
    
    def delete(self):
        if self in User.users:
            User.users.remove(self)
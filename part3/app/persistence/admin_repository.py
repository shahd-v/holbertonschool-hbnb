from app.persistence.user_repository import UserRepository

class AdminRepository(UserRepository):
    def __init__(self):
        super().__init__()

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def check_is_admin(self, current_user_id):
        return self.model.query.get(current_user_id)
        # if not self.model.query.get(current_user_id):
        #     return False
        # return True

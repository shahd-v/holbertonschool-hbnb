from app.models.admin import Admin
from app.persistence.repository import SQLAlchemyRepository


class AdminRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Admin)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def check_is_admin(self, current_user_id):
        return self.model.query.get(current_user_id)

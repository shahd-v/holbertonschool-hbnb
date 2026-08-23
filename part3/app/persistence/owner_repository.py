from app.models.owner import Owner
from app.persistence.repository import SQLAlchemyRepository


class OwnerRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Owner)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def check_is_owner(self, current_user_id):
        return self.model.query.get(current_user_id)

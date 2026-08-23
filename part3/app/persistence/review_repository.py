from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def check_rev_exist(self, review_data):
        # Check if review already exists for this user and place
        existing_review = self.model.query.filter_by(
            user_id=review_data['user_id'],
            place_id=review_data['place_id']).first()
        if existing_review:
            raise ValueError ('Review already exists for this place')

from app.models.base_model import BaseModel
from app.utils.validators import validate_rating


class Review(BaseModel):
    def __init__(self, rating, comment, place, user):
        super().__init__()
        validate_rating(rating)
        self.rating = rating
        self.comment = comment
        self.place = place
        self.user = user

    def create(self):
        type(self)._store().append(self)
        return self

    @classmethod
    def list_by_place(cls, place):
        return [rev for rev in cls._store() if rev.place == place]

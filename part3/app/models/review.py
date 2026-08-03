from flask import abort

from app.models.base_model import BaseModel
from app.utils.validators import validate_empty_input, validate_rating


class Review(BaseModel):
    def __init__(self, rating, comment, place, user):
        super().__init__()
        try:
            validate_rating(rating)
        except ValueError as e:
            abort(400, str(e))
        self.rating = rating

        try:
            validate_empty_input(comment)
        except ValueError as e:
            abort(400, str(e))
        self.comment = comment

        self.place = place
        self.user = user

    def update_rev(self, data):

        try:
            validate_rating(data['rating']):
        except ValueError as e:
            abort(400, str(e))
        try:
            validate_empty_input(data['comment']):
        except ValueError as e:
            abort(400, str(e))

        self.update(data)

    def create(self):
        type(self)._store().append(self)
        return self

    @classmethod
    def list_by_place(cls, place):
        return [rev for rev in cls._store() if rev.place == place]

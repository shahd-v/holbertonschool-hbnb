from app.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, rating, comment, place, user):
        super().__init__()
        self.rating = rating
        self.comment = comment
        self.place = place
        self.user = user

    def create(self):
        type(self)._store().append(self)
        return self

    @classmethod
    def list_by_place(cls, place):
        return [r for r in cls._store() if r.place == place]

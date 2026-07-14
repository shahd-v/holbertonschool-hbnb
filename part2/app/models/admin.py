from app.models.user import User


class Admin(User):
    def manage_users(self):
        return User._store()

    def manage_places(self):
        from app.models.place import Place
        return Place._store()

    def manage_amenities(self):
        from app.models.amenity import Amenity
        return Amenity._store()

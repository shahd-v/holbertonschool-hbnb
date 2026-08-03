from types import SimpleNamespace

from app.models.user import User
from app.models.owner import Owner
from app.models.admin import Admin
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.owner_repo = InMemoryRepository()
        self.admin_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ---------------- User ----------------
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(user_data)
        return user

    def delete_user(self, user_id):
        """Delete a user."""
        raise NotImplementedError


    # ---------------- Admin ----------------
    def create_admin(self, admin_data):
        admin = Admin(**admin_data)
        self.admin_repo.add(admin)
        return admin

    def get_admin(self, admin_id):
        return self.admin_repo.get(admin_id)

    def get_admin_by_email(self, email):
        return self.admin_repo.get_by_attribute('email', email)

    def get_all_admins(self):
        return self.admin_repo.get_all()

    def update_admin(self, admin_id, admin_data):
        admin = self.admin_repo.get(admin_id)
        if not admin:
            return None
        admin.update(admin_data)
        return admin

    # ---------------- Owner ----------------
    def create_owner(self, owner_data):
        payload = dict(owner_data)
        payload.setdefault('password', '')
        owner = Owner(**payload)
        self.owner_repo.add(owner)
        return owner

    def get_owner(self, owner_id):
        return self.owner_repo.get(owner_id)

    def get_owner_by_email(self, email):
        return self.owner_repo.get_by_attribute('email', email)

    def get_all_owners(self):
        return self.owner_repo.get_all()

    def update_owner(self, owner_id, owner_data):
        owner = self.owner_repo.get(owner_id)
        if not owner:
            return None
        owner.update(owner_data)
        return owner


    # ---------------- Amenity ----------------
    def create_amenity(self, amenity_data):
        payload = dict(amenity_data)
        payload.setdefault('description', '')
        amenity = Amenity(**payload)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity

    # ---------------- Place ----------------
    def create_place(self, place_data):
        price = place_data.get('price')
        latitude = place_data.get('latitude')
        longitude = place_data.get('longitude')

        if price is None or price < 0:
            raise ValueError("Invalid price")
        if latitude is None or latitude < -90 or latitude > 90:
            raise ValueError("Invalid latitude")
        if longitude is None or longitude < -180 or longitude > 180:
            raise ValueError("Invalid longitude")

        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        place.update(place_data)
        return place

    def delete_place(self, place_id):
        """Delete a place."""
        raise NotImplementedError

    # ---------------- Review ----------------
    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id') or review_data.get('property_id')

        user = self.get_user(user_id) if user_id is not None else None
        place = self.get_place(place_id) if place_id is not None else None

        if not user:
            user = SimpleNamespace(id=user_id)
        if not place:
            place = SimpleNamespace(id=place_id, reviews=[], amenities=[])
            place.add_review = lambda review: place.reviews.append(review)

        review = Review(
            review_data['rating'],
            review_data['comment'],
            place,
            user
        )
        self.review_repo.add(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return None
        return [rev for rev in self.review_repo.get_all()
            if rev.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return review
